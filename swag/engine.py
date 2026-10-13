"""Reference comparison, independent controls, and contextual precedent lookup."""
from __future__ import annotations

import csv
import re
from pathlib import Path

from .document import extract_file

HEADING = re.compile(r"^(\d+)\.\s+(.+)$")
PARTIES = re.compile(r"^This Mutual Non-Disclosure Agreement is made between [A-Za-z0-9 &'’-]+(?:Ltd|Limited|Inc|LLC|Corp) and [A-Za-z0-9 &'’-]+(?:Ltd|Limited|Inc|LLC|Corp)\. ")
SIGNATURES = re.compile(r"^Signed for [^:]+: _+\s+Signed for [^:]+: _+$")
ROUTE_ORDER = {"routine_candidate": 0, "review_required": 1, "escalate": 2, "blocked_extraction": 3}
STOP = set("a an and are as at be by each for from in is it of on or shall the this to under with confidential information receiving party agreement purpose disclosure".split())


def normal(text):
    return " ".join(text.lower().split())


def clauses(document):
    """Group ordered body paragraphs under headings; keep annex and stray paragraphs."""
    found = {}
    current = None
    for unit in document["units"]:
        if unit["part"] != "word/document.xml":
            continue
        text = unit["text"]
        match = HEADING.match(text)
        if match:
            title = normal(match.group(2))
            current = title
            found.setdefault(title, {"title": match.group(2), "number": match.group(1), "units": [], "heading_anchor": unit["anchor"]})
        elif text.lower().startswith(("schedule ", "appendix ", "annex ")):
            current = "supplement:" + normal(text)
            found[current] = {"title": text, "number": "", "units": [], "heading_anchor": unit["anchor"]}
        elif SIGNATURES.fullmatch(text):
            current = None
        elif current is not None:
            found[current]["units"].append(unit)
        elif text != "MUTUAL NON-DISCLOSURE AGREEMENT" and not re.fullmatch(r"Document ID: [A-Za-z0-9-]+\s*\|\s*Synthetic demonstration material", text):
            key = "unsectioned:" + unit["anchor"]
            found[key] = {"title": "Unsectioned text", "number": "", "units": [unit], "heading_anchor": unit["anchor"]}
    return found


def _finding(category, route, title, explanation, sources, reference=None, method="deterministic", uncertainty="", related=None):
    return {"id": category + ":" + (sources[0]["anchor"] if sources else reference["anchor"] if reference else title), "category": category, "route": route, "title": title, "explanation": explanation, "sources": sources, "reference": reference, "related": related or [], "method": method, "uncertainty": uncertainty}


def compare(reference, incoming):
    baseline = clauses(reference)
    current = clauses(incoming)
    findings = []
    for title, before in baseline.items():
        after = current.get(title)
        if after is None:
            ref_unit = before["units"][0] if before["units"] else {"anchor": before["heading_anchor"], "text": before["title"]}
            route = "escalate" if title == "no licence" else "review_required"
            findings.append(_finding("missing_clause", route, "Missing: " + before["title"], "This reference provision has no matching heading in the incoming document. Check the whole original for differently placed wording.", [], ref_unit, uncertainty="Absence of a heading does not prove absence of equivalent protection elsewhere."))
            continue
        def comparable(section):
            text = "\n".join(u["text"] for u in section["units"])
            if title == "parties and purpose" and PARTIES.match(text):
                text = PARTIES.sub("This Mutual Non-Disclosure Agreement is made between [named parties]. ", text, count=1)
            return normal(text)
        old = comparable(before)
        new = comparable(after)
        if old != new or before["number"] != after["number"]:
            source = after["units"] if after["units"] else [{"anchor": after["heading_anchor"], "text": after["title"]}]
            reference_unit = before["units"][0] if before["units"] else {"anchor": before["heading_anchor"], "text": before["title"]}
            findings.append(_finding("changed_clause", "review_required", "Changed: " + before["title"], "Wording or numbering differs from the reference. Review the source beside the reference; semantic equivalence is not assumed.", source, reference_unit, uncertainty="Textual difference; legal effect requires human judgement."))
    for title, after in current.items():
        if title not in baseline:
            source = after["units"] or [{"anchor": after["heading_anchor"], "text": after["title"]}]
            findings.append(_finding("added_section", "review_required", "Added: " + after["title"], "This section is not in the reference document.", source))
    return findings


def whole_document_controls(reference, incoming):
    """Check every extracted unit, independently of diff and retrieved precedent."""
    findings = []
    body = [u for u in incoming["units"] if u["part"] == "word/document.xml"]
    base = clauses(reference)
    current = clauses(incoming)
    if "no licence" in base and "no licence" not in current:
        ref = base["no licence"]
        ref_unit = ref["units"][0] if ref["units"] else {"anchor": ref["heading_anchor"], "text": ref["title"]}
        findings.append(_finding("protection_absent", "escalate", "No-licence protection is missing", "The reference has a no-licence provision; the incoming document has no matching section. This is a structural absence, not a legal conclusion.", [], ref_unit))
    for unit in body:
        text = normal(unit["text"])
        # These are broad legal-language indicators, not exhaustive legal classification.
        grants_right = bool(re.search(r"\b(?:licen[cs]e|commercially exploit|develop and market|unrestricted use)\b", text))
        broad_scope = bool(re.search(r"\b(?:perpetual|irrevocable|without restriction|any business purpose|competing products|commercially exploit)\b", text))
        if grants_right and broad_scope:
            related = current.get("no licence", {}).get("units", [])[:1] + current.get("permitted use", {}).get("units", [])[:1]
            findings.append(_finding("broad_rights", "escalate", "Potentially broad use or IP rights", "The quoted wording appears to grant or preserve use beyond the reference purpose. Compare it with the linked no-licence and permitted-use provisions.", [unit], uncertainty="Pattern-based flag; a reviewer must interpret the complete provision.", related=related))
        if re.search(r"\b(?:despite|notwithstanding|prevails|override[sd]?)\b", text) and re.search(r"\b(?:clause|provision|agreement|schedule|term)\b", text):
            related = current.get("permitted use", {}).get("units", [])[:1] + current.get("no licence", {}).get("units", [])[:1]
            findings.append(_finding("override", "escalate", "Possible override or conflict", "This wording may take precedence over another provision. Inspect the linked main provisions and the rest of the document.", [unit], uncertainty="The actual legal effect depends on the full agreement.", related=related))
    return findings


