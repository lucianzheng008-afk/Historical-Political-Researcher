# Historical Political Research Agent and Skill Design

Date: 2026-09-22
Status: Approved direction; implementation pending specification review
Owner: Zheng Siyuan

## 1. Objective

Create exactly two globally available Codex components:

1. one custom Agent named `historical_politics_researcher`;
2. one Skill named `historical-political-research`.

Together they must support the complete historical-political-science research cycle: task interpretation, puzzle discovery, research-question construction, title design, research planning, historical causal analysis, comparative case selection, concept formation, evidence assessment, manuscript architecture, and adversarial review.

The system is an instruction, method, template, and evaluation package. It is not model fine-tuning and must not claim that it can guarantee publication in a top journal. Its purpose is to make high-level historical political research auditable, falsifiable, evidence-bounded, and revisable.

## 2. Global Installation

The Skill repository is installed at:

```text
/Users/zhengsiyuan/.agents/skills/historical-political-research/
```

The custom Agent is exposed at:

```text
/Users/zhengsiyuan/.codex/agents/historical_politics_researcher.toml
```

The canonical Agent TOML is versioned inside the Skill repository and installed as a regular-file copy in `~/.codex/agents/`. A live discovery test found that the current loader can fail on an Agent TOML symlink while applying the role, so installation deliberately avoids a symlink while keeping the source in the same Git history.

## 3. Architecture

### 3.1 Global Agent

The Agent is the orchestrator. It must:

- load and follow `$historical-political-research` for substantive historical-political-science tasks;
- identify the correct operating mode before researching;
- parallelize only independent work such as literature mapping, theory criticism, case-design checks, source audits, and blind review;
- integrate subagent outputs through a single evidence ledger;
- treat agreement among agents as neither evidence nor validation;
- preserve uncertainty and stop at the evidence ceiling;
- refuse fabricated citations, archives, quotations, page numbers, data, interviews, or historical details;
- return a design rather than invented findings when evidence is unavailable.

The Agent will not pin a model name, so it can inherit the user's current supported model. It may set `model_reasoning_effort = "high"`. It will inherit sandbox, tool, MCP, and permission settings from the parent session.

### 3.2 Global Skill

The Skill is the method and workflow layer. `SKILL.md` remains a concise router. Detailed guidance is progressively disclosed through focused reference files. Deterministic operations use Python standard-library scripts. Repeated research artifacts use versioned templates.

### 3.3 Relationship to Existing Skills

The package is self-sufficient for its core workflow. When available, it may route to these optional adapters:

- `good-question` for information sufficiency, question cards, falsifiers, and pilots;
- `academic-search` for source-grounded literature discovery;
- `process-tracing-research` for auditable within-case causal inference;
- `social-science-paper-writing` for manuscript alignment and submission review;
- `advantage-led-academic-writing` or `good-story` only after the question and evidence are defensible.

These are soft dependencies. Their absence must not make the new Skill unusable. Their text must not be copied into this repository.

## 4. Methodological Position

Yang Guangbin's *Historical Political Science: A Paradigm Revolution in Chinese Political Science* is an important intellectual foundation, not an unquestionable authority or the sole school represented by the Skill.

The package retains three heuristic chains from the supplied book:

```text
historical ontology -> historical continuity -> temporal spatialization
historical ontology -> mode of institutional change -> historical political theory
political ideas -> domestic institutional change -> international relations -> world order
```

Every use of these chains must pass six safeguards:

1. operationalization;
2. counterfactual reasoning;
3. negative or disconfirming cases;
4. genuine competing explanations;
5. mechanism-specific evidence;
6. explicit scope conditions.

The Skill must separate normative commitments from empirical inference. Historical origin does not establish legitimacy; local origin does not establish effectiveness; Western historical origin does not establish theoretical invalidity.

## 5. Operating Modes

