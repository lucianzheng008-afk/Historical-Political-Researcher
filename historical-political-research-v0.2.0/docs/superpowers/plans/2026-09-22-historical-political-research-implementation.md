# Historical Political Research Agent and Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, test, and globally install one historical-political-science research Agent and one modular Skill that execute the approved end-to-end research workflow.

**Architecture:** The Skill repository is the canonical versioned package. A concise `SKILL.md` routes tasks to focused references, templates, and deterministic Python scripts. One custom Agent TOML orchestrates the Skill and optional parallel research roles; live loader testing requires the installed Agent to be a regular-file copy of the canonical repository file.

**Tech Stack:** Markdown, TOML, YAML, Python 3 standard library, `unittest`, Git, Codex Skill validator.

---

### Task 1: Record RED Behavioral Baselines

**Files:**
- Create: `evals/cases.json`
- Create: `evals/rubric.md`
- Create: `test-reports/baseline-red.md`

- [ ] **Step 1: Define the behavioral cases before production instructions exist**

Create `evals/cases.json` as valid JSON with 16 cases. Each object must include `id`, `prompt`, `required_behaviors`, and `critical_failures`. Cover broad-topic puzzle discovery, gap-without-stake, false continuity, path-dependence misuse, case-selection bias, archive silence, source dependence, discovery/confirmation reuse, concept building, world-politics level jumping, title design, research planning, adversarial review, insufficient evidence, citation fabrication pressure, and the 2026 Renmin University forum.

- [ ] **Step 2: Define the scoring contract**

Create `evals/rubric.md` with a 0/1/2 scale for each required behavior:

```text
0 = absent or contradicted
1 = present but incomplete or not operationalized
2 = explicit, correct, and connected to the requested output
```

Any listed critical failure makes the case fail regardless of score. Overall acceptance is at least 90 percent passing cases and zero critical failures.

- [ ] **Step 3: Run independent agents without the new Skill**

Give at least eight representative prompts to agents that are not given the proposed Skill or intended answer. Record the observed response pattern, exact failure category, and why the failure matters in `test-reports/baseline-red.md`.

- [ ] **Step 4: Verify RED evidence is real**

Run:

```bash
python3 -m json.tool evals/cases.json >/dev/null
rg -n "Observed failure|Critical failure|Baseline" test-reports/baseline-red.md
```

Expected: JSON parses and the baseline report contains observed, not hypothetical, failures.

- [ ] **Step 5: Commit RED artifacts**

```bash
git add evals test-reports/baseline-red.md
git commit -m "test: record historical research baseline failures"
```

### Task 2: Add Package Metadata, License, and Canonical Agent Configuration

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `THIRD-PARTY-NOTICES.md`
- Create: `CITATION.cff`
- Create: `VERSION`
- Create: `CHANGELOG.md`
- Create: `agent/historical_politics_researcher.toml`
- Create: `agents/openai.yaml`

- [ ] **Step 1: Write failing package-structure tests**

Create `tests/test_package.py` using `unittest`. It must fail until every required metadata/configuration file exists and must parse the Agent TOML with `tomllib`.

```python
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PackageTests(unittest.TestCase):
    def test_required_files_exist(self):
        for name in ["SKILL.md", "LICENSE", "CITATION.cff", "VERSION", "CHANGELOG.md"]:
            self.assertTrue((ROOT / name).is_file(), name)

    def test_agent_has_required_fields(self):
        data = tomllib.loads((ROOT / "agent/historical_politics_researcher.toml").read_text())
        for key in ["name", "description", "developer_instructions"]:
            self.assertIn(key, data)
```

- [ ] **Step 2: Run the test and confirm the expected RED failure**

Run: `python3 -m unittest tests.test_package -v`

Expected: FAIL because production package files do not yet exist.

- [ ] **Step 3: Write the package metadata**

Use MIT License with copyright `2026 Zheng Siyuan`. Set `VERSION` to `0.1.0`. `THIRD-PARTY-NOTICES.md` must identify Yang Guangbin's 2023 book as copyrighted source material and state that the OCR/full text is excluded. `CITATION.cff` must name the package and author without inventing a DOI or repository URL.

- [ ] **Step 4: Write the canonical Agent TOML**

Use only confirmed fields:

```toml
name = "historical_politics_researcher"
description = "Historical political science researcher for puzzle finding, temporal causal analysis, comparative design, concept building, planning, and adversarial review."
model_reasoning_effort = "high"
developer_instructions = """
Use $historical-political-research for substantive historical-political-science work. Keep source-backed claims, inference, and unknowns separate. Parallelize only independent research tasks. Integrate through explicit puzzles, rivals, mechanisms, source audits, and conclusion ceilings. Never fabricate evidence or citations.
"""
```

- [ ] **Step 5: Write Skill UI metadata**

