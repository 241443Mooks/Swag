# Issue #21 — Reference registry, matching and comparison

## Slice B — Customer-order backend comparison

This slice starts from refreshed `origin/main` at `442f3f7fb3c60c748fb33be7135dc4e4ceb44b96` (PR #23 merge). The earlier registry and candidate-matching work is already on that base. This change adds a backend-only `CustomerOrderPack`; no UI, upload routing, review ledger, policy status, or deployment path is changed.

- The comparator accepts a specific registry record and extracted incoming document. It refuses a non-order reference, mismatched source identity or incomplete extraction.
- It accounts for preamble text, numbered sections, named schedules/appendices, and extracted non-body parts. It reports changed, added, missing and reordered sections with exact incoming/reference anchors.
- It requires complete extraction and unambiguous customer-order family evidence before comparison; missing, conflicting or wrong-family context returns `needs_context` and does not compare sections.
- Exact text against a research-only unapproved reference still routes to `review_required`. Differences are not assigned legal effect; amounts, dates, quantities and service terms remain plain text requiring a person to interpret.
- Repeated section headings now stop section alignment and return only a source-linked structural-ambiguity finding. This avoids emitting potentially misleading added/changed section findings from a non-unique heading map.
- This does not solve baseline applicability, confirm a candidate, or integrate orders into the reviewer UI. Those boundaries remain explicit until the owner has reviewed the current experience.

### Slice B test evidence

- `python3 -m unittest tests.test_customer_order_pack -v`: 5 passed, including repeated-heading abstention.
- Tests verify all five registry order references remain unapproved, exact research-source comparison cannot become approval, an existing synthetic incoming order yields source-resolvable evidence, and incomplete/wrong-family inputs block.
- `python3 -m unittest discover -s tests -q`: 46 passed.
- `python3 -m tests.evaluate`: original NDA routes agreed 6/6; T03/T04/T05 escalated.
- `python3 -m tests.adversarial_audit`: 11/11 critical cases surfaced or safely blocked, zero false routine routes, 14/16 expected route matches. A05 and A08 remain conservative escalations above their written route targets.
- `node --check web/app.js`, `node --test tests/test_web_ui.mjs` (4 passed), and `git diff --check`: passed.
- Live AI calls: none. No UI or deployment check is claimed for this backend-only slice.

## Slice A — Reference registry and candidate matching (historical)

## Slice A scope

The earlier slice started from `origin/main` at `c4f77b90cc61154d202d26448c0c6211c17db9a8` and implemented a verified research-reference registry, deterministic context extraction and evidence-backed candidate proposals with abstention.

- Eight DOCX sources are registered by stable ID, title, family, variant, channel/deployment, direction, jurisdiction, source-linked scope, version, SHA-256 and explicit unapproved-demo status.
- The loader verifies source paths, document coverage, source hashes and scope anchors. It reads only the catalogue and files under `references/`.
- Matching extracts family and contextual facts from source passages, hard-excludes known conflicts before ranking, asks for missing required context, and abstains on conflicting or unsupported context. Customer-order product variants are derived only from the observed deployment and sales channel. Candidate reasons link back to exact incoming anchors; source scope is linked to the matching reference anchor. Remaining candidates are ranked by shared scope terms, with ties left unresolved.
- A candidate is a proposal only. Human confirmation is required, `comparison_allowed` remains false, and no reference is described as approved policy.
- Customer-order source documents do not specify jurisdiction. Order proposals therefore expose this gap and require human scope validation. NDA proposals require explicit England and Wales context when considering the jurisdiction-limited references.
- Expected labels previously embedded in `catalog.json` have been moved intact to `evaluation-only/expected-matches.json`. Runtime rejects embedded expected-label fields and never reads the evaluation-only directory. Incoming research fixtures remain excluded from matching.

This slice does not integrate matching into the review UI, compare customer orders, validate legal applicability, create blind evaluation data, or claim matching accuracy. Those require later #21 slices and independent acceptance.

## Evidence

- Branch base checked after `git fetch origin --prune`: `c4f77b90cc61154d202d26448c0c6211c17db9a8`.
- `python3 -m unittest discover -s tests -q`: 41 tests passed.
- `python3 -m tests.evaluate`: original NDA routes agreed 6/6; T03/T04/T05 escalated.
- `python3 -m tests.adversarial_audit`: all 11/11 critical exceptions surfaced, 0 false routine routes, 14/16 expected route matches. A05 and A08 remain conservative escalations relative to their `review_required` targets.
- `node --check web/app.js`: passed; `node --test tests/test_web_ui.mjs`: 3 passed.
- `git diff --check`: passed; 8 reference records and source hashes verified.
- Live AI calls: none. Browser review: not applicable to this non-UI slice. Human creative acceptance: not applicable/not claimed.