| Mode | Purpose | Required output |
|---|---|---|
| `triage` | Interpret a prompt, call for papers, assignment, or venue | task contract, fit judgment, missing information, route |
| `puzzle_discovery` | Convert a broad topic, literature, or materials into a puzzle | puzzle register and ranked candidates |
| `question_design` | Form and pressure-test a research question | historical political question card |
| `title_design` | Generate titles only from an approved question | puzzle, mechanism, and theory-revision titles |
| `research_plan` | Convert a viable question into executable work | design memo, source plan, milestones, kill criteria |
| `historical_analysis` | Reconstruct temporal causation or historical processes | timeline, mechanism-evidence matrix, bounded analysis |
| `comparative_design` | Define a case universe and select cases | selection memo, comparability audit, inference ceiling |
| `concept_building` | Build or revise a political concept from historical experience | concept record, neighbors, indicators, scope, negative cases |
| `review` | Review a topic, plan, draft, or submission | blockers, ratings, evidence, repairs, verdict |
| `full_pipeline` | Execute the whole research workflow | complete research pack and blind review |

The Skill must route among theory-testing, theory-building, theory-revision, explaining-outcome, comparative historical analysis, concept formation, historical institutional analysis, and nested designs. It must not force every project into process tracing.

## 6. End-to-End Workflow

```text
task intake
-> information sufficiency gate
-> historical-political-science fit gate
-> domain and literature brief
-> puzzle discovery
-> research-question convergence
-> theory and contribution positioning
-> concept and historical-language audit
-> design routing
-> periodization and case-universe definition
-> comparative case selection
-> mechanisms, rivals, fingerprints, and falsifiers
-> two-week pilot and continue/pivot/stop decision
-> source collection and criticism
-> temporal and comparative analysis
-> evidence aggregation and conclusion ceiling
-> title, plan, outline, or manuscript output
-> friendly review
-> hostile review
-> revision loop
```

The workflow must support backward transitions. A weak puzzle returns to literature and anomaly discovery. Non-discriminating cases return to the case universe. Unobservable bottleneck steps downgrade the design. Dependent evidence returns to source collection. Overstated conclusions return to the claim register.

## 7. Core Method Modules

### 7.1 Task Contract and Evidence Status

Record the target output, language, deadline, word limit, venue, citation style, supplied materials, allowed search, known cases, time scope, and uncertainty policy.

Separate all domain statements into:

- `source-backed`;
- `inference`;
- `unknown / needs verification`.

### 7.2 Puzzle Discovery

Support at least these puzzle types:

- empirical anomaly;
- similar conditions, different outcomes;
- different conditions, similar outcomes;
- unexpected timing, delay, reversal, or non-occurrence;
- continuity after disruption;
- substantive change beneath formal stability;
- micro-macro mismatch;
- concept or theory migration failure.

A mature puzzle must contain an observed outcome, a supported prior expectation, a tension between them, a theoretical stake, and historical evidence capable of discriminating among explanations.

The following are not sufficient puzzles: importance, lack of studies, a new case, Chinese characteristics, or a claim that two things are related.

### 7.3 Research Question

The historical political question card contains:

- research object;
- spatial and temporal boundaries;
- empirical puzzle;
- prior theoretical expectation;
- defined outcome and threshold;
- main proposed cause;
- temporal causal claim;
- competing explanations;
- discriminating evidence;
- falsifying observations;
- contribution type;
- scope conditions;
- case and source feasibility;
- two-week pilot;
- strongest reviewer objection;
- stop or pivot conditions.

### 7.4 Theory and Contribution

The system recognizes contributions through new mechanisms, scope conditions, temporal sequences, concept reconstruction, theory revision, new comparisons, or new evidence that changes an established inference. A new case or alleged literature gap alone is insufficient.

### 7.5 Concepts and Historical Translation

Each core concept records actor language, analyst language, intension, extension, threshold, meaning change across periods, neighboring concepts, indicators, scope, and misuse risks.

Identical words across periods do not establish conceptual equivalence. Functional similarity does not establish historical continuity. Contemporary analytical language must not be projected onto historical actors without explanation.

### 7.6 Time and Continuity

Every design identifies baseline conditions, start, trigger, critical junctures, expected lags, sequence, consolidation, feedback, interruptions, reversals, and competing timelines.

A continuity claim requires:

```text
historical origin
-> carrier
-> transmission activity
-> reproduction mechanism
-> interruption test
-> later outcome
```

Path dependence additionally requires an initial choice set, a critical juncture, and a specified self-reinforcing or reactive sequence.

### 7.7 Cases and Comparison

