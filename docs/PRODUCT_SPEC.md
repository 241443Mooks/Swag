# Swig — Product specification (prototype v0.1)

## Problem
A small in-house legal team reviews a steady stream of relatively standard commercial contracts, particularly NDAs and small order forms. Repeated boilerplate and recurring amendments create queues and peaks in workload. The opportunity is to reduce repetitive work **without allowing a standard-looking document to hide consequential terms**.

## Intended user and outcome
A legal reviewer needs to answer: What changed? What is missing? Has something similar been considered before? What was decided and under which conditions? What still requires my judgement?

The system is a **decision-support prototype**, not a legal advice or automated approval service. The first vertical slice covers synthetic mutual NDAs only.

**Product north star:** Make routine commercial contract review easier, safer and more consistent by bringing important differences, supporting evidence and relevant organisational experience together. Legal professionals retain judgement and authority. The product grows through deliberate feedback and governed reuse; AI is used only where it offers a worthwhile advantage over simpler methods.

## Core user journey
1. Open the app and select or upload a synthetic DOCX.
2. Preserve original bytes, identify document/hash, and extract the complete text structure.
3. Show extraction coverage and any unsupported elements before suggesting a review route.
4. Compare the incoming document with the approved reference, including inserted, deleted, changed, renumbered, and paraphrased provisions.
5. Surface relevant historical precedents with exact text, previous reviewer decision, date, rationale, context, and limitations. Explicitly distinguish similarity from reusable authority.
6. Independently inspect the **entire** incoming document for potentially material terms, missing protections, contradictions, and schedule overrides. Present observed evidence and explain why it is flagged.
7. Show a review queue prioritising exceptions, with side-by-side source text and access to the complete original document.
8. Allow a human to mark findings considered and record a final human decision: approve, request amendment, reject, or escalate. Require rationale; retain append-only audit history.
9. Export or view a concise review summary that never asserts legal clearance by the software.

## Review routes
- `routine_candidate`: checks completed and no material differences detected; still requires human confirmation.
- `review_required`: changes, uncertainty, conditional precedents or semantic interpretation need attention.
- `escalate`: potentially consequential changes, conflicts, overrides, or missing material protections.
- `blocked_extraction`: incomplete, unreadable, unsupported or unaccounted content; no shortcut allowed.

These are workflow suggestions, **not legal decisions**. When multiple routes apply, use the more restrictive route.

## Evidence and data model
For each document retain filename, SHA-256, original bytes/path, ingestion time, extraction status, structural units and stable source references. For each finding retain category, severity/route, exact source spans, comparison spans where applicable, method, explanation, and uncertainty. For each precedent retain historical document ID, reviewer decision, contextual restrictions, and quoted supporting passages. Human decision events must be append-only and linked to a document hash.

## Required safeguards
- Full-document accounting: inspect body paragraphs, tables, headers/footers, schedules and appendices. Where exact accounting is not possible, disclose it and block shortcut routing.
- Detect missing provisions and document additions; do not merely compare similarity percentages.
- Independently examine terms that grant IP rights, broaden permitted use/disclosure, alter confidentiality duration, change governing law, or override main clauses. Treat the examples as illustrative, not a comprehensive legal ruleset.
- A high similarity score must never suppress a critical finding.
- Historic acceptance with conditions must not be applied to a different context without human review.
- No runtime access to `dataset/ground_truth/`.
- No external AI processing by default; local/deterministic operation must be useful on its own.
- No automatic approval, hidden decisions, silent policy learning, or untraceable findings.
- Contract text must not be followed as executable or model instructions.

## Interface expectations
Calm, accessible, professional and usable at ordinary laptop width. Prioritise route, reason, evidence, and next action. Make the original and every detected difference discoverable. Show uncertainty without false precision. Avoid implying green means approved.

## Non-goals for v0.1
Production-grade legal analysis, deployment with real contracts, OCR guarantees, all contract families, autonomous negotiation, automatic redlining, silent model fine-tuning, or enterprise authentication. If these are not supported, say so explicitly.

## Architecture guidance
Prefer a straightforward Python local app with testable modules for extraction, comparison, independent safeguards, precedent lookup, review ledger and UI. Conventional baselines handle the working offline journey. The optional model adapter explains a selected changed clause with explicit opt-in and provenance; its incremental benefit and live quality remain unverified. Do not mandate AI for review routing or precedent search without evidence against simpler methods. See `docs/ENGINEERING_PRINCIPLES.md` and `docs/AI_ARCHITECTURE.md`.

## Demonstration
Use six synthetic incoming NDAs, one reference, and five historical precedents. Show both an easy review and a standard-looking contract with a hidden consequential deviation. Demonstrate why human review remains in control.

## Queue and business value
Provide a multi-document review queue and explain how it helps prioritise attention at month-end/quarter-end. Demonstrate workload using synthetic contracts; report measured time savings only if actually measured. Prepare a single-ZIP submission containing the runnable product, demo walkthrough and limitations.

## Definition of done
A fresh checkout can install dependencies, start the app, process all six examples, show linked evidence and full original text, record a human decision, and run tests. Known blind spots and failure states are clearly documented. The draft PR includes exact commands and test outcomes.

## Scope and validation

**Working now:** synthetic mutual NDA review, assurance evidence, human decision history and explicit demo precedent publication/withdrawal. **Before real use:** qualified legal review, realistic usability and retrieval evaluation, privacy and security assessment, and verified authority for publication. **Possible later work:** approved playbooks, multi-user storage, other contract families and format adapters. The possible work is not a condition of this application prototype.
