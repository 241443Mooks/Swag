# Issue #14 — Owner-led evaluation kit

## Purpose and limits

This kit prepares a repeatable comparison of ordinary, difficult and misleading synthetic NDA reviews. It records no results in advance and makes no claim about speed, quality, legal accuracy or user preference. The current synthetic materials are not a blind test set: filenames, document text and fixtures reveal some scenario intent. Treat this as a rehearsed owner walkthrough and protocol check, not an independent or legally validated benchmark.

Use synthetic files only. Do not enable the optional AI adapter; it is off by default and this kit does not authorize paid calls or external processing. Every route is a recommendation about attention. Only a human reviewer records the legal decision.

## Case set

Use the same case documents and ordinary tools in both conditions. Keep the table visible to the observer; do not use any expected-findings answer key to prepare the assisted result.

| Case | Source | Challenge type | What the session observes |
|---|---|---|---|
| O1 | `dataset/incoming/T01-template-match.docx` | Ordinary | Orientation, source/reference access, human next action |
| D1 | `dataset/incoming/T02-known-term-change.docx` | Difficult | A changed term alongside context from a conditional historical decision |
| D2 | `dataset/incoming/T04-missing-no-licence.docx` | Difficult | An omitted protection and how absence evidence is explained |
| D3 | `dataset/incoming/T05-appendix-overrides.docx` | Difficult | A schedule that may conflict with the main wording |
| D4 | `dataset/incoming/T03-hidden-perpetual-licence.docx` | Difficult | Material added rights among otherwise familiar wording |
| M1 | `dataset/incoming/T06-paraphrase-equivalent.docx` | Misleading | Similar meaning with different wording; whether uncertainty stays visible |

Optional backend-only applicability exercises are provided in `research/reference-library-v0.1/incoming-tests/`: the desktop reseller, hosted-region-change and ambiguous reseller/cloud examples. They are research fixtures, not uploaded product cases. The 20 `routine-clients` documents are not blind matching tests because their metadata contains proposed reference identifiers. Do not use those 20 to claim matching accuracy.

## Session protocol

1. Use a fresh local state directory and confirm it contains no prior decisions. Follow the local-only startup instructions in `START_HERE.md`; do not use a public deployment.
2. For each case, run a **manual baseline** first: inspect the same incoming document and reference in Word or another ordinary local viewer, with the same written instructions and time limit. Record the outcome before opening ChugChug for that case.
3. In the **assisted condition**, use the local synthetic reviewer, inspect the original wording and reference, note any past decision's context, then record a human outcome only if this is part of the planned exercise. Do not treat the displayed route as a legal conclusion.
4. Alternate or randomize which case is first across repeat sessions. If one owner runs both conditions, mark the second pass as learning-contaminated; do not treat the two observations as independent.
5. After each case, complete the blank record template in `docs/evaluation/owner-session-record.csv`. Capture timings with a clock, not estimates. Keep raw observations and quotations attributable to this owner session.
6. Do not open `dataset/ground_truth/` until both independent outputs are recorded. If an answer key exists, a separate evaluator may compare outcomes afterward; the key is not legal validation unless a qualified practitioner reviewed it and recorded that provenance.

## Measures and evidence classes

Record the same measures in both conditions:

- elapsed minutes to a stated human outcome, including any pause;
- material points the reviewer noticed, plus missed or unnecessary points;
- route shown and route the reviewer would choose, kept as separate fields;
- clicks or explicit context switches, counted with a consistent rule;
- confidence from 1–5 and one sentence explaining it;
- perceived cognitive burden from 1–5 and the specific moment that drove it;
- whether the reviewer could locate exact original and reference passages;
- for a later correction exercise, whether a saved comparison correction can be inspected and whether it changes a later review without changing the route or implying approval.

**Automatable:** route/output snapshots, presence of source anchors, extraction status, persisted synthetic decision history, repeatable clicks only where the interface exposes them, and technical correction/retrieval behavior.

**Owner-observed only:** comprehension, confidence, cognitive burden, task clarity, preferences, and observed friction. These are one person's observations, not general user feedback or productivity evidence.

**Qualified legal validation required:** what counts as a material issue, whether a clause's effect was understood correctly, whether a proposed human outcome is legally appropriate, whether a case key is an authoritative expectation, and whether any review shortcut is defensible. The current synthetic fixtures and automated tests do not supply that validation.

## Record and interpretation rules

- Preserve each condition's notes before comparing conditions. Do not tune the product or test expectations between the manual and assisted pass.
- Report all six cases, including omissions, false alarms, incomplete extraction, and cases where the reviewer disagrees with the displayed attention route.
- Report counts and raw observed times only. Do not extrapolate one owner's results to workload reduction, legal accuracy, or other reviewers.
- If using a qualified reviewer later, document role/qualification, scope, date, conflicts, review method, and which expectations they actually validated.
- Keep evaluation answer keys isolated from runtime, prompts, matching, and pre-comparison notes. Never modify source contracts or expected answers to improve a score.

## Current readiness

The kit and case list are reproducible. No evaluation session, user study, legal review, time comparison, accuracy score, or business benefit has been completed by preparing this kit. The order-family UI is not implemented; the optional order examples support only scoped backend/applicability work and cannot be counted as an end-to-end reviewer evaluation.

## Blank session template

Copy `docs/evaluation/owner-session-record.csv` for each run. Leave cells blank rather than substituting guesses. Keep one copy per condition and include the product commit, environment, local-state path label, case order, and any interruptions in the session notes.
