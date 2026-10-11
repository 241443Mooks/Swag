# Swag — Design journal

Record meaningful discoveries, decisions and surprises as the product is built. Separate observations from hypotheses; do not fabricate user research, performance or results.

## Entry 001 — Starting design conviction
**Observation:** A small legal team repeatedly reviews mostly standard contracts, while changes and precedents recur and peak periods create queues.

**Hypothesis:** The largest benefit may come from reorganising review around exceptions and prior context, rather than automating full-document reading or adding AI to every step.

**Design direction:** Simple on the surface; exceptionally robust underneath. Deterministic extraction, coverage, comparison and workflow; real AI only where a conventional baseline is insufficient; human legal judgement preserved.

**What to validate:** Can a reviewer rapidly identify what needs attention, inspect its evidence and act without rereading everything? Are shortcut conditions sufficiently reliable and transparent? Which semantic task actually benefits from AI?

**Status:** Hypothesis — not validated with legal-team users.

## Entry 002 — Unsectioned text is a route blocker

**Observation:** An adversarial test placed text after the signature block. The parser extracted it, but the first comparison omitted it and offered a routine route.

**Decision:** Inventory every non-administrative body paragraph, including text outside numbered sections, as a difference. Treat signatures and metadata as administrative only when they match a constrained structure. Similarly, normalise only the party names in clause 1, while comparing the purpose wording. This preserves the simple reviewer surface without concealing unclassified content.

**Evidence:** Adversarial regression tests now require review for trailing instructions and changed purpose wording. This is a limited NDA-family rule, not a claim of general legal-document coverage.

## Entry 003 — The queue needs counterparties, not fixture filenames

**Observation:** Raw fixture slugs made the first browser view feel like a test harness rather than a legal team's queue.

**Decision:** Display the counterparty extracted from the parties clause, retaining the filename and hash in the document view. This reduces scanning effort without changing source identity or routing.

**Status:** Browser checked at desktop and 390 px. Human creative acceptance remains pending.
