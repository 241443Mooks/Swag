"""Loopback-only web app for synthetic NDA review."""
from __future__ import annotations

import argparse
import json
import re
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

from .ai import AIService, AIUnavailable
from .document import extract
from .engine import analyse, load_library, ROUTE_ORDER
from .ledger import Ledger


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
            for meta_path in uploads.glob("*.json"):
                try:
                    meta = json.loads(meta_path.read_text())
                    path = uploads / (meta["sha256"] + ".docx")
                    if path.is_file():
                        self.contracts[meta["id"]] = {"document": extract(path.read_bytes(), meta["filename"]), "path": path}
                except (OSError, ValueError, KeyError):
                    pass
        self.ledger = Ledger(state_dir / "decisions.jsonl")
        self.ai = AIService()
        self.ai_results = {}

    def analysis(self, document_id):
        return analyse(self.reference, self.contracts[document_id]["document"], self.historical, self.decisions)

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
        return {"id": document_id, "display_name": self.display_name(document), "document": document, "reference": self.reference, "analysis": self.analysis(document_id), "history": self.ledger.all(document["sha256"]), "ai": self.ai.status(), "ai_results": self.ai_results.get(document["sha256"], [])}

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
            with file_path.open("xb") as handle:
                handle.write(data)
            (target / (document["sha256"] + ".json")).write_text(json.dumps({"id": document_id, "sha256": document["sha256"], "filename": document["filename"]}))
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
            return self._json({"items": self.app.queue()})
        if path.startswith("/api/contracts/"):
            parts = path.split("/")
            if len(parts) not in (4, 5) or parts[3] not in self.app.contracts:
                return self._error(404, "Contract not found")
            document_id = parts[3]
            if len(parts) == 4:
                return self._json(self.app.detail(document_id))
            if parts[4] != "original":
                return self._error(404, "Not found")
            data = self.app.contracts[document_id]["path"].read_bytes()
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
            if path == "/api/decisions":
                document_id = body["document_id"]
                if document_id not in self.app.contracts:
                    return self._error(404, "Contract not found")
                detail = self.app.detail(document_id)
                valid_ids = {f["id"] for f in detail["analysis"]["findings"]}
                finding_ids = body.get("finding_ids", [])
                if not isinstance(finding_ids, list) or not set(finding_ids).issubset(valid_ids):
                    raise ValueError("Unknown finding reference")
                doc = detail["document"]
                event = self.app.ledger.append(doc["sha256"], doc["filename"], body.get("reviewer", ""), body.get("decision", ""), body.get("rationale", ""), finding_ids)
                return self._json(event, 201)
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
