"""Independent backend tests for the synthetic customer-order comparator."""
from pathlib import Path
import unittest

from chugchug.customer_order_pack import CustomerOrderPack
from chugchug.document import extract_file
from chugchug.reference_registry import load_registry, propose_reference


ROOT = Path(__file__).resolve().parents[1]


class CustomerOrderPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.references = load_registry(ROOT)
        cls.order_references = [item for item in cls.references if item["family"] == "customer_order"]
        cls.pack = CustomerOrderPack()

    def test_registry_contains_five_order_references_and_exact_text_is_not_approval(self):
        self.assertEqual(len(self.order_references), 5)
        for reference in self.order_references:
            report = self.pack.compare(reference, reference["document"])
            self.assertEqual(report["findings"], [])
            self.assertEqual(report["route"], "review_required")
            self.assertTrue(report["human_decision_required"])
            self.assertFalse(report["approved"])
            self.assertEqual(report["baseline"]["sha256"], reference["sha256"])

    def test_customer_order_difference_has_resolvable_source_evidence(self):
        incoming_path = ROOT / "research/reference-library-v0.1/routine-clients/C009 - Inverlea Media Ltd.docx"
        incoming = extract_file(incoming_path)
        proposal = propose_reference(incoming, self.references)
        self.assertIn(proposal["status"], {"proposed", "proposed_with_gaps"})
        selected = next(item for item in self.order_references
                        if item["reference_id"] == proposal["proposal"]["reference_id"])

        report = self.pack.compare(selected, incoming)
        self.assertEqual(report["checks"]["extraction"], "complete")
        self.assertEqual(report["route"], "review_required")
        self.assertTrue(report["findings"])
        incoming_units = {unit["anchor"]: unit["text"] for unit in incoming["units"]}
        reference_units = {unit["anchor"]: unit["text"] for unit in selected["document"]["units"]}
        for finding in report["findings"]:
            for evidence in finding["sources"]:
                self.assertEqual(incoming_units[evidence["anchor"]], evidence["text"])
            for evidence in finding["reference"]:
                self.assertEqual(reference_units[evidence["anchor"]], evidence["text"])

    def test_incomplete_source_and_wrong_family_fail_closed(self):
        reference = self.order_references[0]
        incomplete = {**reference["document"], "coverage": {"status": "blocked"}}
        report = self.pack.compare(reference, incomplete)
        self.assertEqual(report["route"], "blocked_extraction")
        self.assertEqual(report["checks"]["comparison"], "not run")

        nda = next(item for item in self.references if item["family"] == "nda")
        report = self.pack.compare(nda, reference["document"])
        self.assertEqual(report["route"], "blocked_extraction")
        self.assertFalse(report["findings"])

    def test_incoming_family_must_be_explicit_before_comparison(self):
        reference = self.order_references[0]
        nda_path = ROOT / "research/reference-library-v0.1/incoming-tests/Incoming - Evaluation NDA with Longer Retention.docx"
        incoming = extract_file(nda_path)
        report = self.pack.compare(reference, incoming)
        self.assertEqual(report["status"], "needs_context")
        self.assertEqual(report["checks"]["comparison"], "not run")
        self.assertEqual(report["context"]["dimensions"]["family"]["value"], "nda")


if __name__ == "__main__":
    unittest.main()
