# Implicit Routing Smoke Test

Date: 2026-09-23
Evaluator: fresh default agent `/root/implicit_routing`
Package commit at test start: `28b5770327924a1d3b526b050d5c3c63d017c00a`

The evaluator received only the globally available Skill metadata and two routing probes. It was told not to open a Skill before deciding and not to carry a choice from the first probe into the second.

## Relevant research task

Prompt: `我想把中国古代国家治理收敛为一个可检验的历史政治学研究问题`

Actual routing result:

> `selected_skill: historical-political-research`——任务要求把历史材料转化为可检验的政治学研究问题，直接符合该 Skill 的历史政治学研究场景。

Verdict: PASS. The relevant research-design request selects the global Skill.

## Unrelated historical fact task

Prompt: `汉武帝的出生年份是什么？`

Actual routing result:

> `selected_skill: none`——这是单一、明确的历史事实查询，无需沿用 A 的研究设计 Skill。

Verdict: PASS. A simple historical fact query does not select the research Skill.
