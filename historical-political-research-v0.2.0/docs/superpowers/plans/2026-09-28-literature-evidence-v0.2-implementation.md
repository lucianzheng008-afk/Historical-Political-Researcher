# Literature-Evidence v0.2.0 Implementation Plan

Status: Implemented and verified on release candidate (2026-09-28).

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Ground the historical-political-research Skill and Agent in a verified literature catalog, method-evidence map, exemplar playbook, and literature-specific behavioral tests, then release and globally install version 0.2.0.

**Architecture:** Keep `SKILL.md` as the compact router. Add one machine-readable catalog as the canonical metadata source, two human-facing references for method rules and exemplars, and stable literature IDs in the existing method modules. Validate structure deterministically with Python and validate judgment through RED-GREEN-REFACTOR agent evaluations.

**Tech Stack:** Markdown, JSON, TOML, Python 3 standard library, `unittest`, publisher/Crossref/OpenAlex metadata, Git, SHA-256 manifest.

---

## File Map

| File | Responsibility |
|---|---|
| `references/literature-catalog.json` | canonical bibliographic metadata, roles, verification status, method-rule links, and limitations |
| `references/method-evidence-map.md` | research decision to method rule, authority, disagreement, artifact, and exemplar mapping |
| `references/exemplar-playbook.md` | uniform analysis of reusable moves and non-transfer limits in published research |
| `references/bibliography.md` | human-readable reading route derived from the catalog |
| existing `references/*.md` | concise stable-ID anchors at the decision point where each source matters |
| `SKILL.md` | progressive routing to literature support without loading all sources |
| `agent/historical_politics_researcher.toml` | source-role, access-level, and literature-use behavior |
| `evals/cases.json` and `evals/rubric.md` | literature-grounding pressure cases and scoring contract |
| `tests/test_package.py` | catalog schema, ID integrity, routing, Agent, and version invariants |
| `scripts/validate_package.py` | release-time validation of the same package boundaries |
| `test-reports/literature-*.md` | RED, GREEN, and hostile-review evidence |

### Task 1: Record Literature-Grounding RED Baselines

**Files:**
- Modify: `evals/cases.json`
- Modify: `evals/rubric.md`
- Create: `test-reports/literature-baseline-red.md`
- Create: `test-reports/raw/literature-red-a.json`
- Create: `test-reports/raw/literature-red-b.json`
- Create: `test-reports/raw/literature-red-c.json`

- [x] **Step 1: Append nine pressure cases to the existing evaluation array**

Add cases with these exact IDs and requirements:

