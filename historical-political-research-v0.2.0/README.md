# Historical Political Research

`historical-political-research` is a global Codex Skill plus one custom orchestration Agent for historical political science. It turns broad interests into auditable research puzzles, designs temporal and comparative explanations, tracks source and evidence limits, produces research plans, and conducts adversarial review.

The package treats Yang Guangbin's historical-political-science program as an important Chinese theoretical resource while adding comparative-historical, process-tracing, concept-formation, source-criticism, falsification, and scope-condition gates.

## Components

- Skill: `$historical-political-research`
- Agent: `historical_politics_researcher`
- Templates: project contracts, puzzle and concept registers, case and period designs, mechanism/evidence ledgers, plans, and review reports
- Literature catalog: verified Chinese and international works with explicit source roles, access levels, rule mappings, and limitations
- Method-evidence map: rule-level links between design judgments and supporting methodological literature
- Exemplar playbook: transferable moves from published historical-political research without treating exemplars as case evidence
- Scripts: project initialization, validation, claim auditing, and package validation

## Boundaries

The package does not guarantee publication, replace archival verification, or authorize fabricated evidence. It distinguishes source-backed claims, inference, and unknowns, and stops conclusions at the weakest necessary evidentiary step. Its access-level ceiling forbids claims stronger than the accessible source permits. Method sources justify research-design rules, exemplar papers demonstrate transferable analytical moves, and case evidence supports substantive historical claims; these roles are not interchangeable.

## Development

Requires Python 3.11 or newer (`tomllib` is used by the package validator).

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_package.py .
python3 scripts/validate_behavior_reports.py .
```

See `docs/superpowers/specs/` for the approved design and `docs/superpowers/plans/` for the implementation plan.

## Global installation

The repository itself is the global Skill directory:

```text
~/.agents/skills/historical-political-research/
```

Install the versioned Agent configuration as a regular file. The current Codex loader may reject a TOML symlink while applying an agent role, so do not symlink this file:

```bash
mkdir -p ~/.codex/agents
install -m 0644 ~/.agents/skills/historical-political-research/agent/historical_politics_researcher.toml \
  ~/.codex/agents/historical_politics_researcher.toml
```

If the destination already exists, compare it with the repository copy before replacing it. Restart Codex or open a new task after installation, then confirm that `$historical-political-research` and `historical_politics_researcher` are discoverable.

To upgrade, fast-forward or pull this Git repository, run the test commands above, and reinstall the Agent TOML. To uninstall, remove only the named installed Agent file and this named Skill directory after preserving any local branches or changes.
