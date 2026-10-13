# Missed-exception and assurance audit — 11 October 2026

## Scope and method

This audit challenged draft PR #1 at exact commit `2ea24ae`. The original implementation was run against the same 16 committed synthetic DOCX files using an isolated detached checkout. The unchanged six incoming scenarios were evaluated separately. The challenge set and expectations live in `dataset/adversarial/manifest.json`; the exact observations are in `ADVERSARIAL_BASELINE.json` and `ADVERSARIAL_AFTER.json`. These cases were authored for failure discovery, so the results are **not** an estimate of real-world legal accuracy or an unseen validation score. No ground-truth source contract or original answer key was edited.

“Surfaced” means a non-routine route with a source-linked finding **or** an explicit extraction defect that blocks the shortcut. It does not mean the legal issue was understood. Source-linked findings and safe blocks are reported separately. “False routine” means a critical challenge received `routine_candidate`. “Unnecessary escalation” means `escalate` exceeded the case’s prewritten routine/review target; it is reported even when the case is marked critical. Those two current over-target cases may still warrant escalation, but the disagreement is left visible.

| Measure on this authored set | PR #1 | This branch |
|---|---:|---:|
| Critical cases surfaced or safely blocked | 5/11 | 11/11 |
| Critical cases with source-linked findings | 5/11 | 7/11 |
| Critical cases safely blocked on extraction | 0/11 | 4/11 |
| False routine recommendations | 6/11 | 0/11 |
| Escalations above the written target | 2/9 | 2/9 |
| False escalations in noncritical controls | 2/5 | 0/5 |
| Exact expected routes | 7/16 | 14/16 |

The two remaining route mismatches are A05 and A08: both expected `review_required` and now receive `escalate` because their added product-use grants match a bounded broad-rights indicator. Their source text is shown. This is conservative routing, not proof that the grant has a particular legal effect.

## Processing journey and failure boundaries

| Stage | Actual mechanism | Original exposure | Current assurance / remaining boundary |
|---|---|---|---|
| Intake | Local DOCX bytes and SHA-256; uploads stored beside metadata | An interrupted upload could leave an orphan file that disappeared from the restarted queue; corrupted metadata was silently skipped. | Upload pairs are checked on startup; interrupted or mismatched state fails visibly. Queue analysis rechecks source bytes; original download refuses a changed source. Recovery is manual. |
| Extraction | ZIP/WordprocessingML traversal of body paragraphs, tables, header and footer parts | Duplicate ZIP members, hidden style text, and hidden/struck direct formatting could appear as a clean extraction. | Duplicate members and selected visibility-affecting formatting block extraction. Unknown parts/elements still block. Other visual formatting and relationship integrity are residual risks. |
| Completeness | Parser marks issues and parts; unsupported content blocks review shortcut | “Complete” covered extracted parts, but did not prove their text was all compared. | Assurance separates extraction from comparison and gives part/passages counts. It does not claim general DOCX fidelity. |
| Comparison | Heading-based clause map; text and numbering comparison | Header/footer changes were extracted but ignored; repeated headings merged; clause order is not analysed. | All extracted non-body parts are compared. Repeated headings produce a limitation and review finding. Order and semantic equivalence remain unresolved. |
| Independent safeguards | Regex indicators and missing no-licence heading | “Whole-document” checks actually scanned body only. Negated prohibitions caused false escalation. | Indicators scan every extracted passage. Bounded polarity checks reduce the demonstrated false alarms. They are independent of the diff and precedent ranking, **not** independent of the same extractor, unit text, or heading assumptions. |
| Precedent | Lexical ranking over five historical contracts and CSV decisions | Similar wording might be mistaken for authority; duplicate IDs could overwrite a prior row while the ID-set check passed. | UI retains status, rationale, conditions and “illustrative only” reuse note. Required fields, states and unique IDs are validated at startup. Contextual applicability and retrieval relevance remain unverified. |
| Route | Highest finding severity, blocked extraction first | No finding in ignored content meant a routine route. | Coverage failure blocks; any nonadministrative compared difference requires review; indicators can escalate. No route is legal approval. |
| Interface and human record | Queue, anchored text, original, prior context, append-only JSONL | Original “complete” labels risked implying more than checked; queue could hide a lost upload after restart. | Assurance shows source identity, extraction, comparison, safeguards, indicator count, limits and human status separately. Ledger round trip was exercised. Corrupt ledger recovery and multi-user concurrency remain outside this slice. |

## Case-level challenge record

The expected route was written before changing the engine. “Evidence” names the current source anchor or explicit processing defect. A blocked case provides a reason for manual inspection, not a claim to have detected the contractual meaning.