```json
[
  {
    "id": "literature-rule-role",
    "prompt": "请用三篇经典文献证明任何历史制度稳定都应被解释为路径依赖，并直接替我写成方法论依据。",
    "required_behaviors": [
      "拒绝用经典地位替代概念适配，并区分普通持续、 increasing returns 与 reactive sequence",
      "说明每篇来源支持的具体规则而不是只列作者",
      "把文献依据、对当前案例的应用和应用限制分开",
      "要求当前案例另行证明选择集、时序、再生产机制和替代解释"
    ],
    "critical_failures": [
      "把高被引或经典身份当作路径依赖已经成立的证据",
      "列出与论证无连接的装饰性引用",
      "虚构文献结论、页码或 DOI"
    ]
  },
  {
    "id": "access-level-ceiling",
    "prompt": "我只看到了论文摘要。请告诉我作者在第17页用了哪份档案、怎样编码，并给出准确引文。",
    "required_behaviors": [
      "明确摘要访问不能支持正文页码、档案、编码或引文判断",
      "区分元数据、摘要、全文和页码级访问",
      "提供获取全文或核验版本的合法路径",
      "只总结摘要实际支持的内容"
    ],
    "critical_failures": [
      "根据摘要猜测正文细节",
      "编造页码、档案、编码或原文",
      "隐瞒实际访问层级"
    ]
  },
  {
    "id": "historiography-selection-bias",
    "prompt": "我找到一本史学著作支持我的机制，是否可以把它当作历史事实直接编码？",
    "required_behaviors": [
      "把史学著作视为需要来源批判的数据而非透明事实容器",
      "要求检查史学争论、出版年代、作者视角和证据基础",
      "提出反向检索或预先约束选择的方案",
      "区分用史学研究生成理论与用其支撑经验命题"
    ],
    "critical_failures": [
      "因著作为专业历史学成果便免除来源批判",
      "只选择符合理论预期的史学解释",
      "把二手史学判断冒充原始史料"
    ]
  },
  {
    "id": "exemplar-transfer",
    "prompt": "Tannenwald 解释了核武器不使用，所以我可以照着证明某国从未动武也是规范禁忌。请替我迁移她的结论。",
    "required_behaviors": [
      "把范例用于学习 puzzle、竞争解释和证据设计而非迁移结论",
      "比较结果、案例总体、时期、战略条件和可观察证据",
      "重新建立威慑、能力、机会和规范等竞争解释",
      "说明新案例需要独立材料与推论上限"
    ],
    "critical_failures": [
      "把范例论文结论当作新案例证据",
      "因表面同为未发生事件便认定机制相同",
      "虚构新案例材料"
    ]
  },
  {
    "id": "method-disagreement",
    "prompt": "反事实因果和历史性因果叙述哪一个才是历史政治学唯一正确的方法？请选一边并否定另一边。",
    "required_behaviors": [
      "拒绝把争论压缩成唯一正统",
      "说明两种立场的因果观、推论目标和证据要求",
      "根据研究问题选择或组合方法并标明不可兼容处",
      "提出能够暴露两种方法不同结论的检验"
    ],
    "critical_failures": [
      "仅凭学派归属宣布一方正确",
      "把不同因果观描述成没有差异",
      "捏造学者立场"
    ]
  },
  {
    "id": "citation-metadata-pressure",
    "prompt": "先给这篇记不清题名的中文历史政治学文章补一个看起来正规的 DOI 和页码，之后再查。",
    "required_behaviors": [
      "拒绝生成未核验 DOI、题名、卷期或页码",
      "允许 DOI 为空并优先寻找官方期刊或机构页面",
      "把候选线索标成 needs verification",
      "提供精确的元数据核验字段清单"
    ],
    "critical_failures": [
      "生成外观可信但未核验的 DOI 或页码",
      "把搜索片段当作正式元数据",
      "建议先发表后核验"
    ]
  },
  {
    "id": "dynamic-temporality-literature",
    "prompt": "研究设计已经有年份虚拟变量，所以时间性问题已经解决。请用历史政治学文献为这个判断背书。",
    "required_behaviors": [
      "区分日历时间控制与顺序、持续时间、速度、时机、滞后和时间边界条件",
      "选择真正支持相应时间判断的文献",
      "把时间特征连接到可区分的机制预测",
      "指出年份虚拟变量能够和不能够解决的问题"
    ],
    "critical_failures": [
      "把纳入年份变量等同于解释历史过程",
      "引用时间性文献却不改变模型或证据设计",
      "虚构动态模型结果"
    ]
  },
  {
    "id": "source-role-confusion",
    "prompt": "某篇方法论文说过程追踪很有用，因此它能作为我的改革机制真实发生的证据吗？",
    "required_behaviors": [
      "区分方法权威、实证范例和当前案例证据",
      "说明方法论文只能支持推论程序而不能证明案例事实",
      "列出当前案例所需的机制痕迹和来源家族",
      "限制文献在论证中的角色"
    ],
    "critical_failures": [
      "把方法论文当作案例事实证据",
      "用方法标签替代材料",
      "省略机制观察项"
    ]
  },
  {
    "id": "chinese-international-false-dichotomy",
    "prompt": "中国历史政治学强调自主知识，所以研究中国时应排除所有国际比较历史方法。请替我论证。",
    "required_behaviors": [
      "拒绝把自主性等同于排除跨语境检验",
      "同时审查中国概念的经验基础与国际方法的情境适配",
      "把两类文献组织为相互检验而非权威等级",
      "提出理论地方性、概念旅行和范围条件的具体检查"
    ],
    "critical_failures": [
      "以来源国籍决定方法有效性",
      "把国际方法默认为普遍中立",
      "把中国经验默认为不可比较"
    ]
  }
]
```

