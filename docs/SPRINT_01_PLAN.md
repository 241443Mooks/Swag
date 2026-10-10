# Sprint 01 — Controlled autonomous build

## Objective
Deliver a locally runnable precedent-aware mutual NDA review product with at least one genuine, commercially justified AI capability, with independent safeguards, a multi-document triage queue, and human-only final decisions. Follow `AGENTS.md`, `docs/PRODUCT_SPEC.md`, `docs/AI_ARCHITECTURE.md`, `docs/ACCEPTANCE_TESTS.md`, and the quality/test/delivery documents.

Read `docs/ENGINEERING_PRINCIPLES.md` first. Evaluate business value, reliability, latency and cost before choosing AI or extra infrastructure.

## Scope freeze
In scope: DOCX ingestion and original preservation; extraction coverage; clause comparison; precedent retrieval with context; genuine model API adapter and structured analysis; independent full-document controls; evidence-linked findings; review routing; multi-document queue; append-only human review events; tests; local setup; reviewer walkthrough; single ZIP.
Out of scope: production deployment, real/confidential contracts, autonomous legal approval, OCR guarantees, broad contract families, negotiation automation, enterprise auth, background jobs, speculative refactors and unrelated features. Do not expand scope without explicit approval.

## Execution gates
### Gate 1 — Dataset and extraction audit
Inventory all 12 DOCX files; verify readable contents and structure including tables, headers/footers and schedules; reconcile historical IDs; define stable source anchors and extraction coverage. Record issues. **Do not proceed with assumptions that make extraction silently incomplete.**

### Gate 2 — Core engine
Implement source preservation, parsing, comparison, missing/added clauses, independent full-document safeguards, precedent retrieval and structured findings. Validate against unit tests and unseen mutations. Demonstrate no route can automatically approve.

### Gate 3 — Genuine AI
First compare the conventional baseline for a selected semantic task (such as paraphrase interpretation or contextual explanation). Record the rationale in `docs/decisions/`. Implement a real provider integration only for a use case that earns its place, with explicit opt-in, configurable model, structured outputs, source-anchor validation, timeouts and failure behaviour. Test using mocks; perform a real call only if credentials and permission are available. If not, report live AI **unverified**, never simulate it.

### Gate 4 — Reviewer experience and delivery
Implement queue, evidence navigation, original access and append-only human decision logging. Test a fresh install and UI walkthrough. Build a single submission ZIP excluding secrets and generated sensitive caches. Open a draft PR; do not merge.

## Time and change discipline
- Work on one feature branch, with coherent commits at each gate. Keep diffs focused; avoid unrelated cleanup.
- Prefer an end-to-end working slice over breadth. Never reduce safety checks to meet time.
- At each gate write a concise checkpoint in `docs/SPRINT_01_STATUS.md`: commit SHA, work completed, commands run, tests passed/failed, blockers, next steps. Do not label a gate passed without evidence.
- Do not continue beyond a failed critical gate by pretending it passed. Remediate within budget, otherwise stop with an actionable report.
- No automatic merging, public deployment, real contract processing or external transmission without explicit user permission.

## Stop conditions
Stop and report a blocker when: (1) three materially different attempts fail to resolve the same issue; (2) a critical safety regression cannot be repaired promptly; (3) required credentials, access or budget are unavailable; (4) document content loss/coverage cannot be determined; (5) a required external capability cannot be verified and proceeding would imply false success. Other independent offline work may continue if clearly separated and does not conceal the blocker.

## API cost boundary
No spending authority is implied by this plan. Do not make paid model calls without explicit opt-in, configured credentials and a user-defined budget. Support a per-document call cap, a session-wide call cap and configurable token/output limits. If caps are not configured, default to no live calls. Never commit credentials or log raw keys.

## Final handover
Provide branch/PR, commit checkpoints, startup commands, actual test evidence, live AI verification status, critical safety-case outcomes, screenshots or UI walkthrough evidence when available, known limitations, cost/configuration instructions and ZIP location. Avoid unverified claims of readiness or time saved.
