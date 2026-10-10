# Swag — Precedent-Aware Contract Review

A prototype for safe, human-led review of routine commercial contracts.

## Aim

Reduce repetitive reading by finding relevant historical decisions and highlighting document differences, while retaining independent safeguards and access to the full original document.

## Principles

- Similarity is not approval.
- Process the whole document; missing or unreadable content requires escalation.
- Distinguish previous decisions from approved policy.
- Show exact passages and preserve original evidence.
- Human reviewers make the final decision.
- Use synthetic contracts only in this prototype.

## Initial dataset

Dataset v0.1 contains 12 synthetic Word documents (1 reference, 5 historical, 6 incoming), a historical-decision register and a separate ground-truth test register. The dataset ZIP was created in the project conversation; the Word binaries are not yet committed here.

## Proposed structure

- `dataset/reference/` — approved template
- `dataset/historical/` — fictional previously reviewed contracts
- `dataset/incoming/` — test inputs
- `dataset/review_records/` — fictional reviewer decisions
- `dataset/ground_truth/` — expected test results, kept inaccessible to the review engine

## Status

Day 1: dataset and scope definition. Prototype implementation to follow.
