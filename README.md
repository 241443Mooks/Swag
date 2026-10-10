# Swag — Precedent-Aware Contract Review

A human-led prototype for reviewing routine commercial contracts using reference wording, previous review decisions, and independent full-document safeguards.

## Status
**Dataset ready; application not yet implemented.** The 12 synthetic DOCX contracts are committed in `dataset/`.

## Repository map
- `dataset/reference/` — one baseline synthetic mutual NDA
- `dataset/historical/` — five historical synthetic NDAs
- `dataset/incoming/` — six challenge documents
- `dataset/review_records/` — fictional decisions, not approved policy
- `dataset/ground_truth/` — held-out evaluation answer key; **never accessible to runtime**
- `docs/PRODUCT_SPEC.md` — workflow, review states, data and safety requirements
- `docs/ACCEPTANCE_TESTS.md` — test cases and mandatory release gates
- `docs/AI_ARCHITECTURE.md` — scoped genuine model integration, provenance and queue triage
- `docs/ENGINEERING_PRINCIPLES.md` — engineering, business-case and UX standards; AI only when justified
- `docs/CREATIVE_INTENT.md` — simple on the surface, robust underneath
- `docs/EXPERIENCE_PRINCIPLES.md` — calm, evidence-led reviewer journeys
- `docs/CREATIVE_REVIEW.md` — human creative acceptance checkpoint
- `docs/DESIGN_JOURNAL.md` — design discoveries and hypotheses
- `docs/decisions/` — evidence-based design decision records
- `AGENTS.md` — autonomous coding-agent instructions

## Non-negotiable principles
- AI must earn its place: prefer a reliable conventional solution when it meets the need as well or better.
- Similarity is not safety or approval.
- Inspect the whole document, including schedules and omitted clauses; incomplete extraction blocks shortcut routing.
- Show exact source passages and preserve original bytes.
- Previous decisions are context-specific and do not automatically create policy.
- Humans make every final decision.
- Synthetic data only. No external AI processing by default.

## First development task
Audit the actual DOCX files and implement the vertical slice described in `docs/PRODUCT_SPEC.md`. Work in a feature branch and open a draft PR; do not merge automatically.

This project is a demonstration, not a production legal review service or legal advice.
