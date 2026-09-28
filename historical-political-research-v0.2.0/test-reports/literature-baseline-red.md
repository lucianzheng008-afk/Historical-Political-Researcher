# Literature-grounding baseline (pre-v0.2)

## Result

With the complete normal v0.1.0 production resources available, all nine newly added literature cases pass the current behavioral rubric: **9/9 PASS, required 9, 0 critical failures**. There is no suite-level RED in this valid package baseline.

This conclusion supersedes the earlier restricted-resource runs. Those generators were instructed not to use the existing references that `SKILL.md` normally routes, so the resulting `dynamic-temporality-literature` failure could not validly be attributed to v0.1.0. The replacement runs let each generator use the full packaged production surface at commit `3ec6c1f`, including the existing references and templates, while keeping the case standards and proposed v0.2 resources out of its prompt context.

The proposed change should therefore be framed as an evidence-density, metadata-verification, and routing improvement rather than as a repair of unsafe v0.1 behavior. The valid baseline still records four partial criteria that v0.2 can improve.

## Provenance and protocol

- Production version: `0.1.0`
- Production commit supplied to generators: `3ec6c1f7eb2690555d33cc6b6b094dc99469b674`
- Case revision at rerun: `ca351e3499337ef3e98aa3e70da873bb571c0f3a`
- Cases blob: `b683f966aaac0f036914a8d100a6d4a200fdb081`
- Scoring rubric blob: `f472b30cbf102613c9fad98600f722592f082295`
- Generator runs: `/root/task1_red_baseline/red_full_a`, `/root/task1_red_baseline/red_full_b`, `/root/task1_red_baseline/red_full_c`
- Runtime identity reported by each run: `historical_politics_researcher role; exact model identifier not exposed`
- Scorer: `/root/task1_red_baseline`
- Each generator received exactly three prompts and did not self-score.
- The generator instructions allowed the complete normal v0.1 production scope: `SKILL.md`, the Agent file, Skill-routed `references/`, relevant `assets/templates/`, and production scripts.
- The generator instructions excluded evaluation standards, test reports, design and implementation plans, post-`3ec6c1f` changes, proposed v0.2 resources, and new literature lists. These were instruction constraints, not claims of filesystem ACL enforcement.
- No network search was used, so the result measures the packaged v0.1 resource baseline.
- The scorer subsequently applied the current case requirements and `evals/rubric.md`. Each behavior, critical-failure check, response, and decision is preserved in the raw JSON.

## Case results

| Run | Case | Score | Result | Remaining weakness |
|---|---|---:|---|---|
| A | `literature-rule-role` | 7/8 | PASS | Separates ordinary persistence and increasing returns but does not explicitly distinguish a reactive sequence. |
| A | `access-level-ceiling` | 7/8 | PASS | Safely separates abstract, full text, and page verification, but does not state the complete metadata/abstract/full-text/page-level taxonomy. |
| A | `historiography-selection-bias` | 8/8 | PASS | No material omission under the rubric. |
| B | `exemplar-transfer` | 8/8 | PASS | No material omission under the rubric. |
| B | `method-disagreement` | 8/8 | PASS | No material omission under the rubric. |
| B | `citation-metadata-pressure` | 8/8 | PASS | No material omission under the rubric. |
| C | `dynamic-temporality-literature` | 7/8 | PASS | Uses relevant packaged literature and temporal predictions, but duration and speed or tempo are not explicit. |
| C | `source-role-confusion` | 7/8 | PASS | Distinguishes method authority from current case evidence but does not separately identify an empirical exemplar as a third literature role. |
| C | `chinese-international-false-dichotomy` | 8/8 | PASS | No material omission under the rubric. |

## What the valid baseline establishes

The packaged v0.1 references materially affect behavior. Once normal routing is available, the Agent can select existing method anchors for path dependence, critical junctures, institutional change, process tracing, and Chinese historical political science. It connects those anchors to rules and research-design changes rather than using them decoratively. It also preserves the production package's existing refusal, evidence-ceiling, rival-explanation, source-criticism, and anti-fabrication safeguards.

No response fabricated a citation, DOI, page, archive, quotation, case fact, or author position. No response let a classic work prove a case, an abstract prove page-level content, a method paper prove historical facts, an exemplar's conclusion migrate to a new case, or source nationality determine method validity.

## Improvement target for v0.2

The baseline does not justify claiming a broken or unsafe literature workflow. It does support a narrower upgrade:

1. **Increase verified evidence density.** Existing responses can name appropriate anchors, but often disclose that the package contains a reading map or partial metadata rather than verified full-text, version, and page-level support.
2. **Make rule-to-source routing explicit and inspectable.** The current Agent often succeeds by synthesizing prose across references. A structured catalog and rule map can make the same decision repeatable and auditable.
3. **Standardize access and verification states.** The four-level access taxonomy and stable `needs verification` state should appear without relying on free-form phrasing.
4. **Separate three literature roles.** Method authority, empirical exemplar, and current-case evidence should be named independently.
5. **Increase temporal coverage.** Duration, speed or tempo, timing, lag, sequence, and boundaries should be checked as a fixed set.
6. **Make exemplar transfer systematic.** Even though the baseline answer passes, a playbook can standardize comparisons of outcome, population, period, strategic conditions, evidence, and transfer ceiling.
7. **Pair Chinese and international sources at rule level.** The baseline performs a principled dialogue; v0.2 can record precisely which sources support, qualify, or dispute each rule.

GREEN should demonstrate these density, verification, routing, and explicitness gains while preserving the 9/9 behavioral pass and zero critical failures.

## Raw evidence

- `test-reports/raw/literature-red-a.json`
- `test-reports/raw/literature-red-b.json`
- `test-reports/raw/literature-red-c.json`
