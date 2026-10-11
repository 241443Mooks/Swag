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

## Entry 004 — Extraction coverage did not imply review coverage

**Observation:** The first adversarial run offered a routine route when a consequential provision was added in a header or footer. Both parts had been extracted, but neither comparison nor the independent indicator scan examined them. Hidden or struck protection and duplicate ZIP parts produced similarly unjustified routine routes.

**Decision:** Treat extraction, comparison and independent safeguards as separate evidence-bearing checks. Compare all extracted non-body parts, scan all passages, block ambiguous or visibility-altered content, and show each check's status in a short Assurance view. A human still makes the legal decision.

**Evidence and trade-off:** The fixed synthetic challenge set moved from six false routine recommendations to zero. Two critical grants now escalate above the prewritten review target, and general DOCX visual fidelity is still unverified. The [audit](MISSED_EXCEPTION_AUDIT.md) preserves both the original misses and current limitations.

## Entry 005 — A blocked route needs blocked-state language everywhere

**Observation:** Browser QA of a hidden-text challenge showed “Analysis blocked” in the route, while the overview fallback still said no material wording change was found. That mixed message could invite a shortcut despite incomplete checks.

**Decision:** The blocked overview now says extraction is incomplete, comparison and safeguards were not run, and no clause conclusion is available. The Assurance tab repeats the specific extraction issue and leaves potential indicators “not assessed”.

**Evidence:** Reloaded browser view of uploaded A03 showed the corrected notice, blocked extraction, `not run` comparison/indicators and the `vanish` source location. Human legal review remains necessary.