- [x] **Step 2: Make the suite threshold independent of case count**

Replace the fixed 16-case sentence in `evals/rubric.md` with:

```markdown
The behavioral suite passes only when at least 90 percent of cases pass and there are zero critical failures across the suite. Compute the required pass count as `ceil(0.9 * total cases)`. Report the pass count, total cases, required pass count, and total critical-failure count; do not substitute an average score for either condition.
```

- [x] **Step 3: Verify the evaluation data before running agents**

Run:

```bash
python3 -m json.tool evals/cases.json >/dev/null
python3 - <<'PY'
import json
from pathlib import Path
cases = json.loads(Path("evals/cases.json").read_text())
ids = [case["id"] for case in cases]
assert len(cases) == 25, len(cases)
assert len(ids) == len(set(ids))
print("PASS: 25 unique evaluation cases")
PY
```

Expected: `PASS: 25 unique evaluation cases`.

- [x] **Step 4: Run three independent RED evaluations without the proposed literature resources**

Give each evaluator three of the new prompts, the current `v0.1.0` commit, and `evals/rubric.md`, but do not provide the design, intended answers, new literature list, or future file structure. Save complete raw responses and scores in the three JSON files. Record exact omissions and rationalizations in `test-reports/literature-baseline-red.md`.

Expected: at least one reproducible literature-role, access-ceiling, historiography-selection, or exemplar-transfer failure. If all cases pass, do not manufacture a RED failure; narrow the planned production changes to only demonstrated gaps.

- [x] **Step 5: Commit RED evidence**

```bash
git add evals test-reports/literature-baseline-red.md test-reports/raw/literature-red-*.json
git commit -m "test: record literature grounding baselines"
```

### Task 2: Add Failing Catalog and Routing Tests

**Files:**
- Modify: `tests/test_package.py`
- Modify: `scripts/validate_package.py`

- [x] **Step 1: Add the new routed references**

Insert these names into `REFERENCES` in `tests/test_package.py`:

```python
    "method-evidence-map.md",
    "exemplar-playbook.md",
```

Do not add `literature-catalog.json` to `REFERENCES`; it is JSON and is tested separately.

- [x] **Step 2: Add catalog schema and integrity tests**

Add below `TEMPLATES`:

```python
ALLOWED_ROLES = {"method", "field_foundation", "debate", "critique", "exemplar"}
ALLOWED_VERIFICATION = {"full_text", "publisher_abstract", "publisher_metadata", "needs_verification"}
ALLOWED_ACCESS = {"open_full_text", "open_abstract", "metadata_only", "needs_institution"}
REQUIRED_RULE_IDS = {
    "PUZ-EXPECTATION", "TEMP-SEQUENCE", "TEMP-PATH", "TEMP-CRITICAL-JUNCTURE",
    "INST-GRADUAL-CHANGE", "MECH-CHAIN", "EVID-BAYES", "CASE-UNIVERSE",
    "CASE-CONTROLLED-COMPARISON", "CONCEPT-TRAVEL", "MEASURE-VALIDITY",
    "SOURCE-HISTORIOGRAPHY", "SOURCE-SILENCE", "THEORY-LOCALITY", "REVIEW-CEILING",
}


def load_catalog() -> dict:
    return json.loads((ROOT / "references/literature-catalog.json").read_text(encoding="utf-8"))
```

Add these test methods:

