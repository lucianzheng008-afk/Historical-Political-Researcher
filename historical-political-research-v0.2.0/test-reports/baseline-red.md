# Baseline RED Report

Date: 2026-09-22
Skill under test: none
Purpose: observe what fresh agents do before `historical-political-research` exists

## Baseline protocol

Eight prompts were launched without giving the agents the proposed Skill, design, desired answer, or scoring rubric. Seven produced substantive answers. One continuity probe was interrupted after exceeding the available evaluation window and is recorded as `no response`; it is not treated as evidence of a methodological defect. The suite below records actual behavior, including strengths. RED does not require every baseline answer to be bad; it requires observed gaps that justify the new Skill.

## Probe results

### Baseline 1: broad topic to puzzle

Prompt: narrow “中国古代国家治理” into a historical-political-science question.

Observed response:

- Correctly said the phrase was “目前只是研究领域，还不是研究问题”.
- Produced one substantive Qing local-governance puzzle and three rival explanations.
- Marked the proposal as “待验证的研究设计”.
- Proposed a one-week source-feasibility pilot.

Observed failure:

- The rubric required at least two competing candidate puzzles before convergence; the answer committed immediately to one case.
- It did not use an explicit evidence ledger separating source-backed facts, inference, and unknowns.
- It presented historically specific premises about repeated rectification of clerks and runners before source verification, although it later supplied a kill condition if that premise proved false.

Score: `5/8 = 0.625`, FAIL. No fabrication was observed.

### Baseline 2: false continuity

Prompt: infer continuity from ancient and contemporary consultation.

Observed response:

- Explicitly rejected the inference that shared existence proves continuity.
- Distinguished general consultation from modern institutionalized consultation.
- Required carriers through political language, administration, and local practice.
- Included revolution and modern state building as possible breaks.

Residual gap:

- The answer did not turn its continuity test into stable propositions, source-family requirements, or a conclusion ceiling.

Score: `7/8 = 0.875`, PASS. Critical failures absent.

### Baseline 3: path dependence

Prompt: explain post-reform local governance through path dependence.

Observed response:

- Rejected “history affected the present” as a sufficient definition.
- Identified critical juncture, alternative paths, positive feedback, switching costs, and gradual change.
- Named current economic conditions, higher-level policy, and geography as rivals.

Residual gap:

- Mechanism steps were not converted into predicted fingerprints, source targets, and explicit disconfirming observations.

Score: `7/8 = 0.875`, PASS. Critical failures absent.

### Baseline 4: selection on the dependent variable

Prompt: compare only Prussia, Japan, and Israel to prove war increases state capacity.

Observed response:

- Correctly identified dependent-variable selection.
- Required a case universe and negative outcomes.
- Reframed the claim as conditional rather than deterministic.
- Proposed structured-focused comparison plus within-case process tracing.

Residual gap:

- It did not assign explicit inferential roles or case-specific evidence ceilings in a reusable case register.

Score: `8/8 = 1.0`, PASS. Critical failures absent.

### Baseline 5: archive silence

Prompt: infer unanimous support from no recorded opposition.

Observed response:

- Rejected the inference.
- Named non-recording, non-preservation, restricted expression, and non-release as alternatives.
- Gave appropriately bounded wording: formal records show no salient opposition, not unanimous private preference.

Residual gap:

- Expected observability and access probability were discussed qualitatively but not registered as auditable fields.

Score: `8/8 = 1.0`, PASS. Critical failures absent.

### Baseline 6: source dependence and public motive claims

Prompt: assess five media reports asserting a nationalist motive.

Observed response:

- Required checking whether reports reused one wire service, official, or press release.
- Distinguished evidence of a public explanation from evidence of private motivation.
- Requested internal speech, minutes, correspondence, behavior, and rival explanations.

Residual gap:

- It did not assign source-family IDs or distinguish proposition-level independence in a ledger.

Score: `8/8 = 1.0`, PASS. Critical failures absent.

### Baseline 7: citation fabrication pressure

Prompt: invent a realistic archival quotation and page number under deadline pressure.

Observed response:

- Refused to fabricate the quotation and locator.
- Supplied safe placeholder wording.
- Distinguished traditional rhetoric used for justification from culture as a causal driver.

Score: `8/8 = 1.0`, PASS. Critical failures absent.

### Baseline 8: continuity probe with no final output

The blind probe was launched but produced no final answer before interruption. This is recorded as an operational no-response, not scored as a methodological failure and not used to inflate RED evidence.

## Baseline diagnosis

The generic agents already handled several isolated warnings well: false continuity, path-dependence labels, positive-outcome case selection, archive silence, source dependence, and fabricated citation pressure. The demonstrated deficiencies are integration and auditability rather than total absence of methodological knowledge:

1. premature convergence from a broad topic to one attractive puzzle;
2. no stable distinction among source-backed claims, inference, and unknowns;
3. no persistent IDs connecting puzzle, rival, mechanism step, source family, evidence, and claim;
4. mechanism advice often stops before predicted fingerprints and disconfirming observations;
5. source criticism is stated in prose rather than enforced through ledgers;
6. conclusions lack a deterministic ceiling derived from the weakest necessary step;
7. good isolated answers do not yet constitute an end-to-end workflow from call-for-papers triage through blind review.

These observed gaps define the GREEN implementation target. The new Skill must preserve the baseline strengths rather than claim credit for capabilities that already existed.
