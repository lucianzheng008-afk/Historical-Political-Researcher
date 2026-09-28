# Global Agent Smoke Test

Date: 2026-09-23
Package commit: `28b5770327924a1d3b526b050d5c3c63d017c00a`
Agent: `historical_politics_researcher`

## Discovery and installation

- The global Skill was discovered from `/Users/zhengsiyuan/.agents/skills/historical-political-research/SKILL.md` in a fresh task context.
- A symbolic link at `/Users/zhengsiyuan/.codex/agents/historical_politics_researcher.toml` failed in a Codex CLI spawn with `Too many levels of symbolic links`; the attempted child did not run.
- The link was removed and replaced with a regular file byte-identical to `agent/historical_politics_researcher.toml`. Documentation was updated to make the regular-file copy the supported installation method.

## Successful named-agent run

The collaboration runtime then spawned the custom role explicitly with:

```text
agent_type = historical_politics_researcher
task = release_smoke
```

Prompt: judge whether adoption of a unitary state in 1949 and its persistence to the present is sufficient evidence of path dependence, in no more than 180 Chinese characters, with an evidence ceiling.

Actual response:

> 不足。现有事实仅证明制度长期延续，不能区分路径依赖与持续的功能性选择、权力约束等替代解释。还需证明1949年的可行选项与非必然选择、随后自我强化及转换成本上升；若替代方案长期可行却反复被重新择优，路径依赖将被削弱。证据上限：只能称“制度持续性”，不能作因果判断。

Verdict: PASS. The named custom Agent completed, used the required path-dependence safeguards, gave a rival explanation, and respected the evidence ceiling without inventing historical detail.
