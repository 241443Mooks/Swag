"""Loopback-only web app for synthetic NDA review."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

from .ai import AIService, AIUnavailable
from .document import extract
from .engine import analyse, clauses, load_library, ROUTE_ORDER
from .ledger import KnowledgeLedger, Ledger


class App:
    def __init__(self, root: Path, state_dir: Path):
        self.root = root
        self.state_dir = state_dir
        self.reference, self.historical, incoming, self.decisions = load_library(root)
        self.contracts = {}
        for document_id, document in incoming.items():
            self.contracts[document_id] = {"document": document, "path": next((root / "dataset/incoming").glob(document_id + "-*.docx"))}
        uploads = state_dir / "uploads"
        if uploads.exists():
            if list(uploads.glob("*.uploading")) or list(uploads.glob("*.recording")):
                raise ValueError("Upload recovery required: interrupted write detected")
            metadata = {path.stem: path for path in uploads.glob("*.json")}
            originals = {path.stem: path for path in uploads.glob("*.docx")}
            if set(metadata) != set(originals):
                raise ValueError("Upload recovery required: original and metadata files do not match")
            for stem, meta_path in metadata.items():
                meta = json.loads(meta_path.read_text())
                path = originals[stem]
                data = path.read_bytes()
                digest = hashlib.sha256(data).hexdigest()
                if digest != stem or meta.get("sha256") != digest or meta.get("id") != "U-" + digest[:10] or not meta.get("filename"):
                    raise ValueError("Upload recovery required: source identity mismatch for " + stem)
                self.contracts[meta["id"]] = {"document": extract(data, meta["filename"]), "path": path}
        self.ledger = Ledger(state_dir / "decisions.jsonl")
        self.knowledge = KnowledgeLedger(state_dir / "knowledge.jsonl")
        self.active_precedents()  # Fail visibly on broken publication history or source links.
        self.ai = AIService()
        self.ai_results = {}

    def active_precedents(self):
        decisions = {event["id"]: event for event in self.ledger.all()}
        records = []
        for event in self.knowledge.active():
            item = self.contracts.get(event["document_id"])
            decision = decisions.get(event["decision_id"])
            if not item or not decision or decision["sha256"] != event["sha256"] or decision["decision"] != event["decision"] or decision["rationale"] != event["rationale"] or decision.get("conditions", "") != event["conditions"]:
                raise ValueError("Published precedent has a broken decision or document link; retrieval unavailable")
            document = item["document"]
            source = next((unit for unit in document["units"] if unit["anchor"] == event["source_anchor"]), None)
            try:
                source_matches = hashlib.sha256(item["path"].read_bytes()).hexdigest() == event["sha256"]
            except OSError:
                source_matches = False
            if document["sha256"] != event["sha256"] or document["coverage"]["status"] != "complete" or not source_matches or not source or source["text"] != event["source_text"]:
                raise ValueError("Published precedent source is unavailable or changed; retrieval unavailable")
            considered = decision.get("considered_sources", [])
            evidence_matches = any(row.get("finding_id") == event["finding_id"] and row.get("anchor") == event["source_anchor"] and row.get("text") == event["source_text"] for row in considered)
            if event["finding_id"] not in decision["finding_ids"] or not evidence_matches or decision["timestamp"] > event["timestamp"]:
                raise ValueError("Published precedent no longer matches its reviewed evidence; retrieval unavailable")
            records.append({**event, "document": document, "source": source})
        return records

    def publish(self, document_id, decision_id, source_anchor, authoriser, context, reuse_limits):
        detail = self.detail(document_id)
        if detail["analysis"]["route"] == "blocked_extraction":
            raise ValueError("Complete extraction and source integrity are required before publication")
        decision = next((event for event in detail["history"] if event["id"] == decision_id), None)
        if not decision:
            raise ValueError("Choose a recorded decision for this exact document")
        evidence = next((row for row in decision.get("considered_sources", []) if row["anchor"] == source_anchor and row["finding_id"] in decision["finding_ids"]), None)
        source = next((unit for unit in detail["document"]["units"] if unit["anchor"] == source_anchor), None)
        if not evidence or not source or source["text"] != evidence["text"]:
            raise ValueError("Choose a source passage from a finding considered in this decision")
        section_title = next((section["title"] for section in clauses(detail["document"]).values() if any(unit["anchor"] == source_anchor for unit in section["units"])), "")
        if not section_title:
            raise ValueError("The source passage has no reviewable section")
        return self.knowledge.publish(decision, document_id, evidence["finding_id"], source, section_title, authoriser, context, reuse_limits)

    def withdraw(self, publication_id, actor, reason):
        return self.knowledge.withdraw(publication_id, actor, reason)

    def analysis(self, document_id):
        item = self.contracts[document_id]
        document = item["document"]
        try:
            source_matches = hashlib.sha256(item["path"].read_bytes()).hexdigest() == document["sha256"]
        except OSError:
            source_matches = False
        if not source_matches:
            issue = "Original source is unavailable or changed after intake; analysis cannot be trusted"
            damaged = {**document, "coverage": {**document["coverage"], "status": "blocked", "issues": [*document["coverage"]["issues"], issue]}}
            report = analyse(self.reference, damaged, self.historical, self.decisions)
            report["assurance"]["source_integrity"]["status"] = "mismatch"
            return report
        return analyse(self.reference, document, self.historical, self.decisions, self.active_precedents())

    def queue(self):
        latest = {}
        for event in self.ledger.all():
            latest[event["sha256"]] = event
        rows = []
        for document_id, item in self.contracts.items():
            document = item["document"]
            review = self.analysis(document_id)
            rows.append({"id": document_id, "filename": document["filename"], "display_name": self.display_name(document), "sha256": document["sha256"], "route": review["route"], "reason": review["reason"], "findings_count": len(review["findings"]), "latest_decision": latest.get(document["sha256"])})
        return sorted(rows, key=lambda row: (-ROUTE_ORDER[row["route"]], row["id"]))

    def detail(self, document_id):
        document = self.contracts[document_id]["document"]
        history = self.ledger.all(document["sha256"])
        knowledge_events = self.knowledge.all()
        publications = []
        for event in knowledge_events:
            if event["type"] != "publish" or event["sha256"] != document["sha256"]:
                continue
            withdrawal = next((row for row in knowledge_events if row["type"] == "withdraw" and row["publication_id"] == event["id"]), None)
            publications.append({**event, "status": "withdrawn" if withdrawal else "active", "withdrawal": withdrawal})
        analysis = self.analysis(document_id)
        analysis["assurance"]["human_review"] = {"status": "recorded" if history else "not recorded", "last_decision": history[-1]["decision"] if history else None, "events": len(history)}
        return {"id": document_id, "display_name": self.display_name(document), "document": document, "reference": self.reference, "analysis": analysis, "history": history, "publications": publications, "ai": self.ai.status(), "ai_results": self.ai_results.get(document["sha256"], [])}

    @staticmethod
    def display_name(document):
        for unit in document["units"]:
            if unit["part"] == "word/document.xml":
                match = re.search(r"made between (.+?) and (.+?)\. The parties wish", unit["text"])
                if match:
                    parties = [match.group(1), match.group(2)]
                    other = next((party for party in parties if party != "Northbridge Systems Ltd"), parties[0])
                    return other + " · Mutual NDA"
        return document["filename"].removesuffix(".docx")

    def upload(self, data, filename):
        document = extract(data, filename)
        document_id = "U-" + document["sha256"][:10]
        target = self.state_dir / "uploads"
        target.mkdir(parents=True, exist_ok=True)
        file_path = target / (document["sha256"] + ".docx")
        if not file_path.exists():
            temporary = target / (document["sha256"] + ".uploading")
            with temporary.open("xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, file_path)
        elif hashlib.sha256(file_path.read_bytes()).hexdigest() != document["sha256"]:
            raise ValueError("Existing uploaded original does not match its source hash")
        meta_path = target / (document["sha256"] + ".json")
        if not meta_path.exists():
            temporary = target / (document["sha256"] + ".recording")
            with temporary.open("x") as handle:
                json.dump({"id": document_id, "sha256": document["sha256"], "filename": document["filename"]}, handle)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, meta_path)
        self.contracts[document_id] = {"document": document, "path": file_path}
        return document_id


class Handler(BaseHTTPRequestHandler):
    app: App

    def log_message(self, fmt, *args):
        # Do not log submitted contract text, reviewer rationales or keys.
        print("HTTP", self.address_string(), fmt % args)

    def _json(self, value, status=200):
        body = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status, message):
        self._json({"error": message}, status)

    def _body(self, limit=2_100_000):
        length = int(self.headers.get("Content-Length", "0"))
        if length < 1 or length > limit:
            raise ValueError("Request size is missing or exceeds the local limit")
        return self.rfile.read(length)

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path == "/api/queue":
            try:
                return self._json({"items": self.app.queue()})
            except ValueError as exc:
                return self._error(409, str(exc))
        if path.startswith("/api/contracts/"):
            parts = path.split("/")
            if len(parts) not in (4, 5) or parts[3] not in self.app.contracts:
                return self._error(404, "Contract not found")
            document_id = parts[3]
            if len(parts) == 4:
                try:
                    return self._json(self.app.detail(document_id))
                except ValueError as exc:
                    return self._error(409, str(exc))
            if parts[4] != "original":
                return self._error(404, "Not found")
            try:
                data = self.app.contracts[document_id]["path"].read_bytes()
            except OSError:
                return self._error(409, "Original source unavailable; stop review and inspect local files")
            if hashlib.sha256(data).hexdigest() != self.app.contracts[document_id]["document"]["sha256"]:
                return self._error(409, "Original source identity changed; stop review and inspect local files")
            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            self.send_header("Content-Disposition", 'attachment; filename="contract.docx"')
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return self.wfile.write(data)
        if path in ("/", "/index.html", "/app.js", "/styles.css"):
            filename = "index.html" if path == "/" else path[1:]
            content_type = "text/html" if filename.endswith("html") else "text/javascript" if filename.endswith("js") else "text/css"
            data = (self.app.root / "web" / filename).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type + "; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)
        return self._error(404, "Not found")

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            if path == "/api/upload":
                content_type = self.headers.get("Content-Type", "")
                if not content_type.startswith("multipart/form-data;"):
                    raise ValueError("Choose a DOCX file")
                data = self._body()
                message = BytesParser(policy=policy.default).parsebytes(b"MIME-Version: 1.0\r\nContent-Type: " + content_type.encode() + b"\r\n\r\n" + data)
                files = [part for part in message.iter_parts() if part.get_param("name", header="content-disposition") == "file"] if message.is_multipart() else []
                if len(files) != 1:
                    raise ValueError("Choose one DOCX file")
                filename = files[0].get_filename() or "uploaded.docx"
                if not filename.lower().endswith(".docx"):
                    raise ValueError("DOCX only")
                return self._json({"id": self.app.upload(files[0].get_payload(decode=True), filename)}, 201)
            body = json.loads(self._body(100_000))
            if not isinstance(body, dict):
                raise ValueError("Expected a JSON object")
            if path == "/api/decisions":
                document_id = body["document_id"]
                if not isinstance(document_id, str):
                    raise ValueError("Invalid contract ID")
                if document_id not in self.app.contracts:
                    return self._error(404, "Contract not found")
                detail = self.app.detail(document_id)
                valid_ids = {f["id"] for f in detail["analysis"]["findings"]}
                finding_ids = body.get("finding_ids", [])
                if not isinstance(finding_ids, list) or not set(finding_ids).issubset(valid_ids):
                    raise ValueError("Unknown finding reference")
                doc = detail["document"]
                considered_sources = [{"finding_id": finding["id"], "anchor": source["anchor"], "text": source["text"]} for finding in detail["analysis"]["findings"] if finding["id"] in finding_ids for source in finding["sources"]]
                event = self.app.ledger.append(doc["sha256"], doc["filename"], body.get("reviewer", ""), body.get("decision", ""), body.get("rationale", ""), finding_ids, body.get("conditions", ""), considered_sources)
                return self._json(event, 201)
            if path == "/api/precedents":
                if body.get("role") != "demo_legal_reviewer" or body.get("acknowledged") is not True:
                    raise ValueError("Confirm the local demonstration publisher role and responsibility")
                document_id = body["document_id"]
                if not isinstance(document_id, str):
                    raise ValueError("Invalid contract ID")
                if document_id not in self.app.contracts:
                    return self._error(404, "Contract not found")
                event = self.app.publish(document_id, body["decision_id"], body["source_anchor"], body.get("authoriser", ""), body.get("context", ""), body.get("reuse_limits", ""))
                return self._json(event, 201)
            withdrawal = re.fullmatch(r"/api/precedents/([0-9a-f-]+)/withdraw", path)
            if withdrawal:
                if body.get("role") != "demo_legal_reviewer" or body.get("acknowledged") is not True:
                    raise ValueError("Confirm the local demonstration publisher role and responsibility")
                return self._json(self.app.withdraw(withdrawal.group(1), body.get("actor", ""), body.get("reason", "")), 201)
            if path == "/api/ai":
                document_id = body["document_id"]
                if document_id not in self.app.contracts:
                    return self._error(404, "Contract not found")
                detail = self.app.detail(document_id)
                finding = next((f for f in detail["analysis"]["findings"] if f["id"] == body.get("finding_id")), None)
                if not finding:
                    raise ValueError("Choose a source-linked changed clause")
                result = self.app.ai.analyse(detail["document"]["sha256"], finding, detail["reference"])
                self.app.ai_results.setdefault(detail["document"]["sha256"], []).append(result)
                return self._json(result, 201)
        except (ValueError, KeyError, json.JSONDecodeError, AIUnavailable) as exc:
            return self._error(400, str(exc))
        return self._error(404, "Not found")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--state-dir", type=Path, default=Path(".swag-data"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    Handler.app = App(root, args.state_dir.resolve())
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print("Swag synthetic review: http://127.0.0.1:%d" % args.port, flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
