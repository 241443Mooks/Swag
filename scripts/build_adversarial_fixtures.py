"""Build an independent synthetic challenge set from the unchanged T01 fixture.

Run from the repository root. The generated DOCX files are committed so a
reviewer can inspect the exact inputs used for both audit runs.
"""
from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dataset/incoming/T01-template-match.docx"
DEST = ROOT / "dataset/adversarial"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def paragraph(text):
    item = ET.Element(W + "p")
    ET.SubElement(ET.SubElement(item, W + "r"), W + "t").text = text
    return item


def body_insert(root, text):
    body = root.find(W + "body")
    body.insert(len(body) - 1, paragraph(text))


def replace_text(root, old, new):
    matches = [node for node in root.iter(W + "t") if node.text and old in node.text]
    if len(matches) != 1:
        raise ValueError(f"Expected one occurrence of {old!r}; found {len(matches)}")
    matches[0].text = matches[0].text.replace(old, new)


def replace_all(root, old, new):
    for node in root.iter(W + "t"):
        if node.text:
            node.text = node.text.replace(old, new)


def edit_document(source, change, part="word/document.xml", duplicate=False):
    output = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(source)) as original, zipfile.ZipFile(output, "w") as changed:
        duplicate_contents = original.read(part) if duplicate else None
        for member in original.infolist():
            contents = original.read(member.filename)
            if member.filename == part:
                xml = ET.fromstring(contents)
                change(xml)
                contents = ET.tostring(xml, encoding="utf-8", xml_declaration=True)
            changed.writestr(member, contents)
        if duplicate:
            # ZIP permits duplicate member names; last-wins lookups conceal ambiguity.
            changed.writestr(part, duplicate_contents)
    return output.getvalue()


def hidden_no_licence(root):
    for item in root.findall(".//" + W + "p"):
        text = "".join(node.text or "" for node in item.iter(W + "t"))
        if text.startswith("No intellectual property licence"):
            for run in item.findall(W + "r"):
                properties = run.find(W + "rPr")
                if properties is None:
                    properties = ET.Element(W + "rPr")
                    run.insert(0, properties)
                ET.SubElement(properties, W + "vanish")
            return
    raise ValueError("No-licence paragraph not found")


def duplicate_heading(root):
    body_insert(root, "9. No Licence")
    body_insert(root, "The recipient may incorporate disclosed know-how into its products without further consent.")


def relocate_paragraph(root):
    body = root.find(W + "body")
    for item in list(body):
        text = "".join(node.text or "" for node in item.iter(W + "t"))
        if text.startswith("No intellectual property licence"):
            body.remove(item)
            body.insert(len(body) - 1, item)
            return
    raise ValueError("No-licence paragraph not found")


def build():
    base = SOURCE.read_bytes()
    DEST.mkdir(parents=True, exist_ok=True)
    cases = [
        ("A01-footer-grant", "Critical right in footer", "Footer grants product-development use while body matches reference.", "escalate", True, lambda: edit_document(base, lambda xml: xml.append(paragraph("The recipient may use disclosed know-how to develop competing products without consent.")), "word/footer1.xml")),
        ("A02-header-override", "Critical override in header", "Header overrides the permitted-use restriction.", "escalate", True, lambda: edit_document(base, lambda xml: xml.append(paragraph("Despite clause 3, the recipient may use Confidential Information for product development.")), "word/header1.xml")),
        ("A03-hidden-protection", "Hidden protection", "No-licence paragraph is formatted as hidden text.", "blocked_extraction", True, lambda: edit_document(base, hidden_no_licence)),
        ("A04-duplicate-part", "Ambiguous package", "ZIP contains duplicate document.xml members.", "blocked_extraction", True, lambda: edit_document(base, lambda xml: None, duplicate=True)),
        ("A05-duplicate-heading", "Duplicate clause heading", "A second clause 9 adds a product-use grant under the same heading.", "review_required", True, lambda: edit_document(base, duplicate_heading)),
        ("A06-empty-protection", "Protection hollowed out", "No-licence heading remains but its prohibition is replaced by a grant.", "escalate", True, lambda: edit_document(base, lambda xml: replace_text(xml, "No intellectual property licence or other right is granted by disclosure except the limited right to use Confidential Information for the Purpose.", "The recipient may incorporate disclosed know-how into its products without further consent."))),
        ("A07-negation-flip", "Permitted-use negation", "Clause 3 changes shall not use to may use.", "review_required", True, lambda: edit_document(base, lambda xml: replace_text(xml, "shall not use it for any other purpose", "may use it for any other purpose"))),
        ("A08-unfamiliar-grant", "Unfamiliar broad grant", "An added paragraph allows incorporating know-how into products without an explicit licence word.", "review_required", True, lambda: edit_document(base, lambda xml: body_insert(xml, "The recipient may incorporate any disclosed know-how into its products without further consent."))),
        ("A09-negated-licence", "Negated broad-right wording", "Added wording explicitly denies a perpetual licence; must not be treated as an affirmative grant.", "review_required", False, lambda: edit_document(base, lambda xml: body_insert(xml, "Neither party receives a perpetual licence to commercially exploit Confidential Information."))),
        ("A10-protective-override", "Protective cross-reference", "Added notwithstanding sentence strengthens the permitted-use restriction.", "review_required", False, lambda: edit_document(base, lambda xml: body_insert(xml, "Notwithstanding clause 3, the recipient shall not use Confidential Information for any other purpose."))),
        ("A11-party-only", "Administrative party change", "Only the counterparty name differs from T01.", "routine_candidate", False, lambda: edit_document(base, lambda xml: replace_all(xml, "Birchbridge Ltd", "Mapleline Ltd"))),
        ("A12-unchanged", "Exact supported template", "Byte-identical T01 for a routine-route control.", "routine_candidate", False, lambda: base),
        ("A13-displaced-protection", "Displaced protection", "No-licence wording moves after signatures, leaving its heading with no body.", "review_required", True, lambda: edit_document(base, relocate_paragraph)),
    ]
    manifest = []
    for stem, risk, change, expected, critical, make in cases:
        filename = stem + ".docx"
        (DEST / filename).write_bytes(make())
        manifest.append({"id": stem[:3], "file": filename, "risk": risk, "change": change, "expected_route": expected, "critical_exception": critical})
    (DEST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    build()
