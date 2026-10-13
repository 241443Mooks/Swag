# ChugChug — review the exceptions first

PortSwigger's task describes a small legal team receiving mostly standard commercial contracts, many with familiar amendments, while its queue grows faster than it can read everything. This proof of concept reorganises six **fictional mutual NDAs** around the exceptions that deserve a person's attention. It is decision support, not legal advice or automatic approval.

**Product direction:** ChugChug makes routine commercial contract review easier, safer and more consistent by bringing important differences, source evidence and relevant organisational experience together. Legal professionals retain judgement and authority. The synthetic prototype demonstrates a governed reuse cycle: a new decision enters later precedent search only after explicit local demo publication, and can be withdrawn. This does not create production authorisation or organisational policy. See [Product direction](docs/PRODUCT_DIRECTION.md).

## Risks, concerns and responsible use

ChugChug explores whether a small legal team can spend less effort on repetitive contract checks, notice important exceptions and preserve the reasoning behind earlier decisions. **It is a workflow demonstration, not legal advice, an autonomous approval system or a validated legal product.**

**Design principle:** Technology should earn its place by improving human capability, not by making human judgement subordinate to the technology. Faster processing alone is not proof of better decisions or a better working environment.

| Concern | Current safeguard or approach | What remains unresolved |
| --- | --- | --- |
| Missed legal issues | Source-linked differences, omission checks, independent indicators and conservative routing | These checks cannot identify every legally material issue; synthetic expected outcomes are not legal validation |
| False reassurance | Unsupported extraction blocks routine routing; a routine *candidate* still requires human confirmation | Reviewers might over-trust reassuring labels or incomplete checks |
| Precedent misuse | Explicit publication with source, rationale, conditions and reuse limits; withdrawal retains history | Similar language may have a different legal or commercial effect; publisher identity is self-attested |
| Automation bias | The system does not approve contracts or transfer earlier approval to a new case | Time pressure may still discourage independent review or challenge |
| Unnecessary AI | Conventional methods handle predictable work; model interpretation is optional, scoped and cannot change the route | No live provider-quality, benefit, latency or cost evaluation has been completed |
| Confidentiality and security | Local, synthetic-only demonstration; no external AI call by default | Real contracts need privacy, supplier, access-control, security and retention assessments |
| Accountability | Source identity and append-only review/publication events | No production roles, authorised legal playbook, monitoring or operational recovery process |
| Impact on people | Designed to reduce repetitive effort and surface evidence | Efficiency could be used to intensify workloads or monitor individual staff rather than support them |

### Evidence and boundaries

Automated tests, adversarial synthetic DOCX cases and the demonstrated publication/retrieval/withdrawal cycle establish that selected technical behaviours work in the tested conditions. They **do not establish legal accuracy, real-contract safety or measurable time savings**. No qualified legal professional has reviewed or validated this prototype. Legal subject-matter review, realistic user testing and an authorised operational design would be necessary before deployment.

Human oversight must be meaningful: a reviewer needs access to the original wording, the ability to question the comparison or precedent, and authority to make an independent decision. Whether ChugChug actually improves reviewer autonomy and reduces cognitive burden remains untested.

### Why AI is optional

AI is not the default solution. For predictable, testable tasks, conventional software is the starting point. Model-assisted interpretation should be retained only if comparison against that baseline shows a worthwhile improvement in understanding or outcomes, after accounting for errors, confidentiality, latency, running costs and maintenance. A decision *not* to add AI can be a valid outcome of that evaluation.

### Governance and ethics lens

The design is informed by themes associated with the IAPP AIGP body of knowledge, the EU AI Act's risk-based approach, and the human-centred ethical principles discussed in *Magnifica Humanitas*: proportionality, transparency, accountability, human dignity, professional autonomy and consequences for workers. These are **design considerations, not claims of AIGP certification, EU AI Act compliance or ethical endorsement**. Whether particular legal obligations apply depends on the actual AI functionality, intended use and deployment context, and requires separate assessment.

**The unresolved question:** Can legal professionals make better-informed decisions with less unnecessary effort, while retaining their independence, expertise and accountability? The developer and automated tests cannot answer that alone.

## Start in under a minute

Requires Python **3.9 or newer**. No package installation, account or API key is needed for the offline journey.

```sh
python3 -m chugchug.server --port 8771
```

Open `http://127.0.0.1:8771`. The server binds only to loopback. Start from the repository root. If 8771 is busy, choose another unused port. Decisions and uploaded local demonstration files go into ignored `.chugchug-data/`; a clean checkout starts without reviewer decisions. Use synthetic documents only.

Home leads with **Start reviewing** and live counts for **Needs closer review**, **Needs judgement** and **Looks routine**. Each count opens a queue filtered to contracts still awaiting a human decision. **Review queue** also provides **Add DOCX**. The selected reference for new uploads is linked from Home; each existing review remains bound to the reference used at intake.

