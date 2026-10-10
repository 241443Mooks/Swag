# Quality gates and release blockers

A gate passes only when supported by executable checks or recorded manual evidence. Passing unit tests alone does not prove a working product.

## Gate 1 — Input integrity
- All 12 synthetic DOCX files are inventoried and readable.
- Each original is preserved byte-for-byte with SHA-256.
- Structural extraction accounts for paragraphs, tables, headers/footers, schedules and appendices, or explicitly marks unsupported/omitted elements.
- Decision register references match historical documents.
- Ground truth is segregated from runtime ingestion and retrieval.
**Blocker:** silently omitted or unaccounted document content.

## Gate 2 — Engine and safeguards
- Comparison identifies insertions, deletions, changes and missing clauses.
- Independent whole-document checks can flag a critical issue despite high similarity.
- T03, T04, T05 are escalated with correct supporting evidence; no quick-review path for these cases.
- Failed/incomplete extraction blocks quick review.
- Historical approval, rejection and conditional acceptance remain distinguishable.
- Evidence anchors resolve to actual source passages.
**Blocker:** missed critical scenario, fabricated source anchor, or automatic legal approval.

## Gate 3 — Genuine AI
- At least one candidate AI use case has a recorded conventional baseline and a justified expected advantage (quality, reviewer effort, or otherwise), including cost/latency/privacy trade-offs.
- A real model provider adapter exists for that justified use case, with explicit user opt-in, model configuration and documented data transmission.
- Outputs are schema-validated and citations checked against extracted source anchors.
- No provider/key, timeout, malformed output or failed anchor validation cannot produce fake AI findings or an inappropriate routine route.
- Mock-based integration tests pass; live-provider execution is **separately** evidenced when credentials/budget are available.
- Provider/model/status and analysis timestamp are visible to reviewer.
**Blocker:** simulated analysis presented as live, unsafe fallback, secret leakage.

## Gate 4 — Experience and packaging
- A fresh checkout can install and run using documented commands.
- Actual DOCX upload, analysis, source navigation, multi-document queue and reviewer decision are manually exercised.
- A human creative review checkpoint is prepared under `docs/CREATIVE_REVIEW.md`; if not yet performed, explicitly mark creative acceptance as pending rather than passed.
- Human decision events persist append-only.
- A single ZIP contains source, synthetic dataset, explanation, setup and reviewer walkthrough, with no keys, caches or private data.
- A draft PR is opened with exact test results, limitations and any unverified live AI features.
**Blocker:** product cannot run from instructions, source unavailable, misleading demo, or missing requested ZIP.

## Regression policy
Re-run critical extraction, routing, isolation and no-auto-approval tests after changes to parser, analysis, prompts, routing or data models. A failed critical regression must be fixed or clearly reported; never delete, skip or weaken tests to get green status.

## Completion language
Use `passed`, `failed`, `blocked` or `not verified` for each gate. Avoid `done` or `production-ready` without evidence. Distinguish measured results from estimates and synthetic demonstrations.