`agents/openai.yaml` must set `interface.display_name`, `interface.short_description`, and a `default_prompt` explicitly containing `$historical-political-research`. Keep implicit invocation enabled. Do not declare nonexistent MCP dependencies.

- [ ] **Step 6: Re-run package tests**

Run: `python3 -m unittest tests.test_package -v`

Expected: the TOML and metadata checks pass; the missing `SKILL.md` test remains RED until Task 5.

- [ ] **Step 7: Commit metadata and configuration**

```bash
git add README.md LICENSE THIRD-PARTY-NOTICES.md CITATION.cff VERSION CHANGELOG.md agent agents tests/test_package.py
git commit -m "chore: add package metadata and canonical agent config"
```

### Task 3: Build Deterministic Research-Project Scripts

**Files:**
- Create: `scripts/init_project.py`
- Create: `scripts/validate_project.py`
- Create: `scripts/audit_claims.py`
- Create: `scripts/validate_package.py`
- Create: `tests/test_scripts.py`
- Create: `tests/fixtures/valid-project/`
- Create: `tests/fixtures/invalid-project/`

- [ ] **Step 1: Write failing script tests**

Tests must assert that initialization creates the defined research pack, valid fixtures pass, invalid fixtures fail for specific missing gates, duplicate IDs fail, unknown references fail, and a claim cannot exceed an unsupported necessary mechanism step.

- [ ] **Step 2: Run and verify RED**

Run: `python3 -m unittest tests.test_scripts -v`

Expected: FAIL because scripts do not exist.

- [ ] **Step 3: Implement `init_project.py`**

Use `argparse`, `csv`, `json`, `pathlib`, and `shutil` only. Require an explicit target directory, reject nonempty targets unless `--force` is supplied, and copy templates without modifying the Skill package.

- [ ] **Step 4: Implement project and claim validators**

`validate_project.py` checks required fields, ID uniqueness, cross-file references, source states, and blocking gates. `audit_claims.py` reports unsupported claims, missing rivals, missing scope conditions, and evidence/source-family problems. Both return nonzero on blocking failures.

- [ ] **Step 5: Implement package validator**

`validate_package.py` checks frontmatter, required files, internal Markdown links, Agent TOML fields, Skill UI metadata, template JSON/CSV schemas, and absence of the 639 KB copyrighted OCR text.

- [ ] **Step 6: Run script tests to GREEN**

Run: `python3 -m unittest tests.test_scripts -v`

Expected: all script tests pass and the invalid fixture fails only inside the tested subprocess assertions.

- [ ] **Step 7: Commit scripts and tests**

```bash
git add scripts tests
git commit -m "feat: add research project scaffolding and audits"
```

### Task 4: Create Templates and Progressive Method References

**Files:**
- Create: `assets/templates/project-metadata.json`
- Create: `assets/templates/domain-brief.md`
- Create: `assets/templates/puzzle-register.csv`
- Create: `assets/templates/question-cards.md`
- Create: `assets/templates/concept-register.csv`
- Create: `assets/templates/theory-rival-matrix.csv`
- Create: `assets/templates/case-universe.csv`
- Create: `assets/templates/case-selection-memo.md`
- Create: `assets/templates/periodization.csv`
- Create: `assets/templates/mechanism-evidence-matrix.csv`
- Create: `assets/templates/source-register.csv`
- Create: `assets/templates/source-dependence-matrix.csv`
- Create: `assets/templates/evidence-register.csv`
- Create: `assets/templates/timeline.csv`
- Create: `assets/templates/claim-register.csv`
- Create: `assets/templates/research-plan.md`
- Create: `assets/templates/review-report.md`
- Create: `references/historical-politics-foundations.md`
- Create: `references/puzzle-and-question.md`
- Create: `references/temporal-causality.md`
- Create: `references/concept-formation.md`
- Create: `references/comparative-historical-design.md`
- Create: `references/case-selection.md`
- Create: `references/sources-and-evidence.md`
- Create: `references/writing-and-review.md`
- Create: `references/quality-gates.md`
- Create: `references/bibliography.md`

- [ ] **Step 1: Add failing schema/link tests**

Extend `tests/test_package.py` to require every template and reference, validate JSON and CSV headers, and ensure every reference is linked from `SKILL.md` or another routed reference.

- [ ] **Step 2: Verify RED**

Run: `python3 -m unittest tests.test_package -v`

Expected: FAIL with missing reference/template paths.

- [ ] **Step 3: Write templates with stable IDs and explicit evidence states**

Use the approved IDs `PUZ`, `RQ`, `CON`, `CASE`, `PER`, `H`, `M`, `P`, `SRC`, `FAM`, `E`, `EV`, `CL`, `U`, and `REV`. Templates must distinguish found, not-found, conflicted, unavailable, and stipulated evidence.

- [ ] **Step 4: Write focused method references**

