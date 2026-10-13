# Governed precedent reuse — feature evidence

**Branch:** `feature/governed-precedent-learning-loop`, stacked on draft PR #2 at `55882e7`. **Scope:** one local synthetic decision → publication → later retrieval → withdrawal journey. No real legal publishing authority is implied.

## Implementation

- Decision events now optionally record conditions beside rationale and snapshot the source passages for findings the reviewer marked as considered. Publication validation uses that stable event evidence, rather than depending on a future run of the finding algorithm.
- A separate append-only knowledge event log records explicit publication and withdrawal. Publication requires a decision for the exact document, a source passage from a finding marked as considered, complete extraction, matching original bytes, commercial context, reuse limits and a named self-attested demonstration publisher. Startup validates active source and decision links. Broken publication history or source identity blocks retrieval rather than showing an apparently complete result.
- Historical and newly published records enter one lexical ranking path. A published record carries its source, past decision, rationale, conditions, context, reuse limits and publisher to the reviewer. Retrieval never changes comparison, safeguards, route or human decision.
- Decision history exposes publication and withdrawal progressively. A retrieved demo precedent links back to the full source passage. Withdrawn records remain in the event history but leave active search.

## Verification

| Check | Result | Evidence |
| --- | --- | --- |
| New HTTP lifecycle test | Passed | L01/L02 upload → conditional decision → unpublished stays out → explicit publication → L02 retrieves with conditions and remains `review_required` → L02 receives its own decision → restart → withdrawal → active retrieval stops, history persists → second restart. |
| Negative boundaries | Passed | Unacknowledged publisher rejected; unconsidered source rejected; source tampering or a relink to unconsidered wording rejected; broken publication log stops startup; duplicate publication and withdrawal rejected. |
| Full unit and HTTP suite | Passed | `python3 -m unittest discover -s tests -q`: 23 tests. |
| Original six scenarios | Passed | `python3 -m tests.evaluate`: 6/6 route agreement. |
| Adversarial audit | Passed within existing targets | `python3 -m tests.adversarial_audit`: 11/11 critical cases surfaced or safely blocked, 0/11 false routine recommendations, 14/16 exact expected routes; two critical cases still escalate above their prewritten review target. |
| Frontend syntax | Passed | `node --check web/app.js`. |
| Rendered browser journey | Passed at 887 × 787 | Local in-app browser: both DOCX uploads, L01 conditional decision, publication, L02 unchanged route and visible source/context/conditions, source navigation, withdrawal, L02 active-result removal. Console had no error or warning entries. |

The browser run used a temporary state directory and synthetic data. The Browser plugin and a local Playwright installation were unavailable; the Codex computer-use browser supplied the interaction and accessibility evidence. A mobile-size browser check and live AI call were not performed in this feature QA.

## Residual limits and release boundary

- Publisher names and the `demo_legal_reviewer` role are self-attested. There is no authentication, role management, separation of duties or production-grade authorisation. Anyone with access to the local demo can publish or withdraw. This must change before real contracts or an organisational precedent library.
- The publication form captures context and limits as free text. No legal reviewer has evaluated their completeness. Version 1 and withdrawal are recorded; replacement guidance, conflicts, expiry and approval policy remain undefined.
- Retrieval is lexical, limited to the changed findings and three displayed results. The L01/L02 test proves this pair is surfaced with conditions and that routes do not change; it does not measure relevance or legal usefulness across a representative corpus.
- Storage is local JSONL in one process. There is no shared multi-user transaction model, backup/recovery interface or tamper-proof audit log. Malformed event history stops the local app; manual recovery is not implemented.
- Decisions recorded before source snapshots existed remain visible in history but cannot be published through this new path. The reviewer can make a fresh decision after checking the source; no silent migration invents what they considered.
- The earlier DOCX extraction limits, lack of real-contract validation and optional AI's unverified live behaviour remain. Human creative acceptance and submission QA are pending.

## Review

Run the [learning-cycle walkthrough](../START_HERE.md#five-minute-learning-cycle-walkthrough) in a fresh local state directory. Confirm that publishing is a separate action from recording a decision, that L02's commercial context is visibly different, and that withdrawal removes active search without erasing the trail. Keep this PR draft and unmerged until owner review.
