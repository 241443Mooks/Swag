# AI architecture and evidence

## Product position

PortSwigger asks how AI **could help** a small legal team with repetitive commercial contracts. The brief does not require a live paid model call. Swig's current offline journey is useful without AI: deterministic extraction, comparison, independent checks, routing, lexical precedent retrieval and human decisions carry the workflow. AI should be retained or expanded only if it provides a worthwhile advantage over that conventional baseline, considering errors, confidentiality, latency, cost and maintenance.

## Current optional capability

`swag/ai.py` integrates the OpenAI Responses API for one narrow task: explaining the possible effect and uncertainty of a **selected changed clause** against its reference wording. It is disabled by default. A user must configure a key and call/output caps, then invoke the action on a synthetic passage. The model cannot change the route, repair failed extraction, publish a precedent or approve a contract. This is not a whole-document contradiction detector or a required safeguard.

The adapter sends only the selected source and reference passages, treats them as untrusted data, requests structured output, validates the response and supplied source anchors, and labels a successful provider response with provider, model and timestamp. Failure is shown as unavailable; it never becomes a silent positive check. The UI distinguishes “not run” from a completed model response.

The lexical/deterministic baseline already identifies and routes the changed passage to a person. Model interpretation might help with paraphrases or unfamiliar wording, but **incremental usefulness has not been measured**. No live paid provider call has been made in this environment. Mocked tests verify request handling, response shape, anchor checks and failure handling; they do not establish live model performance or legal accuracy.

## Evaluation before relying on it

With explicit authority to incur a paid call and use synthetic text, run the provider against a separate set of selected changes. Record model/configuration, outputs, errors, latency and cost. Have legal reviewers judge whether explanations improve understanding against the same evidence shown without AI; check for invented effects, misleading certainty and unnecessary effort. Do not tune against the held-out answer key or use model output as a route override. Removing the optional action is appropriate if it fails that comparison.

## Submission boundary

The runnable ZIP should work offline and explain the optional integration honestly. A reviewer supplying their own credentials can reproduce the configured path, but the submission must not include a key, claim a live result that was not observed, or imply that AI is necessary for the routine journey. No real or confidential contracts should be sent to the provider from this prototype.