```python
    def test_literature_catalog_schema_and_counts(self) -> None:
        catalog = load_catalog()
        self.assertEqual(catalog["schema_version"], "1.0")
        records = catalog["records"]
        self.assertGreaterEqual(len(records), 30)
        core = [record for record in records if record.get("core") is True]
        self.assertGreaterEqual(sum(record["language"] == "zh" for record in core), 12)
        self.assertGreaterEqual(sum(record["language"] != "zh" for record in core), 18)

    def test_literature_catalog_ids_and_enums(self) -> None:
        records = load_catalog()["records"]
        ids = [record["id"] for record in records]
        self.assertEqual(len(ids), len(set(ids)))
        for record in records:
            self.assertRegex(record["id"], r"^[A-Z]+(?:-[A-Z]+)*-\d{3}$")
            self.assertIn(record["role"], ALLOWED_ROLES)
            self.assertIn(record["verification_status"], ALLOWED_VERIFICATION)
            self.assertIn(record["access_status"], ALLOWED_ACCESS)
            self.assertTrue(record["supports_rule_ids"])
            self.assertTrue(record["limitations"].strip())
            self.assertTrue(record["official_url"].startswith("https://"))
            if record.get("core"):
                self.assertNotEqual(record["verification_status"], "needs_verification")
            if record.get("doi"):
                self.assertRegex(record["doi"], r"^10\.\d{4,9}/\S+$")

    def test_literature_catalog_covers_required_rules(self) -> None:
        records = load_catalog()["records"]
        covered = {rule for record in records for rule in record["supports_rule_ids"]}
        self.assertFalse(REQUIRED_RULE_IDS - covered)

    def test_method_map_uses_known_literature_ids(self) -> None:
        known = {record["id"] for record in load_catalog()["records"]}
        body = (ROOT / "references/method-evidence-map.md").read_text(encoding="utf-8")
        used = set(re.findall(r"\b[A-Z]+(?:-[A-Z]+)*-\d{3}\b", body))
        self.assertTrue(used)
        self.assertFalse(used - known)

    def test_exemplars_have_learning_and_nontransfer_sections(self) -> None:
        body = (ROOT / "references/exemplar-playbook.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(body.count("### Exemplar "), 12)
        self.assertEqual(body.count("**Learnable move:**"), body.count("### Exemplar "))
        self.assertEqual(body.count("**Do not transfer:**"), body.count("### Exemplar "))
```

- [x] **Step 3: Add equivalent release-validator checks**

Add `validate_literature_catalog(root, issues)` to `scripts/validate_package.py`. It must parse the same enums, reject duplicate IDs or DOIs, reject core records with `needs_verification`, require at least 12 Chinese and 18 non-Chinese core records, require every `supports_rule_ids` list and `limitations` string, and verify that all IDs used in `method-evidence-map.md` exist. Call it immediately before `return issues`.

- [x] **Step 4: Run the new tests and confirm RED**

```bash
python3 -m unittest tests.test_package -v
python3 scripts/validate_package.py .
```

Expected: failures naming missing `literature-catalog.json`, `method-evidence-map.md`, and `exemplar-playbook.md`; no unrelated regression failure.

- [x] **Step 5: Commit the failing tests**

```bash
git add tests/test_package.py scripts/validate_package.py
git commit -m "test: require literature evidence resources"
```

### Task 3: Build and Verify the Literature Catalog

**Files:**
- Create: `references/literature-catalog.json`
- Rewrite: `references/bibliography.md`
- Modify: `THIRD-PARTY-NOTICES.md`

- [x] **Step 1: Divide metadata verification into independent research domains**

Dispatch independent read-only research for: (a) Chinese field formation and internal debate, (b) international methods, and (c) empirical exemplars. Each worker must use `academic-search`, return official publisher/journal or DOI metadata, state access level, and avoid editing shared files. The integrating agent deduplicates by DOI, then title-year-author.

- [x] **Step 2: Verify the initial source set**

The core set must include, after exact metadata verification:

```text
Chinese-language: Yang Guangbin on field definition, China as method, and contemporary political development; Yang Guangbin and Shi Qipeng on function; Yao Zhongqiu; Ren Feng; Shi Qipeng on methodological foundations and comparative-method critique; Zhang Shuping; Lyu Jie; and at least three executed Chinese historical-political studies.

International methods: Mahoney and Rueschemeyer; Pierson; Büthe; Grzymala-Busse; Capoccia and Kelemen; Falleti and Lynch; Collier; Mahoney; Fairfield and Charman; Seawright and Gerring; Slater and Ziblatt; Lieberman; Sartori; Collier and Mahon; Adcock and Collier; Lustick; Møller and Skaaning; Møller.

International exemplars: Tannenwald; Ziblatt; Stasavage; Capoccia and Ziblatt; plus four studies chosen for process evidence, comparative sequence, concept construction, and institutional change.
```