Define the case universe before selecting cases. Record cause, outcome, context, period, expected mechanism, evidence access, heterogeneity risks, inferential role, and selection-bias risk.

Support typical, deviant, crucial, pathway, most-likely, least-likely, most-similar, most-different, within-case temporal, paired, and shadow comparisons.

Do not select only positive outcomes or vivid confirming cases. Unequal evidence access requires case-specific inference ceilings and comparison on a common evidence layer.

### 7.8 Mechanisms and Observables

Every mechanism step must specify entity, activity, input, output, context, timing, changed state, productive link, predicted trace, alternative evidence-generating process, disconfirming observation, and target source.

Labels such as culture, pressure, persuasion, tradition, or institution are not mechanisms by themselves.

### 7.9 Sources and Evidence

Evaluate authenticity, proximity, competence, audience, genre, motive, preservation, access, diagnosticity, and proposition-specific independence.

Use source-family IDs to prevent copied reports from being counted as triangulation. Metadata supports only bibliographic existence. Official records support official expression, not necessarily private motivation. Absence is negative evidence only when expected observability and access probability are high.

### 7.10 Rivals and Falsification

Construct the strongest plausible rival symmetrically. A rival may be another outcome-generating mechanism, another pathway from the same cause, or an alternative process that generated the observed evidence.

Supporting the focal explanation does not eliminate a rival. Complementary mechanisms must be allowed.

### 7.11 Evidence Aggregation

Aggregate only in this order:

```text
observation -> proposition -> mechanism step -> mechanism -> bounded claim
```

Evidence moves only one level at a time. A complete claim cannot be stronger than its weakest necessary step. Use qualitative Bayesian updating by default and never invent precise posterior probabilities.

### 7.12 Writing and Review

Organize analysis by causal or conceptual function rather than chronology alone. Each analytical unit contains theoretical function, case condition and timing, entity and activity, best evidence and source context, transmission, comparison with the best rival, update, and limitation.

Review occurs twice:

- friendly review finds the strongest repairable version;
- hostile review applies editor and methods-reviewer standards.

Each failed or partial item must name its location, severity, operation, and expected improvement.

## 8. Stable IDs and Research Artifacts

Use immutable IDs:

```text
PUZ-* puzzle
RQ-* research question
CON-* concept
CASE-* case
PER-* period
H-* explanation
M-* mechanism
M-*-S* mechanism step
P-* predicted fingerprint
SRC-* source
FAM-* source family
E-* evidence state
EV-* event
CL-* claim
U-* update
REV-* revision
```

The full research pack includes:

- `project-metadata.json`;
- `domain-brief.md`;
- `puzzle-register.csv`;
- `question-cards.md`;
- `concept-register.csv`;
- `theory-rival-matrix.csv`;
- `case-universe.csv`;
- `case-selection-memo.md`;
- `periodization.csv`;
- `mechanism-evidence-matrix.csv`;
- `source-register.csv`;
- `source-dependence-matrix.csv`;
- `evidence-register.csv`;
- `timeline.csv`;
- `claim-register.csv`;
- `research-plan.md`;
- `review-report.md`.

Smaller tasks produce only the relevant subset while preserving compatible IDs and evidence rules.

## 9. Hard Quality Gates

Any blocking failure prevents mature manuscript drafting:

1. no explicit tension between observation and supported expectation;
2. undefined outcome, case, or time boundary;
3. contribution limited to a gap or new case;
4. history used only as background;
5. continuity asserted without carrier and reproduction mechanism;
6. cases chosen without inferential logic;
7. mechanism expressed only through labels or arrows;
8. necessary steps lack propositions or observability;
9. metadata or abstracts used for substantive factual claims;
10. dependent reports counted as independent evidence;
11. no genuine rival;
12. no possible falsifier;
13. conclusion exceeds the weakest necessary step;
14. single-case mechanism evidence generalized without scope conditions;
15. autonomous knowledge treated only as a normative slogan;
16. normative legitimacy inferred directly from historical origin;
17. fabricated or unverified bibliographic and historical detail.

## 10. Package Structure

