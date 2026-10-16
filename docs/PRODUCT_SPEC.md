# CHUG — Product Specification

**Capture. Hold. Use. Grow.**

*An enduring organisational knowledge foundation.*

**Status:** Working prototype specification. The first implementation explores commercial contract review using fictional documents. The wider organisational knowledge foundation remains a developing product direction.

## Purpose and scope

Chug explores how organisations can preserve, connect and reuse knowledge created through everyday work.

The first practical experiment focuses on commercial contract review.

A small in-house legal team may receive a substantial volume of relatively standard agreements. Many contain familiar wording or amendments that resemble something considered previously.

Reviewing these documents can involve repetitive comparison, searching for previous decisions, identifying exceptions and reconstructing the context behind earlier judgements.

The opportunity is to reduce unnecessary effort while making important differences, supporting evidence and relevant organisational experience easier to find and understand.

The prototype explores two connected questions:

1. **Can we make the immediate task easier?** Use conventional software to identify changes, organise evidence, surface potential concerns and help reviewers focus their attention.
2. **Can today's work help with future work?** Preserve decisions, their supporting evidence, reasoning and context so that relevant experience can be found and considered again.

The first implementation focuses on synthetic mutual non-disclosure agreements (NDAs). Research and development into other contract families are separate from the completed reviewer journey.

Chug is a decision-support experiment, not a legal advice service or automatic contract approval system.

The wider ambition is to explore whether similar approaches to capturing, connecting and reusing knowledge could benefit other organisational activities.

**The legal review experience is the first implementation. The organisational knowledge foundation is the longer-term direction.**

## Intended user and core workflow

The first implementation is designed around the needs of a legal professional reviewing incoming commercial contracts.

A reviewer needs to understand:

- What has changed?
- What is missing or different from the reference?
- Why might those differences matter?
- Has something similar been considered before?
- What was decided previously, and under which conditions?
- What still requires my judgement?

Chug should bring this information together within the review process, without requiring someone to reconstruct the evidence from multiple places.

### The working review journey

The current local prototype supports the following experience using fictional mutual NDAs:

1. **Organise the work.** Present a queue of contracts grouped by the attention they may require, allowing a reviewer to focus on exceptions.

2. **Preserve the source.** Retain the original document and its identity, including a cryptographic hash, so findings and decisions can be traced to the material actually reviewed.

3. **Understand document coverage.** Extract supported document content and identify limitations. Incomplete or unsupported extraction must not produce a reassuring routine recommendation.

4. **Identify differences.** Compare an incoming document against its associated reference, identifying changes, additions and missing provisions within the supported comparison scope.

5. **Check for important exceptions.** Apply independent, rule-based checks for selected potentially consequential wording, including terms that might otherwise be overlooked in a largely familiar document.

6. **Recover relevant experience.** Retrieve potentially related historical decisions and show their source evidence, reasoning, context and limitations. Similarity does not establish applicability.

7. **Support human judgement.** Present the findings, explanation and supporting evidence so the reviewer can inspect, challenge and decide what action to take.

8. **Record the outcome.** Allow a person to record their decision, reasoning and the findings considered, preserving an auditable record connected to the original document.

9. **Enable deliberate reuse.** Allow selected decisions or corrections to be explicitly shared for future retrieval, with context and limitations. Published material can also be withdrawn.

### What this does not establish

The prototype does not interpret every possible contractual issue, guarantee legal completeness or determine whether an agreement is safe to sign.

Its comparisons, checks and historical retrieval are bounded technical capabilities, not substitutes for professional review.

The current working journey centres on synthetic mutual NDAs. Additional contract families, wider reference selection and more advanced interpretation remain separate areas of development and validation.

**The intended experience is simple: Chug does the mechanical work it can perform reliably, brings relevant evidence and previous experience into view, and leaves professional judgement with the reviewer.**

## Review routes and safeguards

Chug uses programmatic checks to help organise incoming contracts according to the attention they may need.

The purpose of these recommendations is to support a proportionate review process, not to determine whether a contract is legally acceptable.

### Review routes

The current prototype uses four routes:

**Looks routine — `routine_candidate`**

The supported checks have completed without identifying material differences or concerns requiring a more restrictive route.

A person must still confirm that the agreement is appropriate, including its parties, purpose and relevant circumstances.

**Needs judgement — `review_required`**

Differences, uncertainty or contextual considerations require a person's interpretation.

A previous decision may provide useful context, but cannot automatically determine the outcome.

**Needs closer review — `escalate`**

Potentially consequential wording, missing protections, conflicting provisions or other identified concerns require particular attention.

Chug should make the concern and its supporting evidence readily available.

**Analysis blocked — `blocked_extraction`**

The document could not be processed or accounted for sufficiently to support a reliable comparison.