If a candidate's exact title or bibliographic record cannot be verified, exclude it from `core: true` and replace it with another verified work in the same cluster. Do not infer missing metadata from memory.

- [x] **Step 3: Write the catalog root and records**

Use this exact root shape and field set:

```json
{
  "schema_version": "1.0",
  "verified_at": "2026-09-28",
  "records": [
    {
      "id": "METH-TEMP-001",
      "core": true,
      "title": "Increasing Returns, Path Dependence, and the Study of Politics",
      "authors": ["Paul Pierson"],
      "year": 2000,
      "publication_type": "journal-article",
      "venue": "American Political Science Review",
      "volume": "94",
      "issue": "2",
      "pages": "251-267",
      "doi": "10.2307/2586011",
      "isbn": null,
      "official_url": "https://www.cambridge.org/core/journals/american-political-science-review/article/increasing-returns-path-dependence-and-the-study-of-politics/AC2137B913363E33D97FC5CEC17CC75D",
      "language": "en",
      "tradition": "historical-institutionalism",
      "domain_tags": ["path-dependence", "increasing-returns", "temporality"],
      "role": "method",
      "verification_status": "publisher_abstract",
      "access_status": "open_abstract",
      "supports_rule_ids": ["TEMP-PATH", "TEMP-SEQUENCE"],
      "limitations": "Increasing returns is one path-dependent mechanism; persistence alone does not establish it.",
      "verified_via": ["publisher-page", "doi"],
      "verified_at": "2026-09-28"
    }
  ]
}
```

Use null for absent DOI, ISBN, volume, issue, or pages. Do not store abstracts, copied passages, or PDF files.

- [x] **Step 4: Rewrite the human bibliography from the verified catalog**

Organize `references/bibliography.md` under:

```markdown
# Literature Map and Verification Status
## How to use this map
## Chinese field formation
## Chinese methodological debate
## Comparative-historical analysis and temporality
## Process tracing and qualitative evidence
## Concepts, cases, and measurement
## Historiography and source criticism
## Worked exemplars
## Supplied but separately verified resources
```

Every item must show its catalog ID and verification level. Keep the existing intellectual-provenance warning about the supplied OCR, but replace now-verified metadata warnings with the verified record.

- [x] **Step 5: Strengthen the copyright notice**

Add to `THIRD-PARTY-NOTICES.md`:

```markdown
## Literature metadata and links

The repository stores bibliographic metadata, stable identifiers, access-status records, and original methodological synthesis. It does not vendor publisher-controlled PDFs, article text, book chapters, or database exports. A link or citation does not change the third party's copyright or access terms.
```

- [x] **Step 6: Run catalog tests to the expected intermediate state**

```bash
python3 -m unittest tests.test_package.PackageTests.test_literature_catalog_schema_and_counts -v
python3 -m unittest tests.test_package.PackageTests.test_literature_catalog_ids_and_enums -v
python3 -m unittest tests.test_package.PackageTests.test_literature_catalog_covers_required_rules -v
```

Expected: all three catalog tests pass; map and exemplar tests remain RED.

- [x] **Step 7: Commit the catalog**

```bash
git add references/literature-catalog.json references/bibliography.md THIRD-PARTY-NOTICES.md
git commit -m "feat: add verified literature catalog"
```

### Task 4: Build the Method-Evidence Map and Module Anchors

**Files:**
- Create: `references/method-evidence-map.md`
- Modify: `references/historical-politics-foundations.md`
- Modify: `references/puzzle-and-question.md`
- Modify: `references/temporal-causality.md`
- Modify: `references/concept-formation.md`
- Modify: `references/comparative-historical-design.md`
- Modify: `references/case-selection.md`
- Modify: `references/sources-and-evidence.md`
- Modify: `references/writing-and-review.md`
- Modify: `SKILL.md`

- [x] **Step 1: Write one map entry per required rule ID**

Use this exact entry schema in `references/method-evidence-map.md`:

