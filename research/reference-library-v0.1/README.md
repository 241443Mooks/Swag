# ChugChug — synthetic reference-library research (v0.1)

**Status: research fixtures, not supported by the running application, and not legally approved.**

This directory contains **8 synthetic reference documents and 4 incoming test documents**, along with a proposed dataset for exploring intelligent matching of incoming agreements to the *applicable* reference, not merely the most textually similar one. It supplements GitHub issue [#16](https://github.com/241443Mooks/Swag/issues/16).

## Candidate standards

**NDA (3):**
- Mutual NDA — Product evaluation (UK) (`NDA-UK-EVAL`)
- Mutual NDA — Supplier assessment (UK) (`NDA-UK-SUPPLIER`)
- One-way NDA — Customer disclosures (UK) (`NDA-UK-ONEWAY`)

**Customer order (5):**
- Customer Order — Desktop user licences (direct) (`ORDER-PRO-DIRECT`)
- Customer Order — Managed cloud scanning (`ORDER-DAST-CLOUD`)
- Customer Order — Self-hosted scanning (`ORDER-DAST-SELF`)
- Customer Order — Desktop plus cloud bundle (`ORDER-COMBINED`)
- Customer Order — Reseller desktop licences (`ORDER-RESELLER`)

## Incoming cases (4)

- `IN-01`: Evaluation NDA with longer, broader archival use → evaluation NDA candidate; material retention/use concerns
- `IN-02`: Managed cloud scanning order with different hosting region → hosted/cloud reference; region variation requires review
- `IN-03`: Desktop reseller seat increase → reseller desktop reference; quantities and entitlements must be checked
- `IN-04`: Reseller request for hosted/cloud scanning → **no appropriate approved reference** within this candidate set; abstain rather than substitute direct-cloud or desktop-reseller wording

## Applicability before textual similarity

Suggested metadata: reference ID, display name, family, variant, product, deployment, direct/reseller channel, disclosure direction, jurisdiction, version/effective dates, human approval status, provenance/hash, companion terms, known exclusions and escalation requirements.

Proposed processing sequence:
1. Retain original bytes and evidence anchors.
2. Identify family and transaction context from evidence; ask for missing facts.
3. Hard-exclude the wrong family, model, channel or direction.
4. Rank remaining candidates, showing reasons, gaps and uncertainty.
5. Escalate/abstain if no appropriate candidate exists.
6. Require an authorised reviewer to confirm applicability; immutably bind the chosen baseline version/hash to this review.
7. Compare exact wording, run independent safeguards and record the **human** legal decision.

AI may assist with classification, explanation or ranking but must not silently approve, publish standards or override a hard exclusion.

## Boundaries and caveats

- Inspired by common software-company transactions and public product categories only; **not PortSwigger's internal legal templates or approved policy**.
- All parties, prices and terms are invented for demonstration.
- The active ChugChug code supports one mutual-NDA heading family, not these extra agreements or automatic reference matching.
- Do not place these files into `dataset/reference/`, `dataset/incoming/` or runtime precedent search without separate architecture, legal, security and evaluation work.
- The 12 `.docx` documents under this folder are compact, regenerated Word specimens preserving the synthetic clause wording and key variations from the original starter set. **They are not byte-for-byte copies** of the separately supplied starter ZIP; formatting and ancillary metadata differ. Keep them research-only and revalidate them before test automation or legal review.

The key test is not merely finding something similar: it is **knowing when not to match**.
