# Swag — Precedent-Aware Contract Review

A human-led prototype for reviewing routine commercial contracts using reference wording, previous review decisions, and independent full-document safeguards.

## Status
**Working local proof of concept; pending human QA and live-AI verification.** The 12 synthetic DOCX contracts are committed in `dataset/`. Start with [START_HERE.md](START_HERE.md).

## Repository map
- `dataset/reference/` — one baseline synthetic mutual NDA
- `dataset/historical/` — five historical synthetic NDAs
- `dataset/incoming/` — six challenge documents
- `dataset/review_records/` — fictional decisions, not approved policy
- `dataset/ground_truth/` — held-out evaluation answer key; **never accessible to runtime**
- `swag/` — conservative extraction, comparison, safeguards, precedent search, AI adapter, ledger and local server
- `web/` — queue and reviewer interface
- `tests/` — adversarial, HTTP journey and isolated evaluation checks
- `START_HERE.md` — startup, walkthrough and limitations
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

## Review status
The implementation is ready for owner QA on a feature branch. See `docs/SPRINT_01_STATUS.md` for test evidence and remaining verification. Human creative acceptance and live AI quality are pending; the draft PR must remain unmerged.

This project is a demonstration, not a production legal review service or legal advice.
