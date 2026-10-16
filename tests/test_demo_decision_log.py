"""Boundaries for the intentionally fictional, read-only decision history."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "dataset" / "review_records" / "demo_decision_log.json"
PUBLIC = ROOT / "web" / "demo-data" / "decision-log.json"
REVIEWS = {f"T{i:02d}" for i in range(1, 7)}
EXAMPLES = {f"H{i:02d}" for i in range(1, 6)}


class DemoDecisionLogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.public = json.loads(PUBLIC.read_text(encoding="utf-8"))
        cls.records = cls.source["records"]

    def test_fixed_snapshot_matches_explicitly_synthetic_source(self):
        self.assertEqual(self.source, self.public)
        self.assertTrue(self.source["synthetic"])
        self.assertEqual(self.source["schema_version"], 1)
        self.assertEqual(len(self.records), 300)

    def test_all_ids_and_review_links_are_valid(self):
        self.assertEqual(len({r["id"] for r in self.records}), 300)
        self.assertTrue(all(r["synthetic"] is True for r in self.records))
        self.assertTrue(all(r["record_status"] == "illustrative_unverified" for r in self.records))
        self.assertTrue(all(r["review_id"] in REVIEWS for r in self.records))
        self.assertTrue(all(r["related_fixed_example_id"] in EXAMPLES | {None} for r in self.records))
        self.assertTrue(all("not" in r["reuse_authority"].lower() for r in self.records))
        self.assertEqual({r["flag"] for r in self.records}, {"green", "red", "amber"})
        self.assertEqual({r["decision"] for r in self.records},
                         {"approve", "request_amendment", "reject", "escalate"})
        for review in REVIEWS:
            self.assertTrue(list((ROOT / "dataset" / "incoming").glob(f"{review}-*.docx")))

    def test_multiple_comparison_examples_in_existing_scenarios(self):
        for review in REVIEWS:
            with self.subTest(review=review):
                rows = [r for r in self.records if r["review_id"] == review]
                self.assertGreaterEqual(len(rows), 40)
                self.assertGreaterEqual(len({r["issue"] for r in rows}), 2)
        self.assertTrue(any(r["review_id"] == "T03" and r["comparison_type"] == "same_red_flag" for r in self.records))
        self.assertTrue(any(r["review_id"] == "T03" and r["comparison_type"] == "resolved_after_amendment" for r in self.records))
        self.assertTrue(any(r["review_id"] == "T01" and r["comparison_type"] == "same_green_pattern" for r in self.records))
        self.assertGreater(sum(r["related_fixed_example_id"] is not None for r in self.records), 40)

    def test_no_pseudo_source_evidence_or_automatic_promotion(self):
        forbidden = {"sha256", "source_anchor", "source_text", "publication_id", "authority_mode"}
        self.assertTrue(all(not forbidden.intersection(r) for r in self.records))
        self.assertTrue(all(r["rationale"] and r["conditions"] and r["issue"] for r in self.records))


if __name__ == "__main__":
    unittest.main()
