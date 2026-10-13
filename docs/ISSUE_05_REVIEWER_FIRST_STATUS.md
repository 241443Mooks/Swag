# Issue #5 — Reviewer-first iteration

**Status:** Implemented for owner walkthrough; creative acceptance is pending. This iteration begins at PR #11 head `e6c9016e9078f664179b4fe6a284a7da5c5d230c`. It changes presentation and navigation, not review policy or detection.

## Journey change

Previously, Home showed passive counts and a prominent Explore invitation. Falcon opened with tabs, provenance and a long overview before the human decision was discoverable.

Now Home states the task plainly, offers **Start reviewing**, and routes each live pending count to its own filtered queue. Falcon leads with one qualified concern, why it may matter, the exact added wording beside the applicable reference protection, and **Record decision**. Other findings remain visible as a list; source anchors, full text, check coverage, prior decisions, correction tools and original files remain available.

The filtered queue is retained through a review and same-tab refresh. A recorded decision removes that contract from pending category counts, while **All contracts** still shows its history. Decisions remain append-only, source-linked and human-made.

## Owner observations addressed

- The 13 October Home counts now open filtered work rather than acting as decoration.
- Technical filenames, fixture IDs and hashes have moved to Document details.
- Falcon's first comparison and the next human action are visible before specialist detail.
- Explore is linked from Help rather than Home.
- General Home copy describes contract review; a discreet label states that the current data are synthetic mutual NDAs.

## Verification

Verification on the candidate tree (Python 3.9, Node available locally):

- `python3 -m unittest discover -s tests -q`: **31 passed**.
- `python3 -m tests.evaluate`: **6/6** original scenario routes, including T03/T04/T05 escalation.
- `python3 -m tests.adversarial_audit`: **16 exercised**; 11/11 critical exceptions surfaced or safely blocked, zero false routine recommendations, 14/16 exact route matches. The two mismatches are conservative escalations already documented in the adversarial audit.
- `node --check web/app.js`: passed. `node --test tests/test_web_ui.mjs`: **3 passed**. `git diff --check`: passed.

Repeat the commands on the final PR head:

```sh
python3 -m unittest discover -s tests -q
python3 -m tests.evaluate
python3 -m tests.adversarial_audit
node --check web/app.js
node --test tests/test_web_ui.mjs
git diff --check
```

Browser walkthrough used a separate `--state-dir` under `/tmp`. The 1440 × 900 and 390 × 844 views showed readable Home and Falcon screens; the narrow view had no horizontal overflow. All three category filters selected the expected queue items. Falcon's exact incoming source link opened and highlighted the original passage; the reference wording, other findings, historical case, correction control and check coverage remained accessible. A synthetic escalation decision was recorded with rationale and a considered finding, survived refresh, reduced the pending count, and returned to the same queue category. The Home keyboard path reached the first category with a visible 3 px focus outline. Browser console warnings/errors: none. This is local synthetic UX proof, not owner acceptance.

## Boundaries

- The reference picker supports only structurally compatible synthetic mutual NDAs. It selects the baseline for **new** uploads; existing reviews keep their intake reference. Additional families and automated intake belong to #16.
- Historical decisions remain contextual evidence, not policy. Optional AI remains off; no provider call is part of this iteration.
- This interface uses **ChugChug**. Some older issue and repository documentation says **Swig**; the owner should confirm the final name under #13 before packaging.
- Do not merge, package a submission ZIP, or mark creative acceptance complete before the owner's new first-hand walkthrough.
