# Swig reviewer journey — reversible design proposal

These are implementation wireframes for Issue #8, not owner creative acceptance. The existing contract checks and human authority remain unchanged.

## Desktop, first visit

```text
Swig                         Home   Review queue   Reference   Help
─────────────────────────────────────────────────────────────────
Your contract review, in order
Six fictional NDAs are ready. Swig compares each with the named
reference and points you to wording that needs a human decision.

3 closer review     2 judgement     1 routine candidate

[Start reviewing]   [Add incoming DOCX]

Reference: bundled mutual NDA · exact source identity available
What Swig cannot decide → Help
```

The counts are derived from the queue, never hardcoded. Returning users can use the persistent Review queue link without passing through instructions.

## Review and evidence

```text
Home   Review queue   Reference   Help
─────────────────────────────────────────────────────────────────
Queue / Falcon Data                     Reference: bundled NDA · hash
┌───────────────┐ ┌─────────────────────────────────────────────┐
│ Falcon        │ │ Swig noticed a possible broader right      │
│ Elm           │ │ Escalate · human judgement required         │
│ Moorland      │ │ Wording may preserve commercial use.        │
│ Brookside     │ │ [Compare wording] [Record decision]         │
│ Orchard       │ │                                             │
│ Birchbridge   │ │ Findings to inspect                         │
└───────────────┘ │ 1. Broader rights · view evidence             │
                  │ 2. Possible override · view evidence        │
                  │ 3. No Obligation changed · view evidence    │
                  │                                             │
                  │ Similar past decisions · [View history]     │
                  │ [Something Swig missed?]                    │
                  │ [What was checked]  [Full text]              │
                  └─────────────────────────────────────────────┘
```

Opening a finding shows incoming and exact reference wording side by side. If a finding is an independent whole-document flag, say no direct reference pair exists. Source and reference links open the exact passage; Back returns to the same review and finding. The history panel is secondary and opens on demand, with contract-level outcomes explicitly labelled.

## Reference and intake

```text
Reference NDA
Current: bundled sample · filename · SHA-256 · complete extraction
[Use bundled sample] [Choose synthetic reference DOCX]
Selecting a reference affects new incoming uploads only. Existing
reviews keep the version used when the document entered the queue.

Add incoming DOCX → Validate source → Bind current reference →
Compare/route → Queue. Errors name the unsupported content or
structural limit; no incomplete analysis receives a routine route.
```

## Help and smaller screens

Help is a short, optional explanation of route labels, comparison scope, precedent limits, AI status and human authority. On smaller screens the queue becomes a full-width list above the review, evidence columns stack, and the history panel occupies the available width. Controls remain usable with keyboard and touch; no hover-only meaning or mandatory tour.

## Content rules

- One short observation and route at the top. Distinct material findings remain visible as a list.
- Verbatim wording is labelled **Incoming document** or **Reference**. Explanations are Swig commentary.
- Check details, source IDs and full audit events are available deliberately, without crowding the default view.
- “Looks routine” is a queue priority, never legal approval. An untested or failed check remains visible.
- Past decisions are about whole contracts unless a reviewed source passage is explicitly linked. Similarity does not authorise reuse.
