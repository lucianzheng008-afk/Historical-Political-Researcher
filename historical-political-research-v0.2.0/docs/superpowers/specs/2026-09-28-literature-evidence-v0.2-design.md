# Literature-Evidence Upgrade for Historical Political Research

Date: 2026-09-28
Status: Approved by user on 2026-09-28
Target release: 0.2.0
Branch: `feature/literature-evidence-v0.2`

## 1. Objective

Upgrade the global `historical-political-research` Skill and the single global `historical_politics_researcher` Agent from a method package with a selective bibliography into a literature-grounded research system.

The upgrade must connect four layers:

```text
method rule -> authoritative source -> worked exemplar -> behavioral test
```

The purpose is not to maximize citation count. It is to ensure that important research judgments can be traced to an appropriate methodological literature, illustrated by a real study, bounded by known disagreements, and tested in realistic use.

This remains instruction and reference engineering, not model fine-tuning. It cannot guarantee publication or substitute authority for research judgment.

## 2. Scope and Non-Goals

### In scope

- at least 30 verified core works in the first literature catalog; the initial 30-record release set will contain 12 Chinese-language historical-political-science works and 18 international methods or exemplars;
- a method-evidence map covering the Skill's major blocking rules;
- an exemplar playbook of at least 12 studies, including at least four Chinese-language studies and eight international studies;
- progressive routing from `SKILL.md` to the literature resources relevant to the current mode;
- Agent instructions that require source-role awareness and access-level disclosure;
- static and behavioral tests for literature-grounded decisions;
- version, changelog, manifest, installation, and Git release updates for `v0.2.0`.

### Out of scope

- copying copyrighted books, journal PDFs, or the supplied OCR corpus into the repository;
- building a vector database, full-text RAG service, citation-counting service, or automatic paywall bypass;
- claiming that a famous or highly cited work is correct by virtue of status;
- requiring citations for simple factual answers or every sentence;
- turning one Chinese or international school into the uncontested canon of historical political science.

## 3. Design Principles

### 3.1 Citations must change a decision

A source belongs in the core map only if it clarifies a choice, limit, warning, or procedure. Decorative citations are a failure.

### 3.2 Method sources and exemplars have different roles

A methods article may justify a design rule. An empirical article may demonstrate how a move was executed. An exemplar does not prove that the same mechanism holds in a new case.

### 3.3 Authority never removes disagreement

Where sources conflict, the package records the disagreement and states what design choice or evidence would discriminate between them. This is especially important for:

- counterfactual versus historical-narrative accounts of causation;
- comparison as causal control versus comparison as interpretation or concept formation;
- mechanisms as entities and activities versus mechanisms as event sequences;
- universal concepts versus historically reconstructed or locally generated concepts;
- autonomy of Chinese knowledge construction versus cross-context validity tests.

### 3.4 Access determines the claim ceiling

Metadata permits bibliographic claims. An abstract permits only claims directly supported by the abstract. Full-text access permits section-level interpretation. Pinpoint page claims require inspecting the cited edition and page.

### 3.5 Chinese and international literatures are mutually testing resources

The package will not rank them as local theory versus universal method. Chinese historical-political-science arguments will be assessed for operationalization, evidence, scope, and inference. International methods will be assessed for historical and contextual fit rather than treated as neutral universal standards.

## 4. Architecture

### 4.1 Machine-readable catalog

Create `references/literature-catalog.json` as the canonical metadata store. Each record will contain:

| Field | Purpose |
|---|---|
| `id` | stable identifier such as `METH-TEMP-001`, `CN-DEB-001`, or `EX-IR-001` |
| `title`, `authors`, `year` | display metadata |
| `publication_type`, `venue`, `volume`, `issue`, `pages` | publication context |
| `doi`, `isbn`, `official_url` | stable identifiers and access path |
| `language`, `tradition`, `domain_tags` | routing fields |
| `role` | `method`, `field_foundation`, `debate`, `critique`, or `exemplar` |
| `verification_status` | `full_text`, `publisher_abstract`, `publisher_metadata`, or `needs_verification` |
| `access_status` | `open_full_text`, `open_abstract`, `metadata_only`, or `needs_institution` |
| `supports_rule_ids` | method rules affected by the work |
| `limitations` | dispute, transfer risk, or non-applicability |
| `verified_via`, `verified_at` | provenance and date |

The catalog must use official journal, publisher, DOI, Crossref, OpenAlex, or authoritative institutional pages where available. A missing DOI is allowed for Chinese articles and books; invented identifiers are not.

### 4.2 Method-evidence map

Create `references/method-evidence-map.md`. It will organize literature by research decision rather than author name. Each mapped rule will contain:

1. the operational rule used by the Skill;
2. one or more authoritative sources;
3. the source's actual role and access level;
4. an important disagreement or boundary;
5. the output record that demonstrates compliance;
6. one relevant exemplar where available.

The initial map will cover:

