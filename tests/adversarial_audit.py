"""Independent, reproducible challenge-set scoring; never imported by runtime."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from swag.document import extract_file
from swag.engine import analyse, load_library

ROOT = Path(__file__).resolve().parents[1]
ORDER = {"routine_candidate": 0, "review_required": 1, "escalate": 2, "blocked_extraction": 3}


def audit():
    reference, historical, _, decisions = load_library(ROOT)
    manifest = json.loads((ROOT / "dataset/adversarial/manifest.json").read_text())
    rows = []
    for case in manifest:
        document = extract_file(ROOT / "dataset/adversarial" / case["file"])
        result = analyse(reference, document, historical, decisions)
        actual = {unit["anchor"] for unit in document["units"]}
        baseline = {unit["anchor"] for unit in reference["units"]}
        valid_evidence = all(
            all(unit["anchor"] in actual for unit in finding["sources"] + finding["related"])
            and (finding["reference"] is None or finding["reference"]["anchor"] in baseline)
            for finding in result["findings"]
        )
        surfaced = result["route"] != "routine_candidate" and (
            bool(result["findings"]) or bool(document["coverage"]["issues"])
        ) and valid_evidence
        rows.append({
            **case,
            "observed_route": result["route"],
            "finding_categories": [finding["category"] for finding in result["findings"]],
            "source_anchors": [unit["anchor"] for finding in result["findings"] for unit in finding["sources"]],
            "coverage_issues": document["coverage"]["issues"],
            "exception_surfaced": surfaced,
            "valid_evidence": valid_evidence,
            "unsafe_routine": case["critical_exception"] and result["route"] == "routine_candidate",
            "unnecessary_escalation": not case["critical_exception"] and ORDER[result["route"]] > ORDER[case["expected_route"]],
            "meets_expected_route": result["route"] == case["expected_route"],
        })
    critical = [row for row in rows if row["critical_exception"]]
    noncritical = [row for row in rows if not row["critical_exception"]]
    return {
        "scope": "Small, authored synthetic challenge set; not real-world legal accuracy.",
        "metrics": {
            "critical_exception_recall": {"surfaced": sum(row["exception_surfaced"] for row in critical), "total": len(critical)},
            "false_routine_recommendations": {"count": sum(row["unsafe_routine"] for row in critical), "critical_cases": len(critical)},
            "unnecessary_escalations": {"count": sum(row["unnecessary_escalation"] for row in noncritical), "noncritical_cases": len(noncritical)},
            "expected_route_matches": {"count": sum(row["meets_expected_route"] for row in rows), "total": len(rows)},
        },
        "cases": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = audit()
    encoded = json.dumps(report, indent=2) + "\n"
    if args.out:
        args.out.write_text(encoded)
    print(json.dumps(report["metrics"], indent=2))
    for row in report["cases"]:
        print(row["id"], row["observed_route"], row["expected_route"], "SURFACED" if row["exception_surfaced"] else "MISSED", ",".join(row["finding_categories"]))


if __name__ == "__main__":
    main()