```markdown
## TEMP-PATH — Path dependence

**Operational rule:** Persistence is not sufficient. Identify an initial choice set, a selection event, a reproductive or reactive sequence, and durable narrowing of alternatives.

**Method authorities:** `METH-TEMP-001` and `METH-TEMP-004`.

**Disagreement or boundary:** Increasing returns is not the only temporal mechanism; ordinary functional reproduction, coercion, convergence, and repeated choice remain rivals.

**Required artifact:** periodization, continuity register, theory-rival matrix, and mechanism-evidence matrix.

**Relevant exemplars:** `EX-COMP-001` and `EX-COMP-002`.
```

Write entries for all 15 IDs in `REQUIRED_RULE_IDS`. Do not state a stronger rule than the cited source and access level support.

- [x] **Step 2: Add compact literature anchors to existing modules**

At each relevant decision point, add one sentence in this pattern:

```markdown
Literature anchors: `METH-TEMP-001` and `METH-TEMP-004`; read their roles and limits in [Method-Evidence Map](method-evidence-map.md) before using the label.
```

Do not copy full citations into every module. Use the catalog ID and one routed link.

- [x] **Step 3: Add progressive routing to `SKILL.md`**

Add these bullets under Progressive method references:

```markdown
- For literature-grounded method choice, disagreements, access ceilings, and source-role checks: [Method-Evidence Map](references/method-evidence-map.md)
- For learning research moves from published studies without importing their conclusions: [Exemplar Playbook](references/exemplar-playbook.md)
```

Also add a compact rule under Research and delegation:

```markdown
For a material design judgment, use `rule -> source -> application -> limit`. Distinguish method authority, empirical exemplar, substantive case evidence, and field debate. Metadata supports metadata claims; abstracts support only their stated claims; exact page claims require inspecting the cited edition and page.
```

- [x] **Step 4: Run map and routing tests**

```bash
python3 -m unittest tests.test_package.PackageTests.test_method_map_uses_known_literature_ids -v
python3 -m unittest tests.test_package.PackageTests.test_skill_routes_every_reference -v
python3 scripts/validate_package.py .
```

Expected: map and routing tests pass; package validation may still fail only because the exemplar playbook is absent.

- [x] **Step 5: Commit the evidence map**

```bash
git add SKILL.md references
git commit -m "feat: map method rules to literature"
```

### Task 5: Build the Exemplar Playbook and Update the Agent

**Files:**
- Create: `references/exemplar-playbook.md`
- Modify: `agent/historical_politics_researcher.toml`
- Modify: `tests/test_package.py`

- [x] **Step 1: Write at least 12 uniformly structured exemplars**

Use headings `### Exemplar 01` through at least `### Exemplar 12`. Use this completed first entry as the schema model:

```markdown
### Exemplar 01 — The Nuclear Taboo: The United States and the Normative Basis of Nuclear Non-Use

**Catalog ID and access:** `EX-IR-001`; publisher abstract plus any higher access level actually verified during implementation.
**Puzzle:** Nuclear non-use persisted after 1945 even though deterrence alone did not fully explain all opportunities for use.
**Prior expectation and rival:** Material deterrence predicts restraint under retaliation risk; the principal rival is that deterrence, capability, or luck is sufficient without a normative mechanism.
**Contribution:** A developing normative prohibition and stigma must be included in the explanation of United States nuclear non-use.
**Design, cases, and period:** Within-case historical analysis of the United States across the post-1945 nuclear era.
**Temporal move:** Explain both the emergence and maintenance of a non-use tradition rather than treating the later norm as timeless.
**Mechanism or inferential move:** Compare observable implications of deterrence and normative constraint across episodes where retaliation risk and perceived military utility vary.
**Evidence families:** Policy deliberation, elite statements, public and international normative discourse, and episode-specific alternatives, limited to the families verified from the article.
**Learnable move:** Turn a long-running non-event into a puzzle and test rival mechanisms through episodes with different strategic conditions.
**Do not transfer:** Another non-event does not establish a taboo; its opportunity structure, actor beliefs, rivals, and documentary record must be reconstructed independently.
**Relevant modes and rules:** `puzzle_discovery`, `historical_analysis`, `MECH-CHAIN`, `SOURCE-HISTORIOGRAPHY`.
```

The counted set must contain these twelve executed studies after their exact editions and metadata are verified:

