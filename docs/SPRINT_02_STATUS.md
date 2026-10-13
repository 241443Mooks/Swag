# Sprint 02 — missed-exception and assurance audit

## Scope and checkpoints

The baseline is draft PR #1 at `2ea24ae`. This branch is stacked on that commit so the PR isolates audit work; it does not change `main`, the original 12 source DOCX files, the evaluation answer key, or the six original scenario expectations. The fixed adversarial challenge set was committed before engine changes. The exact baseline was rerun from a detached checkout of `2ea24ae` against the final 16 fixtures, then the same harness was run against this branch. See [the audit](MISSED_EXCEPTION_AUDIT.md) and the two JSON observations.

## Gate evidence

| Gate | Status and evidence |
|---|---|
| Input integrity | **Passed for the supported synthetic DOCX scope.** Original 12 inputs still extract; 16 separate adversarial DOCX files challenge hidden/struck text, duplicate parts, header/footer changes and other changes. Unknown content continues to block. General Word rendering fidelity is **not verified**. |
| Engine and safeguards | **Passed for the original six and fixed challenge set.** `python3 -m tests.evaluate`: 6/6 route agreement. `python3 -m tests.adversarial_audit`: 11/11 critical challenges surfaced or safely blocked, 0 false routine, 2 routes above the written target. This does not measure legal accuracy. |
| AI | **Unchanged; live not verified.** The existing real-provider adapter was not called. No paid API use or mocked result is presented as live. |
| Experience | **Technical QA passed for the exercised journey; human creative acceptance pending.** Queue → T03 finding → anchored full text → decision → reload → assurance/human status was exercised in the local browser on `127.0.0.1:8772`. An A03 fixture was uploaded over the local HTTP API and the rendered queue/overview/assurance correctly showed blocked extraction and unrun checks. The first blocked overview falsely said no material difference was found; this was repaired and rechecked in the browser. Desktop assurance rendered with no console warning/error. A 390 px viewport had bounded DOM layout; browser screenshot scaling limited visual confidence at that size. The browser file chooser did not complete during this sprint, but the HTTP upload journey and restart are covered by automated integration tests. |
| Persistence and partial failures | **Focused tests passed.** Upload interruption/metadata mismatch causes a visible startup failure; changed source bytes block routing. The append-only human event survived app reload. Manual repair of interrupted state remains an operational limitation. |

## Commands and results

Environment: macOS, Python 3.9.6, standard-library runtime. The full suite's loopback test required execution outside the command sandbox because local socket binding was denied there.

```sh
python3 scripts/build_adversarial_fixtures.py         # passed; deterministic outputs
git worktree add --detach /tmp/swag-pr1-baseline 2ea24ae  # temporary original implementation
PYTHONPATH=/tmp/swag-pr1-baseline python3 tests/adversarial_audit.py --out docs/ADVERSARIAL_BASELINE.json
git worktree remove /tmp/swag-pr1-baseline
python3 -m tests.adversarial_audit --out docs/ADVERSARIAL_AFTER.json
python3 -m unittest discover -s tests -v             # 19 passed
python3 -m tests.evaluate                             # 6/6 original routes
node --check web/app.js                               # passed
git diff --check                                      # passed
```

The detached baseline checkout was used only for observation; it was not modified. The fixtures and scripts are committed for reproduction. The baseline and current JSON retain per-case observed route, finding categories, source anchors, extraction issues, evidence validity and unsafe-route flags.

## Review state

This work is ready for owner review and QA, **not** declared ready for PortSwigger submission. The UI remains a synthetic local demonstration. Legal reviewer validation, real-contract accuracy, live AI behaviour, privacy review, and human creative acceptance are outstanding. No new ZIP was made: the original submission package predates these audit changes and should not be mistaken for the audited branch.
