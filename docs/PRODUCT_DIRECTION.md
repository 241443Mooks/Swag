# Swag — product direction

**Working direction, 11 October 2026.** This records the owner's direction for future planning. It does not expand the proof of concept's implemented scope or declare it ready for submission.

## The product we are building toward

Help a small legal team turn its review history into **governed, reusable organisational knowledge**. Swag should make the next review easier by showing relevant past wording, decisions, reasons and conditions alongside the current document's evidence. A legal reviewer remains responsible for deciding whether that history applies.

The experience stays simple: find the work needing attention, understand why, inspect the source and relevant history, then record a decision. Underneath, source coverage, check status, provenance, authority and uncertainty must remain explicit. Similarity to a previous acceptance never means approval.

## What exists today

The prototype has a working review journey for synthetic mutual NDAs: queue routing, source-linked findings, comparison and independent indicators, a concise Assurance view, five fixed historical records for lexical precedent retrieval, and an append-only local decision ledger. The ledger records document hash, reviewer label, decision, rationale, finding references and timestamp.

**Recording a decision is not yet learning from it.** `swag/engine.py` loads the five historical contracts and decision CSV at startup and retrieves precedents from that library. New events in `swag/ledger.py` appear in decision history, but are not added to precedent search. The ledger also has no separate, structured fields for commercial context, conditions on reuse or publication authority. The current system neither updates an approved playbook nor evaluates reviewer corrections as improvements to its checks.

The current precedent result is context about a past case. It has no authority to change a review route or to approve wording. Optional AI explains selected changed wording only when explicitly enabled and invoked; its live quality has not been established.

## The governed learning loop

1. **Review:** Bring the current document's differences, safeguards, evidence and relevant prior cases to a person.
2. **Record:** Preserve the human decision, rationale and source-linked findings. The prototype substantially demonstrates steps 1 and 2.
3. **Assess reuse:** An authorised legal reviewer decides whether a past decision is sufficiently documented and applicable to future cases. Record its commercial context, conditions and limits.
4. **Publish knowledge:** Make a reviewed precedent searchable with its source, status, authorisation, version and withdrawal history. Treat authorised playbook guidance as a separate, more authoritative record.
5. **Improve:** Measure retrieval usefulness, repeated questions, missed exceptions, unnecessary escalations and reviewer corrections. Turn verified failure examples into regression cases and revise checks or guidance through review.

Steps 3–5 are a **proposed capability**, not implemented behaviour. They do not require automatic model retraining. A reviewed precedent helps a person reason about a new case; it does not authorise Swag to decide that case.

## Next investment, in order

1. **Make selected new decisions reusable.** Add a deliberate promotion workflow for a decision with its exact source wording, document identity, rationale, commercial context, conditions, reviewer and authorising person. A published record must be versioned and withdrawable. Search should show why it was retrieved and whether its context differs. Promotion must not silently change routing or legal approval.
2. **Introduce versioned playbooks.** Separate individual precedents from approved organisational guidance, with named authority, effective dates, change history and reversal. Do this after the team defines who may publish guidance and how conflicts are resolved.
3. **Establish evaluation.** Collect reviewer corrections and usefulness feedback without converting them directly into policy. Test retrieval relevance and safety on independent, representative cases before claiming that support has improved.
4. **Extend the foundation.** Add format-independent source spans and extraction adapters before PDF or OCR; add secure multi-user storage, access control and data governance before real commercial contracts.

The first investment is worth implementing only when it can demonstrate the full chain: decision → review for reuse → authorised publication → contextual retrieval in a later review → withdrawal or correction. A test must show that conditional acceptance and a superficially similar but materially different case do **not** become blanket permissions. If that chain cannot be built coherently, keep it a roadmap item rather than add a second, ungoverned precedent path.

## Submission claim and limits

Describe Swag as **a working foundation for an evolving, precedent-aware legal review system**. Demonstrate the current end-to-end review, source evidence, historical context, Assurance view and human decision capture. Explain the governed learning loop as the next stage, with the current boundary visible. Do not call the prototype self-learning, imply that newly recorded decisions already inform future reviews, or claim measured legal accuracy or time savings from the synthetic demonstration.

Before any submission or next feature, the owner should review this direction and the legal team should define publication authority, required context and conditions, and how conflicting or withdrawn guidance is handled. Human creative acceptance and submission QA remain open.