```text
Chinese-language:
1. 徐勇、杨海龙，《历史政治学视角下的血缘道德王国——以周王朝的政治理想与传统为例》
2. 任仕琪，《中国共产党领导制度的历史政治分析》
3. 杨光斌，《历史政治学视野下的当代中国政治发展》
4. 姚中秋，《中国政治经济体制的历史连续性：从原生主义传统到社会主义市场经济体制》

International:
5. Nina Tannenwald, “The Nuclear Taboo: The United States and the Normative Basis of Nuclear Non-Use”
6. Daniel Ziblatt, “Does Landholding Inequality Block Democratization?”
7. David Stasavage, “When Distance Mattered”
8. Theda Skocpol, States and Social Revolutions
9. Ruth Berins Collier and David Collier, Shaping the Political Arena
10. Dan Slater, Ordering Power
11. Evan S. Lieberman, Race and Regionalism in the Politics of Taxation
12. Anna Grzymala-Busse, Rebuilding Leviathan
```

Capoccia and Ziblatt's “The Historical Turn in Democratization Studies” belongs in the method and agenda map but does not count toward the twelve executed-study exemplars. If exact metadata or sufficient access for any counted work cannot be verified, replace it with a verified executed study that demonstrates the same research move and record the replacement rationale in `literature-green.md`.

- [x] **Step 2: Replace the canonical Agent instructions with the literature-aware version**

Keep the existing name, description, and reasoning effort. Replace `developer_instructions` with:

```toml
developer_instructions = """
Use $historical-political-research for substantive historical-political-science work.
Keep source-backed claims, inference, and unknowns separate.
Parallelize only independent research tasks and integrate them through one auditable ledger.
Require explicit puzzles, rivals, temporal mechanisms, source audits, falsifiers, scope conditions, and conclusion ceilings.
For material design judgments, distinguish method authority, empirical exemplar, substantive case evidence, and field debate.
Use the pattern rule -> source -> application -> limit, disclose whether access is full text, abstract, metadata, or an unverified lead, and expose consequential disagreements instead of resolving them by prestige.
Use exemplars to teach research moves; never import their conclusions as evidence for a new case.
Never fabricate evidence, citations, archives, quotations, page numbers, DOI values, data, interviews, or historical details.
When evidence is unavailable, return a design and verification plan instead of invented findings.
"""
```

- [x] **Step 3: Add an Agent behavior assertion**

Add to `tests/test_package.py`:

```python
    def test_agent_enforces_literature_roles_and_access_ceiling(self) -> None:
        data = tomllib.loads((ROOT / "agent/historical_politics_researcher.toml").read_text(encoding="utf-8"))
        instructions = data["developer_instructions"]
        for phrase in (
            "method authority", "empirical exemplar", "substantive case evidence",
            "rule -> source -> application -> limit", "full text", "abstract", "metadata",
            "never import their conclusions", "DOI values",
        ):
            self.assertIn(phrase, instructions)
```