- puzzle and contribution formation;
- comparative-historical analysis;
- temporality, sequence, duration, pace, and lag;
- path dependence and critical junctures;
- gradual institutional change;
- causal mechanisms and process tracing;
- Bayesian evaluation of qualitative evidence;
- case-universe definition and purposive case selection;
- controlled, nested, within-case, and cross-case comparison;
- concept formation, conceptual travel, and measurement validity;
- source criticism, historiographical disagreement, and selection bias;
- archival silence, source dependence, and digital-archive abundance;
- theory locality, Chinese autonomous knowledge construction, and cross-context scope;
- manuscript review and conclusion ceilings.

### 4.3 Exemplar playbook

Create `references/exemplar-playbook.md`. Every exemplar entry will use the same schema:

```text
publication and verification status
research puzzle
prior expectation and strongest rival
contribution
design, cases, and period
temporal move
mechanism or inferential move
evidence families
what can be learned
what must not be mechanically copied
relevant Skill modes and rule IDs
```

The initial international anchors will include studies such as Tannenwald on nuclear non-use, Ziblatt on Prussian landholding inequality and democratization, Stasavage on geographic scale and representative assemblies, and Capoccia and Ziblatt on the historical turn in democratization research. Chinese entries will be selected for demonstrated research execution, not merely because they advocate historical political science.

### 4.4 Revised bibliography

Rebuild `references/bibliography.md` as a human-readable reading map derived from the catalog. It will no longer be the canonical metadata source. It will distinguish:

- foundational field statements;
- methods and design;
- critiques and internal debates;
- worked exemplars;
- supplied but not independently verified sources.

### 4.5 Progressive module integration

Existing method references will receive compact literature anchors using stable IDs. They will not reproduce full bibliographic entries. Examples:

- `temporal-causality.md` points to sources on sequencing, duration, path dependence, critical junctures, and narrative evidence;
- `case-selection.md` points to purposive selection, controlled comparison, nested analysis, and historiographical selection bias;
- `sources-and-evidence.md` points to historical-record selection, the Ulysses principle, review criteria, archival silence, and digital-source risks;
- `concept-formation.md` points to Sartori, Collier and Mahon, Gerring, Goertz, and Adcock and Collier;
- `historical-politics-foundations.md` maps Chinese field foundations together with internal methodological criticism.

`SKILL.md` remains a concise router. It will add links to the method-evidence map and exemplar playbook only when the task needs literature justification, method selection, exemplar analysis, or review.

## 5. Agent Behavior

The canonical Agent TOML will require the Agent to:

1. identify the research decision before searching for an authority;
2. consult the relevant rule and literature subset rather than loading the entire catalog;
3. distinguish `method authority`, `empirical exemplar`, `substantive evidence`, and `field debate`;
4. disclose whether a claim comes from full text, abstract, metadata, or an unverified lead;
5. justify major design choices using the pattern `rule -> source -> application -> limit`;
6. use exemplars to teach moves, not to import conclusions into the user's case;
7. expose disagreement between traditions when it changes the design;
8. label package conventions as conventions when no authoritative support is established;
9. refuse invented citations, page numbers, DOI values, quotations, or summaries;
10. omit unnecessary literature display when the user asks for a narrow deliverable.

The Agent will not be instructed to cite a fixed number of works. Relevance and traceability matter more than count.

## 6. Data Flow

```text
user task
-> operating mode and research decision
-> relevant method rule IDs
-> catalog subset and verification ceiling
-> optional exemplar entry
-> source-role and disagreement check
-> research output
-> literature-grounding and inference audit
```

When external search is allowed, newly discovered works remain task-level leads unless their metadata and role are verified. They do not silently become part of the global canon.

## 7. Failure Handling

- **Conflicting metadata:** prefer the publisher or journal record, then Crossref or OpenAlex; retain the disagreement until resolved.
- **No DOI:** use an official journal issue, publisher, institutional repository, or library record and leave DOI null.
- **Abstract-only access:** prohibit detailed claims about argument structure, evidence, or limitations not present in the abstract.
- **Unverified supplied source:** retain it in a separate status and prohibit exact bibliographic claims.
- **Method disagreement:** record both positions and require the research design to choose or test between them.
- **No mapped authority:** mark the instruction as a package convention and schedule it for later review.
- **Exemplar mismatch:** explain the difference in outcome, case universe, period, evidence, or inferential aim instead of forcing analogy.
- **Copyright boundary:** store metadata, synthesis, and short compliant descriptions; do not commit protected full text.

## 8. Literature Coverage

The initial core must include verified anchors in the following clusters:

| Cluster | Core anchors |
|---|---|
| Chinese field formation | Yang Guangbin; Yang Guangbin and Shi Qipeng; Yao Zhongqiu; Ren Feng |
| Chinese methodological debate | Zhang Shuping; Shi Qipeng; Lyu Jie; additional work on temporal and historical causal analysis |
| Comparative-historical analysis | Mahoney and Rueschemeyer; Mahoney and Thelen; Slater and Ziblatt; Lieberman |
| Temporality and institutional change | Pierson; Büthe; Grzymala-Busse; Capoccia and Kelemen; Falleti and Lynch |
| Process tracing and evidence | Collier; Mahoney; Bennett and Checkel; Beach and Pedersen; Fairfield and Charman |
| Concepts and measurement | Sartori; Collier and Mahon; Gerring; Goertz; Adcock and Collier |
| Cases and comparison | Seawright and Gerring; Gerring; Slater and Ziblatt; Lieberman |
| Historiography and sources | Lustick; Møller and Skaaning; Møller; work on digital archival research |
| Exemplars | Tannenwald; Ziblatt; Stasavage; Capoccia and Ziblatt; selected Chinese studies |

Inclusion in this table is a search target, not permission to fill missing metadata from memory.

## 9. Testing Strategy

### 9.1 RED behavioral baseline

Before changing production instructions, run independent evaluations against the current `v0.1.0` Skill. New cases will test whether an Agent:

- invokes path dependence without distinguishing increasing returns, reactive sequences, and ordinary persistence;
- treats historical narrative as self-validating evidence;
- selects historical monographs that agree with its theory without surveying historiographical disagreement;
- converts archival silence into proof of non-occurrence;
- cites famous methods without connecting them to a design choice;
- mistakes an exemplar's finding for evidence about a new case;
- invents page numbers or DOI values under pressure;
- treats Chinese and international methods as mutually exclusive camps;
- fails to disclose abstract-only or metadata-only access.

The RED report will record exact observed failures. Existing successful safeguards will not be rewritten merely to create work.

### 9.2 Static tests

Extend package tests to require:

- valid JSON and unique literature IDs;
- allowed role, verification, and access enums;
- valid DOI syntax when a DOI is present;
- all mapped literature IDs exist in the catalog;
- all blocking method clusters have mapped sources;
- every exemplar has a learning move and a non-transfer warning;
- every reference linked from `SKILL.md` or a routed reference exists;
- no protected full-text corpus enters the package;
- canonical and installed Agent files match after installation;
- version, changelog, citation metadata, and manifest agree.

Tests will check structure and invariants, not exact prose or a frozen list of authors.

### 9.3 GREEN and refactor evaluations

Re-run the RED prompts with the upgraded Skill and Agent. Acceptance requires:

- at least 90 percent of literature-grounding cases pass;
- zero fabricated citation, quotation, page, DOI, archive, or historical-detail failures;
- correct separation of method source, exemplar, and case evidence;
- explicit access-level disclosure when it affects the claim;
- at least one hostile review that attempts to induce decorative citation or authority substitution;
- the original 16-case behavior suite remains at or above its current release threshold.

## 10. Files Expected to Change

```text
SKILL.md
agent/historical_politics_researcher.toml
references/bibliography.md
references/literature-catalog.json
references/method-evidence-map.md
references/exemplar-playbook.md
references/historical-politics-foundations.md
references/puzzle-and-question.md
references/temporal-causality.md
references/concept-formation.md
references/comparative-historical-design.md
references/case-selection.md
references/sources-and-evidence.md
references/writing-and-review.md
evals/cases.json
evals/rubric.md
tests/test_package.py
test-reports/literature-baseline-red.md
test-reports/literature-green.md
README.md
VERSION
CHANGELOG.md
CITATION.cff
THIRD-PARTY-NOTICES.md
MANIFEST.sha256
```

The exact set may be reduced during planning if a file does not need modification. Unrelated refactoring is excluded.

## 11. Release and Installation

The completed work will:

1. pass unit tests and the package validator;
2. pass independent behavioral evaluation;
3. set the package version to `0.2.0`;
4. record literature and behavior changes in `CHANGELOG.md`;
5. regenerate `MANIFEST.sha256` only after final file contents stabilize;
6. reinstall the canonical Agent TOML as a regular file at `/Users/zhengsiyuan/.codex/agents/historical_politics_researcher.toml`;
7. verify that the installed Agent matches the repository copy;
8. commit the implementation and create the annotated Git tag `v0.2.0` after final verification.

The existing MIT License remains unchanged. `THIRD-PARTY-NOTICES.md` will clarify that bibliographic metadata, original synthesis, and links are included, while supplied and publisher-controlled full texts are excluded.

## 12. Acceptance Criteria

The upgrade is complete only when:

- the literature catalog contains at least 30 verified core records, with 12 Chinese-language and 18 international records in the initial 30-record release set;
- all major method clusters are connected to authoritative sources and limitations;
- at least 12 exemplars are analyzed with a common schema and non-transfer warning;
- the Agent can explain why a source is relevant rather than merely name it;
- access levels and unresolved metadata are visible;
- no rule relies on an invented or unverified citation;
- new literature-grounding evaluations and the original regression suite pass;
- the global Skill and installed Agent report version `0.2.0` consistently;
- the Git worktree is clean and the release tag points to the verified commit.