The limitation must be visible, and Chug must not recommend a routine review based on incomplete evidence.

### Essential safeguards

The review process must preserve the following protections:

- **Document coverage:** Account for supported document structures, including paragraphs, tables, headers, footers and schedules. Where content cannot be reliably processed, prevent routine routing.
- **Independent checks:** Examine selected potentially consequential patterns separately from the main document comparison, so familiar wording or high overall similarity cannot conceal identified concerns.
- **Missing information:** Identify omissions and additions, not simply differences between passages that happen to align.
- **Source traceability:** Connect findings to the original document and applicable reference, with the supporting evidence available for inspection.
- **Conservative routing:** Where multiple findings affect a document, the more restrictive applicable recommendation takes precedence.
- **Contextual precedent:** Do not transfer historical decisions or their conditions to a new agreement without human consideration.
- **Human authority:** No automated route constitutes approval. A person remains responsible for the final decision and its rationale.
- **Transparent uncertainty:** Clearly communicate unsupported content, incomplete checks and limitations that affect confidence in the recommendation.

### Boundaries of these safeguards

The current checks cover selected document structures, contractual patterns and comparison scenarios.

They are not a comprehensive legal ruleset and cannot guarantee the detection of every material issue, contradiction or unusual drafting technique.

A successful technical check establishes only that the particular check completed within its defined scope.

The effectiveness of the review routes and safeguards still requires qualified legal validation and evaluation in realistic working conditions.

**Chug should help people focus their attention without concealing uncertainty or creating confidence that the evidence does not justify.**

## Evidence, decisions and knowledge reuse

Chug should preserve enough information about a piece of work to make its evidence, decisions and relevant context understandable and useful again.

The underlying principle is to maintain reliable connections between information, rather than simply accumulate records.

### Evidence and source identity

In the current contract-review prototype, Chug preserves:

- **Documents:** Original files, identifiers, cryptographic hashes and extracted content.
- **References:** The reference document associated with a review, including its identity and relevant passages.
- **Findings:** Identified differences, potential concerns, explanations, uncertainty and links to supporting evidence.
- **Decisions:** The outcome recorded by a person, their reasoning, the findings considered and the document to which the decision relates.
- **Historical context:** Previous decisions, relevant passages, recorded conditions and limitations.
- **Changes:** Corrections, explicit publication of selected information and subsequent withdrawals.

These connections allow someone to inspect not only what Chug has identified, but also the evidence and history behind it.

### Preserving the meaning of decisions

A decision is not simply an outcome.

Its usefulness may depend on who made it, what was considered, the circumstances involved, when it was made and why.

Chug should preserve that context wherever it is available, without inventing missing information or creating unnecessary administrative work.

A previous decision is evidence of what happened in a particular situation. It does not automatically establish what should happen in another.

The prototype therefore distinguishes between recording a decision and deliberately making it available for future retrieval.

### Making previous experience useful

Chug can retrieve potentially relevant historical information when similar wording arises.

The current approach uses conventional lexical and contextual matching rather than an AI knowledge graph or semantic retrieval system.

Retrieved information remains connected to its original evidence, reasoning and limitations.

A reviewer determines whether the earlier experience is relevant and applicable.

Corrections and published information can also be withdrawn so that they are no longer presented as active reusable guidance, while retaining an appropriate historical record.

### Beyond the first implementation

The wider architectural ambition is to maintain a reliable map of knowledge across organisational systems.

That map could connect people, records, events, decisions, processes and their relationships using the foundational questions:

**Who, What, Where, When and Why?**

Where possible, original information should remain in the system responsible for it.

Chug would maintain the references, context, relationships and history needed to make that information accessible and useful, subject to appropriate permissions and authority.

This wider cross-system knowledge foundation is **proposed architecture, not a capability already implemented in the prototype**.

**The aim is not simply to remember more. It is to preserve enough context and connection for accumulated knowledge to become genuinely useful.**

## Interface and user experience

Chug should make complex information easier to work with, rather than introduce another layer of complexity.

The experience should be shaped around what someone is trying to achieve, what information they need and the decisions they are responsible for making.

**Simple on the surface. Reliable and robust underneath.**

### The reviewer experience

The first contract-review interface should help someone answer four questions:

1. **What has changed?** Present the most important differences and concerns clearly.
2. **Why might it matter?** Explain the potential significance and any uncertainty without presenting suggestions as legal conclusions.
3. **What does the evidence show?** Make original wording, reference material, previous decisions and supporting checks easy to inspect.
4. **What should I do next?** Make the available actions clear, including recording a decision, requesting further review or examining additional evidence.

The reviewer should not need to navigate extensive technical information before understanding the task.

Detailed evidence, source identity, technical checks and history must remain accessible without dominating the initial experience.

