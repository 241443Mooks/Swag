# Independent test strategy

## Test separation
- Runtime may use only `dataset/reference/`, `dataset/historical/`, `dataset/review_records/` and selected `dataset/incoming/` files.
- `dataset/ground_truth/` is evaluation-only. Keep evaluator imports, paths and outputs separate from runtime modules.
- Tests should exercise public interfaces or documented contracts rather than reimplementing the same rules they purport to test.
- Do not hardcode T01–T06 IDs, expected outcomes or hidden answer-key strings into application logic or prompts.

## Technology choice tests
For each selected AI capability, compare it with a non-AI baseline on representative and adversarial inputs. Record quality, latency, model calls/cost when measured, failure behaviour and reviewer effort where measurable. Do not assert AI is superior without evidence. Keep conventional solutions where they perform as well or better.

## Test layers
1. **Unit:** DOCX extraction, structural coverage, hashes, clause alignment, differences, anchors, decision event persistence, route precedence, schema validation.
2. **Integration:** reference + historical decisions + incoming document produces source-linked findings and review route. All six baseline cases required.
3. **Adversarial mutations:** generate new test documents independent of the baseline six: remove/rename/renumber a clause, bury a risky term in a schedule or table, add a contradictory paragraph, reorder sections, include a prompt-injection instruction, corrupt a DOCX, add unsupported objects, change only party names. Use a fixed random seed where generation is random.
4. **Provider failure:** no key, opt-out, rate limit, timeout, malformed JSON, hallucinated citation, unavailable model, exhausted budget. Verify no invented AI result and safe review routing.
5. **Security/privacy:** no secret in logs/ZIP, no external calls by default, no runtime access to ground truth, contract text cannot issue instructions.
6. **End-to-end:** start from clean checkout, ingest DOCX, inspect original, navigate findings and precedents, record human decision, reload and verify audit history, inspect queue.
7. **Evaluation:** run independent outputs first, then compare with held-out `expected_findings.csv`. Report per-case routes and evidence, including failures. Do not train/tune on answer key as though it were unseen validation.

## Required release assertions
- T03, T04 and T05 must each escalate for the intended reason; their absence is a hard failure.
- T01 may be a routine **candidate**, never an automated approval.
- T02 and T06 require review or more restrictive route, with relevant change/uncertainty shown.
- No extraction failure, unsupported content or failed required AI check may silently lead to routine routing.
- Every finding has an authentic source span or a clearly defined missing-clause comparison anchor.
- Precedent context and decision status are visible; no blanket authorisation is inferred.
- Human final decisions are append-only and linked to document hash.

## Evidence recording
For each gate report commands, environment, versions, pass/fail counts, notable failures and whether tests were mocked, deterministic, or used a real model. Record model name and actual cost/usage only if measured. If browser walkthrough cannot be performed, state that it is unverified.

## Prevent test gaming
Do not modify ground truth or source contracts to make tests pass. Do not delete failing tests or turn assertions into snapshots of current output. Add regression tests for every bug fixed. Keep known failures visible.