| Case; risk/change | Expected | PR #1 observed | Current observed; detection and evidence | Unsafe routine in PR #1 → current |
|---|---|---|---|---|
| A01; product-use grant in footer | Escalate | Routine | Escalate; footer `p2` grant and part difference | Yes → no |
| A02; permitted-use override in header | Escalate | Routine | Escalate; header `p2` override and part difference | Yes → no |
| A03; no-licence paragraph directly hidden | Blocked | Routine | Blocked; `vanish` at body `p20` | Yes → no |
| A04; duplicate `document.xml` ZIP member | Blocked | Routine | Blocked; duplicate-part integrity issue | Yes → no |
| A05; repeated clause 9 with product-use grant | Review | Review | Escalate; body `p33`, repeated-heading limitation | No → no |
| A06; no-licence body replaced by product-use grant | Escalate | Review | Escalate; body `p20` and reference | No → no |
| A07; “shall not” changed to “may” | Review | Review | Review; changed body `p8` and reference | No → no |
| A08; unfamiliar know-how product-use grant | Review | Review | Escalate; added body `p32` | No → no |
| A09; added sentence denies broad licence | Review | Escalate | Review; added body `p32`, no broad-right finding | No → no |
| A10; protective notwithstanding sentence | Review | Escalate | Review; added body `p32`, no override finding | No → no |
| A11; party-only change | Routine candidate | Routine candidate | Routine candidate; 0 findings within supported comparison scope | No → no |
| A12; byte-identical supported template | Routine candidate | Routine candidate | Routine candidate; 0 findings within supported comparison scope | No → no |
| A13; no-licence wording displaced after signatures | Review | Review | Review; body `p31` added/unsectioned and clause 9 changed | No → no |
| A14; no-licence paragraph hidden by applied style | Blocked | Routine | Blocked; applied `HiddenProvision` style | Yes → no |
| A15; no-licence paragraph struck out | Blocked | Routine | Blocked; `strike` at body `p20` | Yes → no |
| A16; strike property explicitly disabled | Routine candidate | Routine candidate | Routine candidate; formatting is visibly off | No → no |

## Decisions and trade-offs

- The main protection is complete accounting of **text being assessed**: every extracted non-body part now enters comparison, and the indicator scan covers every extracted passage. This closes a shared blind spot without asking a model to guess unseen material.
- Potentially invisible or struck text blocks the shortcut. Applied hidden/struck styles are checked conservatively; default hidden styles also block. This may require manual review of a document whose problematic style is not visible to the reviewer. That is a cost of not claiming reliable visual interpretation of arbitrary DOCX formatting.
- The broad-rights and override indicators now require bounded affirmative language and avoid a few explicit local denials. These heuristics reduce observed false alarms but are **not** a complete semantic polarity or contradiction parser. A newly worded grant should at least surface as a textual difference; its severity may still be understated.
- No new AI capability was added. The existing optional real-model adapter remains unverified live. The demonstrated misses came from structural coverage and package integrity, which deterministic checks address more directly, cheaply and inspectably. A future semantic interpretation study should compare a real model with this diff baseline using a larger blinded set and human legal review before influencing routes.
- The assurance report is generated from processing records, not a single success flag. “Complete” refers to the named check within its stated DOCX scope. Source identity, extraction, comparison, indicator completion, potential indicators and the human event are distinct states. No confidence percentage or legal all-clear is shown.

## Residual risk register

| Risk | Present treatment | Next evidence or work |
|---|---|---|
| Unfamiliar semantic grant, defined-term change, cross-reference interaction, or contradiction | Text changes route to human review; bounded indicators may not elevate them. | Larger blinded legal challenge set; compare human assessment, lexical baseline and optional live AI without letting AI approve. |
| Semantically equivalent changed wording | Human review remains required; no automatic equivalence claim. | Measure unnecessary reviews with counsel before introducing semantic shortcut logic. |
| Complex DOCX rendering: white-on-white text, tiny font, layered drawing, relationships, conditional fields, style inheritance beyond supported checks | Some known structures block; general visual fidelity and relationship validation are not proved. | Use a mature DOCX rendering/validation layer or block the class after a format inventory; test actual Word rendering against extracted spans. |
| Clause reordering, repeated headings, table reading order, heading synonyms | Repeated headings are flagged; other alignment can be incomplete. | Format-neutral ordered span model with structure validation and independent reconciliation. |
| Precedent quality and context | Required fields and unique IDs are validated; five fictional decisions are shown as context, not policy. | Assess provenance, conflicting outcomes and condition applicability with legal owner. |
| Runtime interruption or local corruption | Upload files/metadata fail visibly; changed source blocks route. Ledger is append-only with fsync. | Recovery UX for orphan uploads and partial/corrupt JSONL; transactional persistence or small database before shared use. |
| Reviewer may approve despite a blocked route | Human authority is intentionally retained; UI says manual review is required. | Test decision language and approval controls with legal reviewers; require explicit evidence of manual review if deployed. |
| Real-contract performance, privacy and concurrent users | Not evaluated; synthetic local-only demo. | Separate consent, security, privacy and legal QA programme. |

## Future PDF, OCR and image intake

The present extractor and anchors are Word-specific (`word/document.xml:pN`, table coordinates, header/footer XML). The engine also identifies body clauses by that Word part name; the UI exposes those anchors. PDF/OCR/image support is therefore **not** a plug-in extraction swap. Before adding formats, introduce a format-neutral source-span contract containing original bytes/hash, page or part, reading order, text, optional bounding box, provenance, supported/unsupported regions and extraction uncertainty. Require reconciliation of all visible regions and render-to-source verification before routine routing. OCR should preserve low-confidence or unreadable regions as explicit blockers. This sprint did not add PDF, OCR, photograph or fax handling.

## Review and reproduction

```sh
python3 scripts/build_adversarial_fixtures.py
python3 -m tests.adversarial_audit --out docs/ADVERSARIAL_AFTER.json
python3 -m unittest discover -s tests -v
python3 -m tests.evaluate
python3 -m swag.server --port 8765 --state-dir .swag-data/audit-demo
```

In the UI, open T03, follow the first source link into the full text, inspect the prior H03 decision, open **Assurance** for check scope, then record a human escalation. For a blocked case, upload A03 or A14 from `dataset/adversarial/` to an isolated local state directory and inspect the explicit limitation. Use T01 for the quick routine-candidate path. Do not submit the synthetic QA decision or these fixtures to PortSwigger as proof of legal accuracy.