def _tokens(text):
    return {word for word in re.findall(r"[a-z]{3,}", text.lower()) if word not in STOP}


def precedents(findings, reference, historical, decisions, limit=3):
    terms = set()
    titles = set()
    for finding in findings:
        terms |= _tokens(" ".join(u["text"] for u in finding["sources"]))
        titles |= _tokens(finding["title"])
    ranked = []
    baseline = clauses(reference)
    concern_categories = {f["category"] for f in findings}
    changed_titles = {normal(f["title"].split(":", 1)[-1]) for f in findings if f["category"] == "changed_clause"}
    for document_id, doc in historical.items():
        best = (0, None)
        prior_categories = {f["category"] for f in whole_document_controls(reference, doc)}
        for title, section in clauses(doc).items():
            if title == "parties and purpose":
                continue
            prior = baseline.get(title)
            if prior and normal(" ".join(u["text"] for u in prior["units"])) == normal(" ".join(u["text"] for u in section["units"])):
                continue
            for unit in section["units"]:
                overlap = len(terms & _tokens(unit["text"]))
                title_overlap = len(titles & _tokens(section["title"]))
                score = overlap + title_overlap * 3
                if title in changed_titles:
                    score += 12
                if concern_categories & prior_categories:
                    score += 20
                if score > best[0]:
                    best = (score, unit)
        if best[1] is not None and best[0] >= 5:
            ranked.append((best[0], document_id, best[1]))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    out = []
    for score, document_id, unit in ranked[:limit]:
        decision = decisions[document_id]
        out.append({"document_id": document_id, "filename": historical[document_id]["filename"], "source": unit, "decision": decision["decision"], "date": decision["decision_date"], "rationale": decision["rationale"], "reuse_authority": decision["reuse_authority"], "why_retrieved": "Shared wording or clause topic; lexical baseline (score %d)." % score})
    if not out and changed_titles:
        for document_id, doc in sorted(historical.items()):
            standard = clauses(doc)
            for title in sorted(changed_titles):
                if title in standard and title in baseline and normal(" ".join(u["text"] for u in standard[title]["units"])) == normal(" ".join(u["text"] for u in baseline[title]["units"])) and standard[title]["units"]:
                    decision = decisions[document_id]
                    out.append({"document_id": document_id, "filename": doc["filename"], "source": standard[title]["units"][0], "decision": decision["decision"], "date": decision["decision_date"], "rationale": decision["rationale"], "reuse_authority": decision["reuse_authority"], "why_retrieved": "Same clause topic in a previously reviewed standard provision; not evidence that the changed wording is equivalent."})
                    break
            if out:
                break
    return out


def analyse(reference, incoming, historical, decisions):
    if incoming["coverage"]["status"] != "complete":
        return {"route": "blocked_extraction", "findings": [], "precedents": [], "checks": {"extraction": "blocked", "comparison": "not run", "whole_document": "not run", "ai": "not run"}, "reason": "Document content could not be fully accounted for. Manual review is required."}
    findings = compare(reference, incoming) + whole_document_controls(reference, incoming)
    # Coalesce structural and independent-control descriptions of the same absence.
    if any(f["category"] == "protection_absent" for f in findings):
        findings = [f for f in findings if not (f["category"] == "missing_clause" and f["title"].lower().endswith("no licence"))]
    priority = {"broad_rights": 0, "protection_absent": 1, "override": 2, "added_section": 3, "missing_clause": 4, "changed_clause": 5}
    findings.sort(key=lambda finding: (-ROUTE_ORDER[finding["route"]], priority.get(finding["category"], 9)))
    route = max((f["route"] for f in findings), key=lambda value: ROUTE_ORDER[value], default="routine_candidate")
    context = precedents(findings, reference, historical, decisions) if findings else []
    reason = findings[0]["title"] if findings else "No material wording difference found; party details still need confirmation."
    return {"route": route, "findings": findings, "precedents": context, "checks": {"extraction": "complete", "comparison": "complete", "whole_document": "complete", "ai": "not run"}, "reason": reason}


def load_library(root: Path):
    reference = extract_file(next((root / "dataset/reference").glob("*.docx")))
    historical = {path.name.split("-", 1)[0]: extract_file(path) for path in sorted((root / "dataset/historical").glob("*.docx"))}
    incoming = {path.name.split("-", 1)[0]: extract_file(path) for path in sorted((root / "dataset/incoming").glob("*.docx"))}
    with (root / "dataset/review_records/historical_decisions.csv").open(newline="") as handle:
        decisions = {row["document_id"]: row for row in csv.DictReader(handle)}
    if set(decisions) != set(historical):
        raise ValueError("Historical decision IDs do not match historical documents")
    if any(doc["coverage"]["status"] != "complete" for doc in [reference, *historical.values()]):
        raise ValueError("Reference or historical extraction incomplete")
    return reference, historical, incoming, decisions
