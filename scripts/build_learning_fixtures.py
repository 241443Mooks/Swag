"""Rebuild the two synthetic DOCX files for the governed-reuse journey."""
from __future__ import annotations

from pathlib import Path

from scripts.build_adversarial_fixtures import edit_document, replace_all, replace_text

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dataset/incoming/T01-template-match.docx"
DEST = ROOT / "dataset/learning"
ORIGINAL = "On written request, a receiving party shall return or destroy Confidential Information, except for one archival copy retained for legal compliance and routine backups subject to continuing confidentiality."

CASES = {
    "L01-audit-retention.docx": (
        "Maple Metrics Ltd",
        "L01",
        "On written request, a receiving party shall return or destroy Confidential Information, except for one encrypted archive kept for seven years solely to satisfy a named regulatory retention duty, inaccessible for business use and subject to continuing confidentiality.",
    ),
    "L02-analytics-retention.docx": (
        "Harbour Analytics Ltd",
        "L02",
        "On written request, a receiving party shall return or destroy Confidential Information, except for one encrypted archive kept for seven years to support product analytics, accessible to the recipient's commercial team and subject to continuing confidentiality.",
    ),
}


def build():
    source = SOURCE.read_bytes()
    DEST.mkdir(parents=True, exist_ok=True)
    for filename, (counterparty, document_id, amendment) in CASES.items():
        def change(xml):
            replace_all(xml, "Birchbridge Ltd", counterparty)
            replace_text(xml, "Document ID: T01", "Document ID: " + document_id)
            replace_text(xml, ORIGINAL, amendment)
        (DEST / filename).write_bytes(edit_document(source, change))


if __name__ == "__main__":
    build()