### Design expectations

The interface should be:

- **Clear:** Use familiar language and make the next action easy to identify.
- **Calm:** Prioritise the information that matters, using progressive disclosure rather than overwhelming people with every detail.
- **Accessible:** Support readable layouts, keyboard interaction, clear focus states and meaningful labels.
- **Responsive:** Work comfortably across appropriate screen sizes without losing essential information or functionality.
- **Transparent:** Distinguish source facts, system findings, previous decisions, uncertainty and human conclusions.
- **Consistent:** Use predictable navigation, terminology, interactions and feedback.
- **Forgiving:** Allow people to revisit evidence, correct information and understand the consequences of their actions.

### Designing with the people doing the work

The current interface is an early implementation, not a final design.

I want to develop the experience collaboratively with the people who would use it.

That means understanding their workflow, observing where unnecessary effort occurs, introducing small improvements and testing whether those changes genuinely help.

The interface may change substantially as we learn.

For some future applications, a dedicated Chug interface may be appropriate. Others may work better through existing organisational systems.

The underlying knowledge foundation should support different experiences without requiring everyone to work in the same way.

### Evaluation and acceptance

The reviewer experience should be assessed through practical tasks, not appearance alone.

I want to understand whether people can:

- Recognise what needs their attention.
- Find and understand the relevant evidence.
- Identify uncertainty and challenge suggestions.
- Make and record decisions without unnecessary steps.
- Recover useful previous experience when it matters.
- Complete their work without additional cognitive or administrative burden.

The current prototype's usability and accessibility remain under review. Design intentions and automated interface checks do not establish user acceptance.

**The measure of a successful interface is not how much information it displays, but how effectively it helps someone do their work.**

## Architecture and implementation boundaries

Chug should use the simplest reliable technology that meets the needs of the work.

The architecture should support trustworthy information, clear relationships, useful retrieval and human decision-making without introducing unnecessary technical complexity.

Technology choices should follow the problem being solved, rather than determine what the product becomes.

### Working implementation

The current local prototype is a Python application with a browser-based interface.

It uses conventional software for document extraction, comparison, source identity, independent checks, review routing, historical retrieval and recording decisions.

The application can operate offline without external services or AI credentials.

The core components are designed to be testable independently, with clear evidence and failure handling.

The publicly packaged demonstration provides read-only access to selected fictional review data. State-changing actions require the local application.

### Capabilities under development or evaluation

Several capabilities are being explored beyond the initial mutual NDA workflow.

These include broader reference management, contextual matching and comparison of additional commercial contract families.

Some technical components have been developed separately from the user interface. They should not be described as completed user-facing functionality until they have been integrated, tested and accepted.

The prototype also includes an optional OpenAI Responses API integration for explaining selected changed wording.

This integration is disabled by default. Its additional usefulness, legal accuracy, latency and operating costs have not been validated through live provider evaluation.

### Future architectural possibilities

The longer-term knowledge foundation could connect information held across different organisational systems.

Potential capabilities include:

- Reliable references to existing records and their sources.
- Relationships between people, events, documents, decisions and processes.
- Mechanisms for identifying changed, outdated or unavailable information.
- Contextual retrieval through conventional, semantic or hybrid search.
- AI-assisted identification of potentially useful connections.
- Source-grounded explanations that help people understand relevant information.
- Governed feedback, correction, publication and withdrawal.

These are possibilities to investigate, not an agreed implementation roadmap.

They do not require a particular database, AI model, interface or technology stack to be selected in advance.

### Architectural safeguards

Any development must preserve clear boundaries between:

- Original information and derived interpretations.
- Established relationships and suggested connections.
- Recorded decisions and approved organisational guidance.
- System recommendations and human authority.
- Recorded feedback, updates to searchable knowledge and training an AI model.

Information should remain traceable to its source, with uncertainty and limitations visible.

Where possible, Chug should work with information in existing systems rather than create unnecessary copies.

Future integrations must respect permissions, confidentiality, retention requirements and the authority of the systems responsible for the original information.

**The architecture should remain adaptable. Its purpose is to make organisational knowledge more useful, not to commit the organisation to a particular technology.**

## Validation, evaluation and acceptance

Chug's development should be guided by evidence of what works, what people find useful and what can be relied upon.

Technical functionality, user experience, professional validity and organisational value are different things. Each needs an appropriate form of evaluation.

### Technical verification

The working prototype should be tested to establish that its implemented functions behave as intended.

This includes:

- Reliable processing of supported documents and preservation of original evidence.
- Correct handling of document differences, omissions and independent checks.
- Conservative routing when information is incomplete or potentially consequential.
- Source-linked findings and access to supporting evidence.
- Recording, retrieval, correction, publication and withdrawal of decisions.
- Predictable handling of errors and unsupported situations.
- Reproducible operation from a clean copy of the application.

