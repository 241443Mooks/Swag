# Swig product alignment and local review

**11 October 2026 · branch `feature/swig-product-alignment` · stacked on draft PR #3.** This consolidation changes product wording and review guidance, not the contract analysis architecture or six original scenarios.

## Decisions

- The reviewer-facing name is **Swig** in the page title, brand, server startup line, documentation and HTTP journey assertion. The existing GitHub repository URL, Python `swag` package, `SWAG_AI_*` variables and `.swag-data/` directory remain technical identifiers to preserve working commands and local state.
- One north star now connects the reviewer journey, assurance and governed reuse. The creative intent no longer describes publication as unimplemented. Demonstrated synthetic behaviour, validation needed for real use and optional future investments are labelled separately.
- The optional OpenAI adapter remains a narrow changed-clause explanation. Offline review and routing do not depend on it. A live call, model benefit and legal usefulness remain unverified; the employer brief asks how AI could help, without specifying a live paid call.
- The feature set is frozen for creative acceptance. The owner should judge the running journey before the final submission ZIP is prepared. Publication authority, playbooks, additional formats and production deployment are outside this consolidation.

## Verification on this branch

| Check | Observed result |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | 23 passed, including HTTP brand, queue, decision/reload and upload journey |
| `python3 -m tests.evaluate` | Original six routes 6/6; T03/T04/T05 escalated |
| `python3 -m tests.adversarial_audit` | 11/11 critical exceptions surfaced or safely blocked; 0/11 false routine; 14/16 exact routes; 2/9 unnecessary escalations against prewritten route targets |
| `node --check web/app.js` and `git diff --check` | Passed |
| Local HTTP and rendered browser | `http://127.0.0.1:8771/` returned the Swig page and six queue items. Browser showed T03 evidence and precedent, T03 assurance, and T01 routine candidate with human decision still required. |

The local server uses ignored `.swag-data/swig-review/` so the owner's existing demo state is untouched. This process is an active review convenience, not a deployed service; restart from the repository root with `python3 -m swag.server --port 8771 --state-dir .swag-data/swig-review` if the session ends.

## Still open

Human creative acceptance, qualified legal review, realistic usability and retrieval evaluation, live AI quality and final clean-package QA are **not verified**. No new submission ZIP has been made. The tests use synthetic contracts and do not establish real-world legal accuracy or measured time savings.
