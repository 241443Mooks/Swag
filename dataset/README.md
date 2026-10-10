# Precedent Lab — synthetic contract dataset v0.1

**Purpose:** Test a precedent-aware, human-in-the-loop contract review prototype. All names, decisions, parties, and contracts are fictional. Not legal advice or valid commercial templates.

## Contents
- `reference/`: one baseline mutual NDA.
- `historical/`: five prior NDA examples.
- `review_records/historical_decisions.csv`: fictional decisions with context and limitations.
- `incoming/`: six new NDAs, including deceptively familiar but problematic examples.
- `ground_truth/expected_findings.csv`: answer key; **keep outside the prototype's accessible folders**.

## Suggested experiment
1. Index the reference and historical contracts with the decision register.
2. Ingest the six incoming files one at a time.
3. Compare clauses, including omitted clauses, addenda and overriding language.
4. Retrieve precedents, but distinguish similarity from permission to reuse.
5. Run independent safeguards on the full original document.
6. Record reviewer approval, rejection, correction and escalation without silently changing policy.
7. Compare output to the held-out answer key.

## Acceptance criteria
- Original document preserved and fully accessible.
- Every section, including schedules, accounted for; failed extraction blocks quick review.
- Changed, inserted, removed, paraphrased and contradictory wording surfaced with source citations.
- A previous approval never automatically authorises a new contract.
- Critical surprises T03, T04 and T05 must not be routed to quick approval.
- An uncertain or failed check produces a review-required outcome.

## Limitations
Synthetic data does not establish legal validity or performance on real contracts. The pack contains a deliberately small and consistent clause family; evaluate on broader formats and adversarial cases before deployment.