Convert the approved design into original, concise instructions. Do not copy the reference book or other Skills. The bibliography must distinguish method sources from substantive historical-political-science sources and must not claim full-text reading without evidence.

- [ ] **Step 5: Add the 2026 forum adapter**

Place the forum's eligibility, topic fit, 8,000-15,000-word limit, 300-character abstract, 3-5 keywords, footnote style, Word+PDF requirement, deadline, and email/filename rules in a dated optional adapter loaded only for that venue.

- [ ] **Step 6: Run package tests**

Run: `python3 -m unittest tests.test_package -v`

Expected: references and templates pass; only the missing Skill entrypoint may remain RED.

- [ ] **Step 7: Commit references and templates**

```bash
git add references assets tests/test_package.py
git commit -m "feat: add historical political research methods and templates"
```

### Task 5: Write and Validate the Skill Entrypoint

**Files:**
- Create: `SKILL.md`
- Modify: `README.md`
- Modify: `tests/test_package.py`

- [ ] **Step 1: Confirm the package test is RED for `SKILL.md`**

Run: `python3 -m unittest tests.test_package.PackageTests.test_required_files_exist -v`

Expected: FAIL naming `SKILL.md`.

- [ ] **Step 2: Write concise frontmatter and routing instructions**

Use:

```yaml
---
name: historical-political-research
description: Use when political-science, international-relations, or historical research requires historical-political-science task diagnosis, puzzle discovery, temporal causal explanation, comparative historical case selection, concept formation, research planning, or manuscript review.
license: MIT
---
```

The body must define operating modes, first-response contract, information-sufficiency gate, research-design router, hard gates, progressive reference routes, minimum deliverables, and stopping language. It must explicitly forbid chronology-as-explanation, false continuity, selection on positive outcomes, source-family double counting, normative-to-empirical leaps, and fabricated evidence.

- [ ] **Step 3: Run official and custom validators**

Run:

```bash
python3 /Users/zhengsiyuan/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
python3 scripts/validate_package.py .
python3 -m unittest discover -s tests -v
```

Expected: all validators and unit tests pass.

- [ ] **Step 4: Commit the GREEN package**

```bash
git add SKILL.md README.md tests/test_package.py
git commit -m "feat: add historical political research skill"
```

### Task 6: Run GREEN Behavioral Evals and Refactor

**Files:**
- Create: `test-reports/green.md`
- Create: `test-reports/refactor.md`
- Modify: only files justified by observed failures

- [ ] **Step 1: Re-run the RED prompts with explicit Skill use**

Independent agents receive the same prompts plus the path to the completed Skill. Score every case against `evals/rubric.md`; include response evidence rather than pass/fail assertions alone.

- [ ] **Step 2: Run blind spec review**

Give the approved design, generated package, and eval reports to a fresh reviewer. Require findings ordered by criticality and exact file/section references.

- [ ] **Step 3: Refactor only demonstrated weaknesses**

Address observed loopholes, rerun affected cases, and record before/after behavior in `test-reports/refactor.md`.

- [ ] **Step 4: Enforce behavioral acceptance**

Expected: at least 90 percent cases pass and no critical failure involving fabrication, missing rivals, false continuity, unsupported mature conclusions, or invalid package discovery.

- [ ] **Step 5: Commit evaluation and refactor results**

```bash
git add test-reports evals SKILL.md references scripts tests
git commit -m "test: validate and harden research behavior"
```

### Task 7: Install Globally and Verify End to End

**Files:**
- Install regular-file copy: `/Users/zhengsiyuan/.codex/agents/historical_politics_researcher.toml`
- Create: `MANIFEST.sha256`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Generate the integrity manifest**

Hash tracked package files except `.git`, worktrees, mutable test output, and the manifest itself. Sort paths for deterministic output.

- [ ] **Step 2: Install the single global Agent**

Create `~/.codex/agents` if needed. Compare any existing file before replacing it. Install a regular-file copy from the canonical TOML inside the Skill repository; do not use a symlink because the current Agent role loader can reject it.

- [ ] **Step 3: Run end-to-end checks**

Run official validation, custom validation, all unit tests, a clean-project scaffold/validate cycle, TOML parsing at the installed path, and the complete forum scenario.

- [ ] **Step 4: Perform final requirement audit**

Check every acceptance criterion in the design against current files, command output, behavioral reports, global discovery paths, and Git state. Treat missing evidence as incomplete.

- [ ] **Step 5: Commit release state**

```bash
git add MANIFEST.sha256 CHANGELOG.md test-reports
git commit -m "release: prepare historical political research v0.1.0"
```

- [ ] **Step 6: Merge and tag**

After final review, fast-forward `main` to `build/v0.1`, run the full verification again from the global Skill directory, confirm `git status --short` is empty, run `git fsck --full`, and tag `v0.1.0`.
