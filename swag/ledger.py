"""Append-only local human decision log."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from uuid import uuid4

DECISIONS = {"approve", "request_amendment", "reject", "escalate"}


class Ledger:
    def __init__(self, path: Path):
        self.path = path
        self.lock = Lock()

    def all(self, sha256=None):
        if not self.path.exists():
            return []
        with self.lock:
            with self.path.open(encoding="utf-8") as handle:
                events = [json.loads(line) for line in handle if line.strip()]
        return [event for event in events if event["sha256"] == sha256] if sha256 else events

    def append(self, sha256, filename, reviewer, decision, rationale, finding_ids):
        if decision not in DECISIONS or not reviewer.strip() or not rationale.strip() or len(reviewer) > 100 or len(rationale) > 2000:
            raise ValueError("Choose a decision and provide reviewer name and rationale")
        if not isinstance(finding_ids, list) or any(not isinstance(item, str) for item in finding_ids):
            raise ValueError("Invalid finding references")
        event = {"id": str(uuid4()), "timestamp": datetime.now(timezone.utc).isoformat(), "sha256": sha256, "filename": filename, "reviewer": reviewer.strip(), "decision": decision, "rationale": rationale.strip(), "finding_ids": finding_ids}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock:
            fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
            try:
                os.write(fd, (json.dumps(event, ensure_ascii=False) + "\n").encode("utf-8"))
                os.fsync(fd)
            finally:
                os.close(fd)
        return event