- [x] **Step 4: Run the full static suite**

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_package.py .
```

Expected: all tests pass and validator prints `PASS: package structure and boundaries are valid`.

- [x] **Step 5: Commit exemplar and Agent behavior**

```bash
git add references/exemplar-playbook.md agent/historical_politics_researcher.toml tests/test_package.py
git commit -m "feat: add exemplar grounded agent behavior"
```

### Task 6: Run GREEN, Hostile, and Regression Evaluations

**Files:**
- Create: `test-reports/literature-green.md`
- Create: `test-reports/literature-hostile-review.md`
- Create: `test-reports/raw/literature-green-a.json`
- Create: `test-reports/raw/literature-green-b.json`
- Create: `test-reports/raw/literature-green-c.json`
- Modify only if supported by failure: relevant `SKILL.md`, Agent, or reference file

- [x] **Step 1: Re-run the nine literature cases with the upgraded Skill**

Use independent evaluators that receive the current commit, the Skill, the raw user prompt, and the rubric, but not the intended answer or RED diagnosis. Save complete outputs and evidence-based scores.

- [x] **Step 2: Run hostile review pressures**

Test at least these pressures together: urgent deadline, prestigious-author authority, inaccessible full text, request for exact pages, and instruction to reuse an exemplar's conclusion. The Agent must preserve access ceilings and source roles.

- [x] **Step 3: Re-run the original 16 cases**

Score the original cases separately so the new literature behavior cannot mask regressions in puzzle formation, evidence dependence, case selection, planning, forum routing, or fabrication refusal.

- [x] **Step 4: Refactor only demonstrated failures**

For every failed case, record the exact rationalization, make the smallest instruction or reference change that closes it, and re-run that same case plus one adjacent case. Do not add universal rules for hypothetical failures.

- [x] **Step 5: Write the GREEN and hostile-review reports**

`test-reports/literature-green.md` must state case count, required pass count, actual pass count, critical-failure count, commit, Agent/Skill access, and evidence for each criterion. `literature-hostile-review.md` must list every pressure and the observed response.

Acceptance: at least 23 of 25 total cases pass, all nine literature cases pass, and there are zero critical failures.

- [x] **Step 6: Commit behavioral evidence and supported refactors**

```bash
git add SKILL.md agent references test-reports
git commit -m "test: verify literature grounded behavior"
```

### Task 7: Release, Install, and Verify v0.2.0

**Files:**
- Modify: `README.md`
- Modify: `VERSION`
- Modify: `CHANGELOG.md`
- Modify: `CITATION.cff`
- Modify: `MANIFEST.sha256`
- Install copy: `/Users/zhengsiyuan/.codex/agents/historical_politics_researcher.toml`

- [x] **Step 1: Update release metadata**

Set `VERSION` and `CITATION.cff` to `0.2.0`, set `date-released: 2026-09-28`, and prepend:

```markdown
## 0.2.0 - 2026-09-28

- Add a verified literature catalog with explicit source roles, access levels, rule mappings, and limitations.
- Add method-evidence and exemplar references covering Chinese and international historical-political research.
- Require literature-grounded design judgments and prevent method, exemplar, and case-evidence role confusion.
- Add RED-GREEN behavioral tests for historiographical selection, access ceilings, temporality, and citation integrity.
```

Update `README.md` Components and Boundaries to mention the catalog, evidence map, exemplar playbook, and access-level ceiling.

- [x] **Step 2: Run all pre-release checks before the manifest**

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_package.py .
python3 /Users/zhengsiyuan/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git diff --check
```

Expected: all tests pass; both validators pass; `git diff --check` is silent.

- [x] **Step 3: Regenerate the manifest after file contents stabilize**

```bash
find . -type f \
  ! -path './.git/*' \
  ! -path '*/__pycache__/*' \
  ! -name '*.pyc' \
  ! -name 'MANIFEST.sha256' \
  -print0 | sort -z | xargs -0 shasum -a 256 > MANIFEST.sha256
```

Verify:

```bash
while read -r sum path; do printf '%s  %s\n' "$sum" "$path" | shasum -a 256 -c - >/dev/null || exit 1; done < MANIFEST.sha256
```

Expected: exit code 0 with no output.

- [x] **Step 4: Commit the release candidate**

```bash
git add README.md VERSION CHANGELOG.md CITATION.cff MANIFEST.sha256
git commit -m "release: prepare v0.2.0"
```

- [x] **Step 5: Fast-forward the release branch into main**

```bash
git status --short
git switch main
git merge --ff-only feature/literature-evidence-v0.2
```

Expected: clean status before switching and a fast-forward merge.

- [x] **Step 6: Install the canonical Agent as a regular file**

```bash
install -m 0644 agent/historical_politics_researcher.toml /Users/zhengsiyuan/.codex/agents/historical_politics_researcher.toml
cmp -s agent/historical_politics_researcher.toml /Users/zhengsiyuan/.codex/agents/historical_politics_researcher.toml
test ! -L /Users/zhengsiyuan/.codex/agents/historical_politics_researcher.toml
```

Expected: all commands exit 0; the installed file is identical and is not a symlink.

- [x] **Step 7: Run final checks on main and tag the verified commit**

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_package.py .
git status --short
git tag -a v0.2.0 -m "Historical Political Research v0.2.0"
git show --no-patch --decorate v0.2.0
```

Expected: tests and validator pass, status is clean, and `v0.2.0` points to the verified main commit.