Automated tests should cover expected behaviour, edge cases and deliberately challenging examples.

Passing these tests establishes confidence in the specific technical behaviours tested. It does not establish legal correctness or real-world effectiveness.

### User experience and usefulness

The next question is whether the application genuinely helps someone do their work.

I want to evaluate the experience through practical tasks, observing whether people can understand the information, identify what matters, access evidence and complete their decisions without unnecessary effort.

Where possible, I would compare the experience against how the same work is currently performed.

Measures might include time spent reviewing, unnecessary steps, repeated searches, missed information and the effort required to reach a supported decision.

Qualitative feedback is equally important. People should be able to explain what helps, what creates friction and what they would change.

These benefits have not yet been established through representative user evaluation.

### Knowledge reuse

The wider proposition needs its own evaluation.

I want to establish whether knowledge created through one piece of work can be found, understood and usefully applied to another.

That includes testing whether:

- Relevant previous experience can be recovered.
- Its original evidence, reasoning and conditions remain understandable.
- Misleading similarities and differences in context are made visible.
- Incorrect or outdated information can be challenged and withdrawn.
- Capturing reusable knowledge introduces little or no unnecessary administration.

The aim is to demonstrate that accumulated organisational experience becomes genuinely more useful, not simply that the system stores more records.

### Professional and operational validation

Before Chug could be used with real legal work, appropriately qualified people would need to validate its assumptions, safeguards and limitations.

Real organisational deployment would also require privacy, security, access-control, retention, accountability and operational assessments.

These are separate from demonstrating a working prototype and should not be represented as completed.

### Acceptance of the current demonstration

The immediate goal is a coherent, runnable and honestly described proof of concept.

Before submission, the final version should have:

- Completed technical checks against the exact submitted code.
- A working, understandable reviewer journey.
- A demonstrated decision and knowledge-reuse cycle.
- Documented limitations and unresolved concerns.
- Recorded owner feedback and acceptance, or clearly stated reservations.
- A verified submission package that works when extracted into a fresh environment.

The read-only web demonstration provides an additional way to explore Chug, but does not replace verification of the interactive local application.

**A completed demonstration is not a validated production product.**

The purpose of this stage is to show what has been built, explain the thinking behind it, demonstrate the technical mechanisms and identify what would be worth exploring with a real team.

**Progress should be determined by reliable evidence, meaningful human feedback and demonstrated usefulness — not simply by the number of features completed.**

## Scope, non-goals and future development

Chug is an evolving exploration, but each stage of development should have a clear and achievable scope.

The current demonstration is intended to establish a credible starting point, not deliver a complete organisational knowledge platform.

### Current prototype

The first implementation focuses on:

- Synthetic commercial contract review, primarily mutual NDAs.
- Programmatic document comparison, exception identification and supporting evidence.
- Conservative review recommendations and human decisions.
- Retrieval of relevant previous experience, with its context and limitations.
- Recording decisions and corrections, with deliberate publication and withdrawal.
- A working local application and a separate read-only web demonstration.

The optional AI integration remains an experimental capability whose additional value has not been established.

### What is outside the current scope

The prototype is not intended to provide:

- Comprehensive legal analysis or guaranteed identification of contractual risks.
- Automatic approval, negotiation or legally authoritative decisions.
- Production processing of confidential or real organisational information.
- Enterprise authentication, multi-user permissions or production-grade information governance.
- Support for every contract type, document format or commercial scenario.
- A live cross-system organisational knowledge map.
- An implemented RAG platform, knowledge graph or continuously trained AI model.

These are boundaries of the present experiment, not necessarily permanent limitations on what Chug could become.

### How future development should be determined

I don't want to define a large feature roadmap before understanding what people actually need.

The next stage should begin with the organisation's existing work, systems, information and expertise.

Together, we can identify where unnecessary effort occurs, where useful knowledge becomes difficult to recover and what opportunities are worth exploring.

Some improvements may require only a straightforward change to an existing process. Others might involve better retrieval, new connections between information, a dedicated interface or a carefully selected AI capability.

Each possibility should be considered according to its usefulness, reliability, cost, risks and fit with the people doing the work.

**Build what is useful. Test it. Learn from it. Improve it. Then decide what comes next.**

### The longer-term ambition

Chug's potential extends beyond commercial contracts.

The underlying idea is that work naturally creates knowledge, and that organisations should be able to preserve and benefit from it without creating unnecessary additional administration.

The product, interface and technology may evolve considerably.

What should remain consistent is the purpose:

**Help people make better use of what their organisation already knows, while allowing the knowledge created through today's work to make tomorrow's work easier.**
