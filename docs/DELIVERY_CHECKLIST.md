# Submission and handover checklist

PortSwigger's application task requests **a single zipped file** showing how AI could help a small legal team with routine contracts, recurring redlines and month-end/quarter-end review peaks. This is an application exercise, not a request for production legal automation.

**Current status:** the working prototype can be reviewed locally. Human creative acceptance and final clean-package QA remain pending. Possible later product investments in `PRODUCT_DIRECTION.md` are not submission requirements. Package the final ZIP after the owner accepts the experience; do not describe an unobserved live AI run as completed.

## Reviewer experience
- [ ] Start with a short `START_HERE.md` explaining the problem, approach, why conventional engineering handles much of it, and where the genuine AI contribution earns its place.
- [ ] Provide a five-to-ten-minute guided walkthrough: routine NDA, context-limited precedent, hidden critical amendment, queue prioritisation, human decision.
- [ ] State what is deterministic, what uses a real model, the baseline and business justification for that choice, and what always requires a person.
- [ ] Include clear instructions for running locally with and without optional configured AI access; offline mode must not impersonate AI.
- [ ] Show how the design could reduce repetitive review and handle peaks; do not invent measured time savings.
- [ ] Explain limits, privacy and why this is not legal advice.

## Technical deliverable
- [ ] One ZIP with runnable source, required dependency manifests, synthetic documents, review register, evaluation instructions and reviewer walkthrough.
- [ ] Clean checkout/install/start succeeds with documented commands.
- [ ] Tests execute and report meaningful results; safety cases T03/T04/T05 pass or failure is prominently disclosed.
- [ ] Actual model integration available with explicit opt-in and provider setup; report if live test unverified.
- [ ] Full originals available, evidence navigation working, review queue usable, decisions auditable.
- [ ] No keys, tokens, local `.env`, private records, sensitive logs, caches, virtual environments, build clutter or unnecessary generated artifacts.
- [ ] Include exact commands, supported Python version, known limitations and dependency constraints.

## Git workflow
- [ ] Work on a feature branch; keep commits coherent and reviewable.
- [ ] Draft PR includes milestone evidence and outstanding issues.
- [ ] Do not merge automatically.
- [ ] Record ZIP creation command and checksum.
- [ ] Confirm the ZIP can be opened and contents inspected independently.
- [ ] Do not submit or upload to the employer automatically.

## Creative QA
- [ ] Reviewer sees what changed, why it matters, relevant history and next action without a wall of text.
- [ ] Full evidence is one interaction away; no shortcut hides missing coverage or failed checks.
- [ ] Human creative review is completed or clearly marked pending; document insights in `docs/DESIGN_JOURNAL.md`.
- [ ] The result feels simple on the surface and robust underneath, not like a generic AI dashboard.

## Final QA
An independent reviewer should be able to answer within ten minutes: What problem does this solve? Where is real AI used? What safeguards exist? Can I run it? What evidence shows it works? What are its limitations?