Opening a contract now shows its leading concern, why it may matter, the incoming and applicable reference wording, and **Record decision** before the deeper tools. Other material findings remain listed below. **Full document**, **Reference**, **Check coverage** and **Review history** are available after the first comparison. Document details contain the original DOCX, source identity and hashes. The **Help** page links to the optional **Explore** concept; only Legal is a working journey. See the [Issue #10 status](docs/ISSUE_10_STATUS.md) and [architecture decision](docs/decisions/002-legal-pack-and-workspace-boundary.md).

To rehearse from untouched synthetic state without changing an existing review ledger:

```sh
demo_state_dir=$(mktemp -d /tmp/chugchug-review-XXXXXX)
python3 -m chugchug.server --port 8771 --state-dir "$demo_state_dir"
```

Open `http://127.0.0.1:8771/#home`. Use a different port if 8771 is occupied. Keep the generated directory path if you want to revisit that rehearsal; each new `mktemp` directory starts with no recorded decisions.

## Issue #8: reference → review → correction → reuse

1. Open **Reference**. Inspect the bundled fictional NDA or choose an uploaded synthetic reference. The selected reference applies to **new** incoming uploads. Each existing review keeps its original reference identity. Uploaded references must have complete supported DOCX extraction and the bundled mutual NDA clause headings; this is not a general contract-family matcher.
2. Use **Add incoming DOCX** on Home or in the queue. Try [L01](dataset/learning/L01-audit-retention.docx). Open the returned review and inspect the changed Return or Destruction passage beside the reference. The original DOCX and exact extracted text are available from the review.
3. Open **View history** from an original scenario such as Brookside AI / T02. The drawer shows the actual number of fictional records searched, why each was retrieved and whether its wording is exact, similar or merely the same topic. **Inspect original passage** opens the complete historical extraction and exact historical DOCX; the prior decision remains a whole-contract decision.
4. On L01's changed finding, expand **Improve this comparison**. Record a fictional reviewer correction explaining that retained archives are limited to a named regulatory duty and unavailable for business use. This correction is separate from the legal decision and initially appears only in Review history.
5. In **Review history → Comparison corrections**, explicitly share the lesson with fictional context and reuse limits. Upload [L03](dataset/learning/L03-regulatory-records.docx) and [L02](dataset/learning/L02-analytics-retention.docx). Both can surface the authorised correction beside their changed clause. L03 uses different words for a related restricted archive; L02 permits commercial analytics access. In both, applicability remains **unverified** and the independent review route stays **Needs judgement**. Withdraw the lesson from L01's history to remove it from later active retrieval while retaining its audit trail.

The A/B/C check proves a governed retrieval path and a useful caution on the misleading variant. It does **not** prove that the comparison itself improved semantically, that a reviewer saved time, or that the legal interpretation is correct. The optional AI adapter remains disabled by default; no live model run was made for Issue #8. See [Issue #8 status](docs/ISSUE_08_STATUS.md).

The Python package (`chugchug`), `CHUGCHUG_AI_*` configuration names and `.chugchug-data/` state path now match the reviewer-facing **ChugChug** name. The GitHub repository URL still uses its original slug.

## Five-minute walkthrough

1. **Home → Start reviewing:** The live counts show the pending review mix. Choose a category to see only contracts awaiting a decision, or use Start reviewing for the next task.
2. **Falcon Data / T03:** The first view pairs the added commercial-exploitation wording with the applicable reference no-licence protection. Follow **View in full text** to the exact passages. Inspect the other findings and the related rejected historical case. **Document details and original files** contains the source identifiers and original DOCX.
3. **Elm Studio / T04 and Moorland / T05:** One lacks the no-licence protection; the other has a Schedule 1 that overrides permitted use. Both must remain escalations despite otherwise familiar wording.
4. **Brookside AI / T02:** See the five-year term change and H02's conditional acceptance. The previous decision is context, not reusable authority.
5. **Orchard Research / T06 and Birchbridge / T01:** A paraphrase needs interpretation; the template-like document is only a routine *candidate* because a person must still confirm the parties and purpose.
6. **Check coverage:** Open **Check coverage** on T03. It separates source identity, extraction, comparison, independent indicators and human status. Expand “Scope, evidence and limits” to see what each check actually covered.
7. **Human decision:** Choose **Record decision** from the first review view. Mark findings actually considered, enter a reviewer label, choose an outcome and give a reason. Open **Review history**, refresh the browser and see the append-only event tied to the exact document hash. Return to the filtered queue for the next task.

## Five-minute learning-cycle walkthrough

Use a fresh local state directory for this separate synthetic journey, for example `python3 -m chugchug.server --port 8771 --state-dir /tmp/chugchug-learning-demo`. Upload [L01](dataset/learning/L01-audit-retention.docx) and [L02](dataset/learning/L02-analytics-retention.docx) with **Add DOCX**.

1. Open Maple Metrics (L01). Mark its changed return/destruction finding as considered. Record a human decision, rationale and the condition that the retained archive must serve a named regulatory duty with compliance-only access.
2. In **Decision history**, expand **Share this decision as a precedent**. Confirm the exact source passage, enter the commercial context and reuse limits, and name the demonstration publisher. The local identity claim is self-attested; it is not a production permission check.
3. Open Harbour Analytics (L02). The new case appears beside its changed clause with its source, rationale, conditions and context. L02 remains **Needs judgement**: its commercial-team analytics use is different and requires a separate human decision. **View source in full text** returns to the published source passage.
4. Return to L01 and withdraw the publication in Decision history. L02 no longer retrieves it as active context; L01 retains the publication and withdrawal trail. Refresh the browser to confirm persistence.

See [learning-cycle status](docs/LEARNING_LOOP_STATUS.md) for test evidence and limits. This demonstrates governed workflow plumbing, not legal accuracy or measured productivity benefit.

## What the system does

Conventional software preserves and hashes source bytes, accounts for DOCX body paragraphs, table cells, headers and footers, compares clause text and omissions, checks the whole document for broad rights/overrides, ranks context from the five historical decisions, and persists human review events. Every material finding has a source anchor or an explicit reference anchor for a missing provision. Unsupported or unaccounted content blocks extraction and therefore blocks a routine route.

The one AI capability is an **optional, real provider integration** for explaining the possible effect of a selected changed clause against the reference. The lexical baseline already finds the change and routes it to a person; the model may help a reviewer interpret a paraphrase. It never changes the route or makes a final decision. The interface says when AI has not run. This environment made **no live paid API call**, so model quality and live-provider behaviour are unverified. Mocked adapter tests only verify schema, citations, caps and failure handling. See [Decision 001](docs/decisions/001-scoped-semantic-comparison.md).

To enable later, supply `OPENAI_API_KEY`, set `CHUGCHUG_AI_ENABLED=1`, `CHUGCHUG_AI_MODEL` (defaults to `gpt-4o-mini`), positive `CHUGCHUG_AI_SESSION_CAP`, `CHUGCHUG_AI_DOCUMENT_CAP`, `CHUGCHUG_AI_MAX_OUTPUT_TOKENS`, and `CHUGCHUG_AI_MAX_INPUT_CHARS` before starting the app. The last setting is a conservative input-size cap, not a token count. The UI then offers a per-change action and asks before sending the selected **synthetic** passages to OpenAI. Calls may incur charges. No key is stored in this repository. Do not use this mode with real or confidential contracts.

## Verify

```sh
python3 -m unittest discover -s tests -v
python3 -m tests.evaluate
node --check web/app.js
node --test tests/test_web_ui.mjs
git diff --check
```

The evaluator alone reads the held-out answer key. Runtime modules never access it. The current synthetic route result is 6/6, including the three mandatory escalations. These cases do not establish accuracy or safety on real agreements. The [missed-exception audit](docs/MISSED_EXCEPTION_AUDIT.md) records 16 separate adversarial documents, exact original/current outcomes and remaining risks. Browser QA and limitations are recorded in [Sprint 01 status](docs/SPRINT_01_STATUS.md) and [Sprint 02 status](docs/SPRINT_02_STATUS.md).

## Known limits

- This is a local single-reviewer demonstration. There is no authentication, shared workflow, real-contract privacy review or production storage model.
- The document parser conservatively blocks unfamiliar Word structures. It does not support OCR, nested tables, tracked changes, footnotes, embedded objects or every DOCX feature. Full source bytes are available for manual inspection.
- Structural matching assumes this mutual NDA clause family. Lexical controls are indicators, not a comprehensive legal risk model. A routine candidate means checks completed within that scope, not legal safety.
- Precedent ranking is lexical and contextual. It does not infer policy or transfer conditional acceptance.
- Demo publication requires explicit action and a source-linked considered finding, but publisher identity is self-attested. There is no multi-user access control or legally authorised playbook.
- AI live quality, latency, provider errors and cost remain unverified until an authorised paid test. No synthetic time savings or legal-team productivity study is claimed.
- Human creative acceptance and submission QA are pending. Do not submit this ZIP as a final employer response without review.

## What comes next

The **working prototype** is the offline synthetic review journey, assurance view, decision history and explicit demo precedent publication/withdrawal. **Before real use**, legal reviewers must validate the experience and legal assumptions, and the team needs privacy, security, identity and publication controls. **Possible later work** includes authorised playbooks, retrieval feedback, other contract families and document formats. Those are product options, not unfinished application requirements. See [Product direction](docs/PRODUCT_DIRECTION.md).
