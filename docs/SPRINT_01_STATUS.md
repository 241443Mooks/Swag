# Sprint 01 status — 11 October 2026

## Gate 1 — Input integrity: passed

Checkpoint `0510465` records the [dataset audit](DATASET_AUDIT.md). All 12 DOCX packages opened; each has an ordered body, header and footer. Five historical IDs matched five decision rows. The parser now preserves each source byte sequence, computes SHA-256, exposes original download, and blocks unsupported or unaccounted content. No source fixture or evaluation answer was changed.

## Gate 2 — Engine and safeguards: passed for the synthetic scope

Checkpoint `ecc910f` implements the reference comparison, missing/added clause reporting, independent whole-document indicators, evidence anchors, contextual historical decisions and human-only routes. The final 12 automated tests passed with `python3 -m unittest discover -s tests -v` on Python 3.9.6. The isolated `python3 -m tests.evaluate` reported 6/6 route agreement. T03 broad rights, T04 missing no-licence and T05 schedule override each escalated with source or explicit missing-reference evidence. Mutations checked corrupted DOCX, unknown parts, a table-buried broad right, clause renumbering/removal, purpose change and text after signatures. These synthetic results do not establish performance on real contracts.

## Gate 3 — Optional genuine AI adapter: passed in mocked integration; live unverified

Checkpoint `ecc910f` includes a real OpenAI Responses API adapter for selected changed-clause interpretation, with explicit opt-in, source/reference passage input, structured response format, source-anchor validation, timeout, per-document/session caps and input/output limits. The deterministic review route remains authoritative. Mock tests exercised no configuration, success, fabricated citations, timeout and caps. No live paid call was authorised or made, so provider compatibility, model output quality, cost and latency are **not verified**. The [decision record](decisions/001-scoped-semantic-comparison.md) compares this use against the lexical baseline and records the expected advantage as a hypothesis.

## Gate 4 — Reviewer experience and package: passed for technical delivery; creative acceptance pending

At checkpoint `ecc910f`, the local browser was used to inspect the desktop and 390 px views. The actual UI journey was exercised: queue → T03 exception → anchored full text → H03 context → selected finding → human escalation → refreshed decision history. The original DOCX bytes were verified over HTTP against the SHA-256 identity in the integration test. A synthetic DOCX was also selected through the browser upload control, appeared as a seventh queue item and opened as a routine candidate. The UI's finding checkboxes were exercised; a second append-only event recorded only one selected finding. The test actions used ignored local state, which is excluded from delivery.

The visual concept was an Image Gen mockup. Its two-pane editorial structure, restrained palette, type hierarchy, exception callout and evidence proximity informed the implemented interface. Its invented contract names, approval badges, playbook navigation and fake metadata were deliberately replaced with actual source data and supported actions. At desktop, queue/heading density, source callout, prior context and decision controls were inspected; at 390 px, the horizontal queue, tabs, summary and decision history remained readable. This is engineering visual QA, **not** owner creative acceptance. The human checkpoint in [CREATIVE_REVIEW.md](CREATIVE_REVIEW.md) is pending.

A single ZIP was created from the committed Git tree, passed `unzip -t`, and its fresh extracted copy passed all 12 tests and 6/6 route evaluation. The draft [PR #1](https://github.com/241443Mooks/Swag/pull/1) is open and unmerged. The ZIP remains local for owner review and was not submitted to PortSwigger. The final package checksum is recorded in the PR and handoff.

## Commands and current limits

```sh
python3 -m unittest discover -s tests -v   # 12 passed
python3 -m tests.evaluate                   # 6/6 synthetic routes
node --check web/app.js                     # passed
git diff --check                            # passed
```

Only synthetic mutual NDAs are supported. Unknown DOCX structures fail closed; no OCR, real-contract validation, shared-user permissions or legal accuracy claim exists. The lexical safety indicators can miss unfamiliar language. Live AI and human creative acceptance remain unverified. No measured time saving is claimed.
