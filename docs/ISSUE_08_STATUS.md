# Issue #8 — reviewer journey status (11 October 2026)

Base: draft PR #4, `feature/swig-product-alignment` at `21f7a0a`. Work branch: `feature/issue-8-reviewer-journey`. All material is fictional. Owner creative acceptance, legal validation and release approval are pending.

| Priority | Implemented and verified | Still open |
| --- | --- | --- |
| P0 reviewer UX | Home / Queue / Reference / Help; calm exception-first review, collapsed findings and checks, source and reference navigation, review history drawer. Desktop home and Falcon review visually inspected in the local browser. | Owner creative review and complete interactive browser QA; browser automation stopped delivering clicks after its file chooser stalled. Native interaction was demonstrated earlier in the session, but the final UI has not received a full click-through. |
| P1 chosen reference | Local synthetic DOCX reference upload, hash-bound persisted original, explicit selection, restart and tamper checks, per-analysis and per-decision reference identity. Existing six documents stay on the bundled baseline. | This slice supports the bundled mutual NDA heading family only. A differently structured NDA is rejected with an explicit explanation; cross-family alignment remains unimplemented. |
| P2 history | Five actual historical decisions searched for the bundled reference; bounded result list (at most three), exact/similar/same-topic lexical labels, decision and reuse limits, outcome filter, complete extracted original and downloadable hashed DOCX. Counts are derived from the five records plus active published precedents. | No invented “300 accepted / 9 rejected” corpus. Whole-contract historical decisions are not clause approvals. Retrieval precision and legal relevance remain unmeasured. |
| P3 comparison feedback | Append-only correction ledger distinct from contract decisions, exact document and reference identities, cited passages, reviewer explanation, explicit self-attested demo publication, lexical retrieval, and withdrawal. A reviewer can also report a missed provision when no finding exists; that report blocks a routine route for that document. L01 → L03 and L02 synthetic lifecycle verified through restart and HTTP routes. | No supersession action, production roles, tenant boundaries or semantic candidate aligner. A retrieved lesson is shown as prior context with applicability unverified; it does not revise Swig's original comparison or route. |
| P4 AI experiment | Existing optional, capped adapter remains disabled by default. No live API call or paid cost. | A model-informed A/B/C comparison and measured benefit over the lexical baseline are **not verified**. Adding it without live evaluation would overstate the learning claim, so it is deferred. |

## Evidence at this branch

- `python3 -m unittest discover -s tests -q`: 30 tests passed, including chosen reference, historical HTTP source, correction publication and withdrawal, and a missed-provision challenge to a routine candidate.
- `python3 -m tests.evaluate`: original routes 6/6; T03/T04/T05 still escalate.
- `python3 -m tests.adversarial_audit`: 11/11 critical exceptions surfaced or safely blocked; 0/11 false routine; 14/16 expected route matches, with two unnecessary escalations among nine review/routine targets.
- `node --check web/app.js` and `git diff --check`: passed.
- HTTP tested reference upload, incoming upload, exact historical source, correction record → publish → retrieve → withdraw; persistence checked after restart.
- Browser visual inspection: Home and Falcon T03 desktop at 1280 px. The view was coherent and exception-first. Final browser clicks were not confirmed because the browser session's earlier file chooser stalled and subsequent click commands produced no state change; this is a QA limitation, not a claimed application failure. No narrow-screen visual inspection was completed at this point.

These are synthetic technical checks, not evidence of real-world legal accuracy or reviewer productivity. The original six scenarios and the evaluation answer key were not altered. L03 is a new fictional fixture derived from L01 by changing only the archive wording; it is not in the runtime's historical library and its expected relationship is recorded in the correction test, not used as an application rule.

## Architecture and trade-offs

The chosen reference is bound when a document enters the queue, so changing the selected reference cannot silently reinterpret prior decisions. A source may intentionally be analysed under two references as two review entries; the same original bytes are stored once. The custom reference must pass extraction and required-heading validation. This is a deliberate constrained slice while concept-level matching is unevaluated.

Historical decisions and comparison corrections have different ledgers and publication rules. A correction can be saved without a contract decision. A publication can be withdrawn without erasing its origin. Lexical lesson retrieval supplies an inspectable hypothesis, never an equivalence conclusion. Both the underlying comparison and independent safeguards still run unchanged. This protects against a misleading L02-style transfer while leaving a human to decide how relevant the past correction is.

For PDF/OCR or another NDA family, replace the DOCX-specific extraction adapter and source anchor scheme with a format-independent passage model that retains original bytes, coordinates, coverage and extraction uncertainty. The current `word/document.xml` anchors and heading alignment cannot simply be reused for page-based or image content. That is future architecture work, not a hidden capability of this slice.

## Highest-value next work

1. Owner walks through Home → T03 source evidence → T02 history → L01 correction → L03/L02 reuse, recording where wording or navigation causes hesitation.
2. Establish an independent, legally reviewed A/B/C evaluation set and test whether semantic candidate assistance improves alignment without new false reassurance. Keep the deterministic route floor.
3. Before real documents or shared use: authentication and publisher authority, tenant isolation, privacy/security and retention design, recovery for damaged append-only logs, and legal subject-matter review.