```text
historical-political-research/
├── SKILL.md
├── agents/openai.yaml
├── agent/historical_politics_researcher.toml
├── references/
│   ├── historical-politics-foundations.md
│   ├── puzzle-and-question.md
│   ├── temporal-causality.md
│   ├── concept-formation.md
│   ├── comparative-historical-design.md
│   ├── case-selection.md
│   ├── sources-and-evidence.md
│   ├── writing-and-review.md
│   ├── quality-gates.md
│   └── bibliography.md
├── assets/templates/
├── scripts/
│   ├── init_project.py
│   ├── validate_project.py
│   ├── audit_claims.py
│   └── validate_package.py
├── tests/
├── evals/
├── test-reports/
├── docs/superpowers/specs/
├── README.md
├── LICENSE
├── THIRD-PARTY-NOTICES.md
├── CITATION.cff
├── CHANGELOG.md
├── VERSION
└── .gitignore
```

## 11. Test Strategy

Skill development follows RED-GREEN-REFACTOR.

### RED

Run independent agents without the Skill on realistic pressure scenarios. Record exact failures and rationalizations before writing production instructions.

### GREEN

Write the smallest Skill, references, templates, and scripts that correct observed failures. Re-run the same prompts with explicit Skill invocation.

### REFACTOR

Use an independent blind reviewer to find new loopholes. Add only changes supported by observed failures and re-run all tests.

Behavioral scenarios include:

- broad tradition topic;
- gap-without-stake;
- chronology masquerading as explanation;
- false continuity from shared terminology;
- path-dependence label without feedback;
- selection on the dependent variable;
- archive silence treated as disproof;
- unequal evidence across cases;
- strategic speech treated as private motive;
- dependent reports treated as triangulation;
- discovery evidence reused as confirmatory evidence;
- concept invention without boundaries or indicators;
- autonomous-knowledge slogans without explanatory gain;
- polished title without outcome, mechanism, or rival;
- fabricated citation pressure;
- full Renmin University forum workflow.

Deterministic tests cover:

- official Skill quick validation;
- YAML and TOML parsing;
- internal-link integrity;
- required package files;
- template schemas;
- project initialization;
- valid fixtures passing;
- invalid fixtures failing for the expected gate;
- claim-evidence ceiling checks;
- Git cleanliness and manifest integrity.

Acceptance requires at least 90 percent behavioral success and zero critical failures involving fabricated evidence, missing rivals, unsupported mature conclusions, or invalid package discovery.

## 12. License, Copyright, and Git

Original instructions, templates, configuration, and scripts use the MIT License, copyright 2026 Zheng Siyuan.

The supplied 2023 book is copyrighted third-party material. Its OCR text is not included in the repository. The package includes only original analytical synthesis, bibliographic information, and short necessary references. `THIRD-PARTY-NOTICES.md` records the intellectual sources and their copyright status.

The repository uses branch `main`. Planned commits are:

1. design specification;
2. RED behavioral fixtures and baseline reports;
3. GREEN Skill, Agent, references, templates, and scripts;
4. REFACTOR corrections and final reports.

Release `v0.1.0` is tagged only after all acceptance checks pass and the working tree is clean. No remote repository is created or pushed without a separately supplied destination or explicit request.

## 13. Non-Goals

Version 0.1 will not:

- create more than one persistent custom Agent;
- create more than one Skill;
- copy the full reference book or journal articles;
- guarantee top-journal acceptance;
- invent historical evidence or complete inaccessible archives;
- treat a single historical-political-science school as settled truth;
- require optional third-party Skills to function;
- publish to GitHub or another remote automatically.

## 14. Acceptance Criteria

The work is complete only when:

1. `$historical-political-research` is globally discoverable and explicitly invocable;
2. implicit invocation activates on relevant research tasks and avoids unrelated historical questions;
3. `historical_politics_researcher` can be spawned by name;
4. the Agent consistently loads the Skill and respects its hard gates;
5. official and custom validators pass;
6. script unit tests and positive/negative fixtures pass;
7. at least 90 percent of behavioral cases pass with zero critical failures;
8. the forum test produces a fit judgment, puzzle, question, titles, plan, case logic, temporal mechanisms, evidence needs, and review report;
9. the package contains MIT, third-party notices, citation metadata, and version metadata;
10. the Git repository is clean, internally consistent, and tagged `v0.1.0`.
