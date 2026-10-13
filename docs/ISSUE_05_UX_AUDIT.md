# Issue #5 — Local reviewer UX audit

## Outcome

Two local desktop defects were reproduced and fixed: the queue's **Add DOCX** control was styled as a button but was a non-focusable `label` containing a hidden file input; and the fixed-width queue squeezed the contract title against its route badge until titles wrapped character by character. The control now has native button semantics, and queue title/badge rows can wrap. Focused regression tests protect both changes. The owner’s separate walkthrough adds an unresolved P0 task-clarity finding: the next action and decision entry were hard to discover.

No other defect was confirmed in the sampled local synthetic path beyond the two desktop findings and the owner-reported task-clarity issue below. Creative acceptance remains with the owner. Mobile rendering, assistive-technology behavior beyond the browser accessibility tree, and the full upload/error journey remain **not verified**.

## Reproduction and evidence

**Environment:** refreshed `origin/main` base `442f3f7`; local server at `http://127.0.0.1:8773`, started with a disposable state directory at `/private/tmp/chugchug-issue5-audit-state`; Codex in-app browser; 1280 × 720 desktop viewport; synthetic dataset only. No AI call or external service was used. The owner’s 13 October first-hand Home → Falcon walkthrough is recorded separately in Issue #5 and is included below as owner evidence, not as a qualified-user study or design acceptance.

1. Open Home. The heading says **Review what needs attention**; **Start reviewing** and the three live category counts are buttons. Each category leads to its filtered pending queue. The footer states that every route needs a human decision.
2. Use Tab from Home. Focus reaches Home → Review queue → Reference → Help → Start reviewing. Focus is visible. Activating Start reviewing opens the highest-priority pending contract (T03 / Falcon).
3. Inspect the first T03 view. **Needs closer review** and **Human decision needed** describe the route; the explanation says the wording is a pattern-based flag requiring interpretation. **Added incoming wording** is shown beside **Reference protection**, with links to the exact source passages. The selected historical decision is described as context that may differ.
4. Open **Record decision**. The form says only a person can approve/request amendment/reject/escalate, requires reviewer and rationale, asks which findings were considered, and says recording a decision does not publish it as precedent. Submit blank: native validation focuses **Reviewer name** and displays a required-field message. No event is written.
5. Open Review queue. **Before fix**, the accessibility tree showed `text Add DOCX`; it was absent from keyboard controls. **After fix**, the same position is `button Add DOCX, ID: upload-trigger`; Tab reaches it after the nav and filter. The button invokes the existing DOCX picker. No file was submitted during this audit.
6. Inspect the queue cards at the available browser width. Before the layout fix, the focused Falcon card displayed its name one character per line while the route badge occupied the same row. The title and badge now wrap onto separate lines when their combined width is too large.

Desktop screenshots were captured during these steps in the in-app browser. The available capture surface displayed the accepted images in the audit run but did not expose a local export path; the report therefore records reproducible DOM evidence and steps rather than claiming a committed screenshot artifact.

## Findings

| Priority | Finding | Reproduction | Status |
|---|---|---|---|
| P1 accessibility | **Add DOCX was not keyboard-focusable and lacked button semantics in the accessibility tree.** A styled label around a `hidden` input appeared as plain text and provided no focus target. Screen-reader output was not tested. | Review queue → inspect accessibility tree / Tab sequence. | Fixed with native button semantics and an explicit click handler. |
| P2 usability | **Queue card title collapsed beside the route badge.** In the rendered queue, the fixed-width card wrapped Falcon's name character by character, making the contract hard to scan. | Review queue → focus the first card at the available pane width. | Fixed by allowing the title/badge row to wrap and reserving a readable minimum title width. |
| P0 task clarity | **The next review action and decision entry were not immediately discoverable.** In the owner’s Home → Falcon walkthrough, the first review view felt busy, the reviewer could not immediately tell how to act, and finding **Record your decision** took effort. The owner said the information was useful but too much was presented at once. | Owner’s 13 October walkthrough, described in Issue #5. | Open. Preserve the evidence and checks; evaluate a focused hierarchy change with the owner before claiming acceptance. This report does not prescribe or self-approve a redesign. |

## Focused regression checks

- `node --test tests/test_web_ui.mjs`: covers native upload button semantics/wiring, queue-title wrapping, existing home routing and human decision wording.
- `node --check web/app.js`: syntax check.
- Final branch checks: Python suite **41 passed**; `python3 -m tests.evaluate` **6/6** route agreement; adversarial audit **11/11** critical cases surfaced or safely blocked, **0** false routine routes, **14/16** route matches (A05/A08 are conservative escalations); Node UI suite **6 passed**; app syntax and `git diff --check` passed.
- Responsive CSS defines stacked queue/evidence/form layouts at `max-width:700px`; this was inspected in source only. No narrow viewport was rendered, so mobile fit, horizontal overflow, touch target sizing, and the mobile keyboard path remain unverified.
- Native required-field feedback was observed in the browser. Network/server failure feedback, file-picker selection/cancel, upload rejection, and screen-reader output were not exercised.

## Owner judgement

The owner has already reported that the first Falcon screen feels busy and **Record your decision** was hard to find. The next owner judgement is whether a focused change makes the next action clear while keeping useful evidence accessible. Mobile queue and decision-form comfort remain unverified. This audit and its local synthetic checks are not a legal review or creative acceptance.
