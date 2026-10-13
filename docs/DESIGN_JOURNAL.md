# Swig — Design journal

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

## Entry 006 — A decision log is not a learning loop

**Observation:** The local ledger retains new human decisions, but precedent retrieval reads only the fixed historical library. A recorded decision is therefore visible as history without becoming reusable search context or organisational guidance.

**Direction:** Frame the product around governed reuse of reviewed experience. A decision must be assessed for context, conditions and authority before publication as a precedent; playbook guidance needs a separate approval process. Preserve the distinction in the submission narrative and do not describe the current prototype as self-learning.

**Status at `55882e7`:** Product direction recorded in [Product direction](PRODUCT_DIRECTION.md); promotion, playbook governance and improvement from corrections were then unimplemented. Entry 007 records the subsequent synthetic promotion slice.

## Entry 007 — Reuse needs its own event and the same retrieval path

**Observation:** A human decision and permission to show it in later reviews are different acts. Loading every ledger decision into precedent search would give an unreviewed case more authority than its evidence supports.

**Decision:** Keep decision events and explicit publication/withdrawal events distinct, with the publication tied to a considered source passage and contextual limits. Search historical and newly published cases through one lexical ranker; leave review routing independent. The local publisher role is self-attested and visibly labelled as demonstration-only.

**Evidence and limit:** The L01/L02 HTTP lifecycle and browser walkthrough show that publication makes a case retrievable and withdrawal removes it, while L02 still needs human judgement. This proves the interaction and state boundary, not legal applicability, secure authorisation or improved retrieval quality. See [feature evidence](LEARNING_LOOP_STATUS.md).

## Entry 008 — A reference choice must bind the review, not just the current screen

**Observation:** Choosing a different baseline for future uploads is useful, but a global reference switch could silently change an earlier finding or make an earlier human decision look as though it considered a different document.

**Decision:** Bind every uploaded analysis and decision to the exact reference SHA-256 at intake. Persist reference originals separately; reject incomplete or differently structured baselines within this NDA-family slice. Show the chosen reference in each review and allow the bundled sample to be selected again.

**Evidence and limit:** Restart, duplicate binding, tamper and custom-reference comparison tests pass. This is deliberately limited to the existing mutual NDA heading family; it does not perform concept-level alignment of arbitrary legal templates.

## Entry 009 — A correction teaches a question before it teaches an answer

**Observation:** A past correction to archive wording can be relevant to both a similarly restricted archive and a superficially similar commercial-use archive. A simple lexical match cannot establish that the same legal effect or acceptance applies.

**Decision:** Keep comparison corrections separate from contract decisions and non-reusable until an explicit demo publication. Retrieval shows the past source, reviewer explanation, context, limits and an unverified-applicability label beside the current finding. It never edits the deterministic comparison or route.

**Evidence and limit:** L01 → L03 / L02 tests show the authorised lesson appears for both, while both retain `review_required`; withdrawal removes active retrieval. This demonstrates governed organisational memory and the need for a reviewer to inspect the differing context. A genuine semantic improvement remains to be measured, not presumed.

## Entry 010 — The reviewer must be able to challenge an empty finding list

**Observation:** A correction control attached only to an existing finding cannot capture the most concerning feedback: the reviewer sees a provision Swig missed entirely. Leaving the route as routine after that report would misrepresent the known uncertainty.

**Decision:** Offer a collapsed “Something Swig missed?” control on every completely extracted review. Require an exact incoming or reference passage and explanation. Record the challenge as a comparison event with no invented system finding, and lift a routine candidate to human review while the challenge remains in the audit history.

**Evidence:** A synthetic T01 test begins with zero findings and a routine route, records a source-linked missed-provision report, then verifies `review_required` persists after restart. This is a reviewer signal, not a claim that the reported issue is legally material.

## Entry 011 — Show the extension idea without making it the daily workspace

**Observation:** A permanent organisation map would make every Legal reviewer navigate an unbuilt product on each visit. The existing server also kept NDA reference and comparison policy inside the application.

**Decision:** Put one optional Explore page behind a quiet Home link. Keep Legal as its only actionable tile, with other teams described as concepts. Move actual NDA policy and source-path choices behind a small pack boundary while leaving persistence and source identity in the application. Do not add speculative permissions or a pack registry.

**Evidence and limit:** The pack-boundary test and six-route evaluator exercise the existing Legal path. Browser navigation and responsive inspection are recorded in the Issue #10 status. A second pack, organisational isolation and usefulness of the Explore page remain unvalidated; creative acceptance is pending.
## Entry 012 — One name through the local demo (13 October 2026)

**Observation:** The reviewer-facing name and the launch command used different product names, making a simple user-test handoff confusing.

**Decision:** Use ChugChug consistently for the interface, Python package, optional AI settings and default local state path. Keep older dated test records and working GitHub links as historical identifiers. The local rename changes no review policy or safety route; the renamed app passed the existing tests and rendered smoke check. The repository slug still requires a separate GitHub rename.

## Entry 013 — Show the decision and its evidence before the machinery

**Observation:** In the owner's first Home and Falcon walkthrough, useful controls competed for attention. The Home counts did not route work, and the decision action was hard to find. Technical identifiers and multiple tabs appeared before the incoming/reference contrast.

**Decision:** Home now starts with the next action and live, clickable counts for pending work. A contract opens with one concern, its qualified reason, exact incoming wording and applicable reference wording, followed by other material findings and specialist tools. The human decision action is visible immediately. Source identifiers, hashes and original files remain in Document details.

**Discovery:** Falcon's leading whole-document indicator has no direct comparison pair in the engine, but its related no-licence passage exactly matches the selected reference. Showing that exact reference protection beside the added wording makes the relationship legible without inventing a changed clause. When no exact reference passage is available, the UI says so rather than implying a match.

**Evidence and uncertainty:** Browser checks covered filtered queues, Falcon source navigation, a synthetic decision and refresh, desktop and narrow layouts. They verify UI behaviour in a local demonstration, not reviewer understanding or legal interpretation. Owner creative acceptance remains pending under #13; broader families and incoming feeds remain discovery under #16.
