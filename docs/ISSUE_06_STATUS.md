# Issue #6 — Upload and persist contract reference standards

## Scope

Implement the first reference-library milestone on the `chug/` application path. Reference originals share the existing `state_dir/references/` persistence area. The verified research catalogue remains the source for bundled research candidates; locally uploaded entries join the same library view and retain their exact source bytes.

Uploads are marked `registered_for_evaluation` and `unapproved`. This feature does not add an approval workflow. An uploaded mutual NDA retains the existing behavior of becoming the selected reference for new NDA uploads; its use is evaluation only and does not imply approval. A customer-order upload is stored separately and does not alter the selected NDA or existing review bindings.

## Recorded metadata

Each uploaded entry records a stable content-derived reference ID, display name (from the original filename), family, extracted applicability facts with unknown or ambiguous values preserved, original filename, SHA-256, version, registration status, approval status, provenance and extraction coverage/limitations. Duplicate source bytes return the existing entry without changing its name, version or status.

The local API exposes a read-only library listing and detail, with an original download that verifies the stored bytes against SHA-256. Upload remains on the private Python backend. The public static demo retains its read-only behavior.

## Verification record

- Base: `8a136ab3b174c02b65f5b225aa81959b052d81ec` (`chug/main`, 2026-10-18).
- Focused reference checks: `python3 -m unittest tests.test_reference_library tests.test_reference_selection -v` — 9 passed.
- Full regression suite: `python3 -m unittest discover -s tests -q` — 63 passed.
- NDA evaluator: `python3 -m tests.evaluate` — 6/6 route agreement (T01–T06).
- Web source and UI regressions: `node --check web/app.js` — passed; `node --test tests/test_web_ui.mjs` — 13 passed.
- `git diff --check` — passed.
- The first sandboxed focused HTTP run could not bind a loopback port; rerunning the focused and full Python suites with loopback permission succeeded. No test depended on a live AI provider.
- Browser screenshot/interaction QA: not verified because Playwright is not installed and there is no repository Playwright workflow. The DOM/UI regression tests passed, including the public static upload-hidden state.
- Human creative acceptance: pending; this implementation does not self-certify the review experience.

## Limitations and decisions

- Family identification and applicability fields use the existing deterministic extraction context. Unknown facts remain unknown; this is not a legal validation of the uploaded wording.
- New customer-order standards are stored and viewable but are not yet bound to incoming order reviews or the review queue. The existing customer-order comparison component remains a separate explicit-confirmation path.
- Uploaded reference version defaults to `1.0`; the filename stem supplies the display name. No approval controls are introduced in this issue.
- PR #3 is still an open draft and currently reports a merge conflict against `main`. It modifies the old `chugchug/server.py` path and includes online security changes to that server. When #3 is rebased to current `chug/`, its server changes will need a manual forward-port and conflict resolution with this reference upload work. This branch does not alter PR #3.
