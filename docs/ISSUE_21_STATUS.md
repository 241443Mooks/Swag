# Issue #21 — Reference registry and candidate matching

## Slice A scope

This branch starts from `origin/main` at `c4f77b90cc61154d202d26448c0c6211c17db9a8` and implements only the first bounded slice: a verified research-reference registry, deterministic context extraction and evidence-backed candidate proposals with abstention.

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
