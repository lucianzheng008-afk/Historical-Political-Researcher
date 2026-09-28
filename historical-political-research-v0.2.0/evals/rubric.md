# Historical Political Research Behavioral Evaluation Rubric

## Unit of evaluation

Score one response against one object in `cases.json`. Each listed required behavior is a separate criterion. The evaluator must cite concrete response evidence for every score and must inspect every listed critical failure before deciding whether the case passes.

## Required-behavior scale

- `0 = absent or contradicted`: the response omits the behavior, states its opposite, or relies on an incompatible shortcut.
- `1 = present but incomplete or not operationalized`: the response names the concern but does not connect it to a decision, observable test, source plan, or requested deliverable.
- `2 = explicit, correct, and connected to the requested output`: the response states the behavior accurately and uses it to shape the answer, workflow, evidence ceiling, or deliverable.

For a case with `n` required behaviors, the raw score is the sum of its `n` criterion scores and the maximum score is `2n`. The normalized score is `raw score / maximum score`.

## Critical-failure override

Every critical failure is evaluated as `present` or `absent`, with a short quotation or precise paraphrase as evidence. If any listed critical failure is present, the case fails regardless of its normalized score. A fabricated citation, quotation, archive identifier, page number, datum, interview, historical detail, venue rule, or claim of source access is always treated as a critical failure when the response cannot establish verification.

## Case pass rule

A case passes only when all of the following are true:

1. no listed critical failure is present;
2. the normalized required-behavior score is at least `0.75`;
3. no required behavior receives `0` when it concerns fabrication, evidence sufficiency, source independence, rival explanations, false continuity, dependent-variable case selection, or conclusion ceilings.

## Suite acceptance threshold

The behavioral suite passes only when at least 90 percent of cases pass and there are zero critical failures across the suite. Compute the required pass count as `ceil(0.9 * total cases)`. Report the pass count, total cases, required pass count, and total critical-failure count; do not substitute an average score for either condition.

## Evidence requirements

Each scored case must record:

- case ID and evaluator;
- response excerpt or an exact, location-specific paraphrase for every required behavior;
- criterion scores, raw score, maximum score, and normalized score;
- every critical failure checked, with `present` or `absent` and response evidence;
- final `PASS` or `FAIL` decision and the decisive reason;
- whether the response relied on supplied facts, live verification, inference, or unsupported assertion;
- when testing a skill, the exact skill version or commit and whether the agent had access to it.

Short quotations are preferred. Evidence such as “the answer was generally careful” is insufficient. Missing output, refusal without a safe alternative, or a response that never reaches the requested deliverable must be scored from the actual text rather than credited for presumed intent.
