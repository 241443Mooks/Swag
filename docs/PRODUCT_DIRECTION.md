# Swig — product direction

**Working direction, 11 October 2026.** This records the owner's direction and the narrow synthetic learning-cycle demonstration added on the current feature branch. It does not declare the product ready for submission or real contracts.

## The product we are building toward

Make routine commercial contract review easier, safer and more consistent by bringing **important differences, supporting evidence and relevant organisational experience** together. Swig should make the next review easier by showing relevant past wording, decisions, reasons and conditions alongside the current document's evidence. A legal reviewer remains responsible for deciding whether that history applies. Deliberate feedback and governed reuse should increase usefulness over time; AI is used only where it offers a worthwhile advantage over simpler methods.

The experience stays simple: find the work needing attention, understand why, inspect the source and relevant history, then record a decision. Underneath, source coverage, check status, provenance, authority and uncertainty must remain explicit. Similarity to a previous acceptance never means approval.

## What exists today

The prototype has a working review journey for synthetic mutual NDAs: queue routing, source-linked findings, comparison and independent indicators, a concise Assurance view, five fixed historical records for lexical precedent retrieval, and an append-only local decision ledger. The ledger records document hash, reviewer label, decision, rationale, conditions, finding references and timestamp.

**Recording a decision is not itself publication.** The current feature branch adds a separate, append-only publication event linked to a recorded decision and exact source passage. A named demonstration legal reviewer must explicitly publish it with commercial context and reuse limits. The single lexical retrieval path then searches both the five fixed historical records and active published examples. Withdrawal removes an example from active search while retaining its history. This local role is self-attested; there is no identity verification or production authorisation.

Every precedent result remains context about a past case. It has no authority to change a review route or to approve wording. The current system neither updates an approved playbook nor evaluates reviewer corrections as improvements to its checks. Optional AI explains selected changed wording only when explicitly enabled and invoked; its live quality has not been established.

## The governed learning loop

1. **Review:** Bring the current document's differences, safeguards, evidence and relevant prior cases to a person.
2. **Record:** Preserve the human decision, rationale, conditions and source-linked findings.
3. **Assess reuse:** A legal reviewer decides whether a past decision is sufficiently documented and applicable to future cases. Record its commercial context, conditions and limits.
4. **Publish knowledge:** Make a selected precedent searchable with its source, status, publisher, version and withdrawal history. Treat authorised playbook guidance as a separate, more authoritative record.
5. **Improve:** Measure retrieval usefulness, repeated questions, missed exceptions, unnecessary escalations and reviewer corrections. Turn verified failure examples into regression cases and revise checks or guidance through review.

Steps 1–4 are demonstrated only in a local, synthetic, single-user form. Step 5 and real authorisation remain proposed. None requires automatic model retraining. A reviewed precedent helps a person reason about a new case; it does not authorise Swig to decide that case.

## How development should work with the legal team

Swig should be developed **with the legal team, without making them responsible for building it**. Their knowledge of normal amendments, commercial context, escalation thresholds and practical review work is the starting point. The developer's responsibility is to translate that knowledge into a usable, testable system. The developer must not invent legal policy in the absence of legal expertise.

Use a repeating, proportionate cycle:

1. **Understand together.** Spend focused time observing the team, examining representative contracts and asking what they check first, which variations recur, which decisions depend on context, where work slows down and what would make a tool untrustworthy. Agree a small initial scope and how success will be judged.
2. **Develop independently.** Protect time to design, build, investigate and test a bounded improvement. Use deterministic methods where they are sufficient; assess AI only where it might add demonstrable value. Return with something usable rather than requiring the team to supervise implementation.
3. **Test together.** Have legal professionals try representative examples and observe how they actually work, including hesitations, misunderstandings, missed issues, unnecessary escalations and whether they can challenge the system. Ask them to validate the legal assumptions and decide whether the result is useful and safe enough for its intended scope.
4. **Iterate periodically.** Collect feedback and recurring patterns, prioritise improvements by impact and risk, then repeat. Keep a stable useful product between iterations; do not create a permanent dependency on development activity.

**Learning during use is a parallel activity, not an automatic rule change.** Normal reviews can capture source-linked decisions, reasons, conditions and corrections. A suitably authorised person can explicitly publish selected examples as contextual precedents. Repeated patterns may suggest changes to checks or approved playbooks, but these require separate review, testing, versioning and authorisation. Neither one person's decision nor a frequently repeated practice should silently become policy.

The intended outcome is a product that grows in usefulness as the team works, with minimal extra administration. The team owns legal judgement and acceptance criteria; the developer owns implementation and technical assurance; organisational owners must establish publication authority, privacy, security and deployment controls.

**Current boundary:** This collaboration model is a proposed way of working, not an activity completed for the prototype. No qualified legal professional has yet validated Swig, and there are no observed real-team usability or productivity results.

## Validation before real use

The next decision is whether a legal reviewer can use the current journey quickly and correctly. Human creative acceptance, legal assessment of representative wording, retrieval usefulness, and realistic exception testing remain open. Real documents additionally require privacy, security, verified publication authority and operational controls. These are gates for real use, not features to add to this application prototype.

## Possible later investments

1. **Validate and harden the demonstrated reuse loop.** Test retrieval usefulness and context mismatch with legal reviewers. Before real contracts, replace self-attested demo publication with actual identity, roles and approval policy; define correction and version governance. Promotion must never silently change routing or legal approval.
2. **Introduce versioned playbooks.** Separate individual precedents from approved organisational guidance, with named authority, effective dates, change history and reversal. Do this after the team defines who may publish guidance and how conflicts are resolved.
3. **Establish evaluation.** Collect reviewer corrections and usefulness feedback without converting them directly into policy. Test retrieval relevance and safety on independent, representative cases before claiming that support has improved.
4. **Extend the foundation.** Add format-independent source spans and extraction adapters before PDF or OCR; add secure multi-user storage, access control and data governance before real commercial contracts.

The synthetic slice demonstrates decision → explicit demo publication → contextual retrieval in a later review → withdrawal. Tests show that an unpublished decision stays out of search and a superficially similar but materially different contract retains its own review route and human decision. This is evidence of **workflow plumbing**, not evidence that retrieval is legally useful or that publication authority is secure.

## Submission claim and limits

Describe Swig as **a working foundation for an evolving, precedent-aware legal review system**. Demonstrate the current end-to-end review, source evidence, historical context, Assurance view, human decision capture and the small synthetic publication/withdrawal loop. Make clear that only explicitly published decisions enter later search. Do not call the prototype self-learning or claim measured legal accuracy or time savings from the synthetic demonstration.

Before real use, the legal team must define publication authority, required context and conditions, and how conflicting or withdrawn guidance is handled. Human creative acceptance and submission QA remain open. The possible investments above are not prerequisites for demonstrating the current prototype.
