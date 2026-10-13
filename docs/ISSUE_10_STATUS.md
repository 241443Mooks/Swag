# Issue #10 — Workspace foundation status

## Built on the Issue #8 legal journey

- Optional `#explore` view, linked quietly from Home. The active Legal tile opens `#queue`; four visually muted cards are descriptive concepts with no click, route or data. Home and Review queue remain direct daily paths.
- `swag/nda_pack.py` now owns NDA-specific reference acceptance, comparison policy, labels and bundled source locations. `App` continues to own source integrity, audit events and routing of requests. This is a narrow, tested seam for one active family, not a second pack or general plugin system.
- [Decision 002](decisions/002-legal-pack-and-workspace-boundary.md) separates the shared application, NDA pack, optional overview, absent role/tenant boundary and future concepts. The [annotated wireframe](ISSUE_10_WORKSPACE_WIREFRAME.md) records the proposed experience.

## Verification

Final working-tree gate before commit: `python3 -m unittest discover -s tests -v` passed **31 tests** (including the new pack-boundary test); `python3 -m tests.evaluate` passed **6/6 original routes**; `node --check web/app.js` and `git diff --check` passed. CI and owner creative acceptance remain separate gates.

Rendered browser inspection on local port 8793: desktop and 390 px wide Explore views displayed the working Legal card and one-column concepts correctly. The accessibility tree exposed the Legal action and ordinary navigation as buttons; concept cards were headings and text only. Home → Explore → Legal queue and mobile Legal → queue both reached the real six-item queue. This is navigation and layout evidence, not a formal screen-reader usability study.

## Honest boundaries and owner review

The current Legal demo remains synthetic, DOCX-only and NDA-family-specific. The backend and UI still contain some legal/demo assumptions; a second pack will need its own specialist logic, template and independent tests. No production tenant isolation, verified roles or multi-department sharing exists. Other departments and small customer order forms are concepts. The optional AI integration is off by default; live benefit is unverified. No assertion of legal safety or real-world productivity follows from these tests.

**Creative acceptance is pending.** Inspect whether the optional overview explains the direction quickly without making routine Legal work slower or suggesting that concept cards already work. Start at Home, open Explore, then enter the Legal queue and return to a normal review.
