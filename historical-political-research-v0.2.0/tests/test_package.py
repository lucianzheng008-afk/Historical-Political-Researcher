from __future__ import annotations

import csv
import json
import re
import tempfile
import tomllib
import unittest
from copy import deepcopy
from pathlib import Path

from scripts import validate_package


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "THIRD-PARTY-NOTICES.md",
    "CITATION.cff",
    "VERSION",
    "CHANGELOG.md",
    "agent/historical_politics_researcher.toml",
    "agents/openai.yaml",
    "scripts/validate_behavior_reports.py",
]

REFERENCES = [
    "historical-politics-foundations.md",
    "puzzle-and-question.md",
    "temporal-causality.md",
    "concept-formation.md",
    "comparative-historical-design.md",
    "case-selection.md",
    "sources-and-evidence.md",
    "writing-and-review.md",
    "quality-gates.md",
    "bibliography.md",
    "method-evidence-map.md",
    "exemplar-playbook.md",
    "venue-adapters/ruc-forum-2026.md",
]

TEMPLATES = [
    "project-metadata.json",
    "domain-brief.md",
    "puzzle-register.csv",
    "question-cards.md",
    "concept-register.csv",
    "continuity-register.csv",
    "theory-rival-matrix.csv",
    "case-universe.csv",
    "case-selection-memo.md",
    "periodization.csv",
    "mechanism-evidence-matrix.csv",
    "source-register.csv",
    "source-dependence-matrix.csv",
    "evidence-register.csv",
    "timeline.csv",
    "claim-register.csv",
    "research-plan.md",
    "review-report.md",
]

ALLOWED_ROLES = {"method", "field_foundation", "debate", "critique", "exemplar"}
ALLOWED_VERIFICATION = {"full_text", "publisher_abstract", "publisher_metadata", "needs_verification"}
ALLOWED_ACCESS = {"open_full_text", "open_abstract", "metadata_only", "needs_institution"}
REQUIRED_RULE_IDS = {
    "PUZ-EXPECTATION",
    "TEMP-SEQUENCE",
    "TEMP-PATH",
    "TEMP-CRITICAL-JUNCTURE",
    "INST-GRADUAL-CHANGE",
    "MECH-CHAIN",
    "EVID-BAYES",
    "CASE-UNIVERSE",
    "CASE-CONTROLLED-COMPARISON",
    "CONCEPT-TRAVEL",
    "MEASURE-VALIDITY",
    "SOURCE-HISTORIOGRAPHY",
    "SOURCE-SILENCE",
    "THEORY-LOCALITY",
    "REVIEW-CEILING",
}


def load_catalog(testcase: unittest.TestCase) -> dict:
    path = ROOT / "references/literature-catalog.json"
    testcase.assertTrue(path.is_file(), "missing references/literature-catalog.json")
    return json.loads(path.read_text(encoding="utf-8"))


def exemplar_blocks(body: str) -> list[str]:
    return [
        block
        for block in re.split(r"(?m)(?=^### Exemplar )", body)
        if block.startswith("### Exemplar ")
    ]


class PackageTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        for name in REQUIRED_FILES:
            self.assertTrue((ROOT / name).is_file(), name)

    def test_agent_has_only_supported_core_fields(self) -> None:
        path = ROOT / "agent/historical_politics_researcher.toml"
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        for key in ["name", "description", "developer_instructions"]:
            self.assertIn(key, data)
        self.assertEqual(data["name"], "historical_politics_researcher")
        self.assertNotIn("nickname_candidates", data)

    def test_agent_enforces_literature_roles_and_access_ceiling(self) -> None:
        body = (ROOT / "agent/historical_politics_researcher.toml").read_text(encoding="utf-8")
        for phrase in [
            "method authority",
            "empirical exemplar",
            "substantive case evidence",
            "rule -> source -> application -> limit",
            "full text",
            "abstract",
            "metadata",
            "never import their conclusions",
            "DOI values",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, body)

    def test_version_is_semver(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")

    def test_all_references_and_templates_exist(self) -> None:
        for name in REFERENCES:
            with self.subTest(reference=name):
                self.assertTrue((ROOT / "references" / name).is_file(), name)
        for name in TEMPLATES:
            with self.subTest(template=name):
                self.assertTrue((ROOT / "assets/templates" / name).is_file(), name)

    def test_project_metadata_is_valid_json(self) -> None:
        path = ROOT / "assets/templates/project-metadata.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for key in ["project_id", "task", "target_output", "language", "uncertainty_policy"]:
            self.assertIn(key, data)

    def test_csv_templates_have_headers(self) -> None:
        for name in TEMPLATES:
            if not name.endswith(".csv"):
                continue
            path = ROOT / "assets/templates" / name
            with path.open(encoding="utf-8", newline="") as handle:
                header = next(csv.reader(handle))
            self.assertGreaterEqual(len(header), 3, name)
            self.assertTrue(all(cell.strip() for cell in header), name)

    def test_skill_routes_every_reference(self) -> None:
        body = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        linked = set(re.findall(r"references/([A-Za-z0-9_./-]+\.md)", body))
        self.assertEqual(set(REFERENCES), linked)

    def test_skill_ui_prompt_invokes_skill(self) -> None:
        body = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$historical-political-research", body)
        self.assertIn("allow_implicit_invocation: true", body)

    def test_skill_description_does_not_claim_general_history_queries(self) -> None:
        body = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        description = next(line for line in body.splitlines() if line.startswith("description:"))
        self.assertNotIn("or historical research", description)

    def test_literature_catalog_schema_and_counts(self) -> None:
        catalog = load_catalog(self)
        issues: list[str] = []
        validate_package.validate_catalog_records(
            catalog["records"], catalog["verified_at"], issues
        )
        self.assertEqual([], issues)
        self.assertEqual(catalog["schema_version"], "1.0")
        records = catalog["records"]
        self.assertGreaterEqual(len(records), 30)
        core = [record for record in records if record.get("core") is True]
        self.assertGreaterEqual(sum(record["language"] == "zh" for record in core), 12)
        self.assertGreaterEqual(sum(record["language"] != "zh" for record in core), 18)

    def test_literature_catalog_schema_rejects_bad_records(self) -> None:
        catalog = load_catalog(self)
        base = catalog["records"][0]
        mutations = {
            "missing title": lambda record: record.pop("title"),
            "wrong domain_tags type": lambda record: record.__setitem__("domain_tags", "history"),
            "year outside range": lambda record: record.__setitem__("year", 1799),
            "empty authors": lambda record: record.__setitem__("authors", []),
            "missing verified_at": lambda record: record.pop("verified_at"),
            "empty verified_via": lambda record: record.__setitem__("verified_via", []),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                record = deepcopy(base)
                mutate(record)
                issues: list[str] = []
                validate_package.validate_catalog_records(
                    [record], catalog["verified_at"], issues, require_rule_coverage=False
                )
                self.assertTrue(issues, label)

    def test_literature_catalog_ids_and_enums(self) -> None:
        records = load_catalog(self)["records"]
        ids = [record["id"] for record in records]
        self.assertEqual(len(ids), len(set(ids)))
        dois = [record["doi"].casefold() for record in records if record.get("doi")]
        self.assertEqual(len(dois), len(set(dois)), "DOIs must be unique ignoring case")
        for record in records:
            self.assertRegex(record["id"], r"^[A-Z]+(?:-[A-Z]+)*-\d{3}$")
            self.assertIn(record["role"], ALLOWED_ROLES)
            self.assertIn(record["verification_status"], ALLOWED_VERIFICATION)
            self.assertIn(record["access_status"], ALLOWED_ACCESS)
            supports = record["supports_rule_ids"]
            self.assertIsInstance(supports, list)
            self.assertTrue(supports)
            self.assertTrue(all(isinstance(rule, str) and rule.strip() for rule in supports))
            self.assertFalse(set(supports) - REQUIRED_RULE_IDS)
            self.assertTrue(record["limitations"].strip())
            self.assertTrue(record["official_url"].startswith("https://"))
            if record.get("core"):
                self.assertNotEqual(record["verification_status"], "needs_verification")
            if record.get("doi"):
                self.assertRegex(record["doi"], r"^10\.\d{4,9}/\S+$")

    def test_literature_catalog_covers_required_rules(self) -> None:
        records = load_catalog(self)["records"]
        covered = {rule for record in records for rule in record["supports_rule_ids"]}
        self.assertFalse(REQUIRED_RULE_IDS - covered)

    def test_method_map_uses_known_literature_ids(self) -> None:
        known = {record["id"] for record in load_catalog(self)["records"]}
        path = ROOT / "references/method-evidence-map.md"
        self.assertTrue(path.is_file(), "missing references/method-evidence-map.md")
        body = path.read_text(encoding="utf-8")
        used, malformed = validate_package.extract_literature_id_tokens(body)
        self.assertTrue(used)
        self.assertFalse(used - known)
        self.assertFalse(malformed, f"malformed literature ids: {sorted(malformed)}")

    def test_method_map_id_detection_rejects_id_like_typos(self) -> None:
        valid, malformed = validate_package.extract_literature_id_tokens(
            "Valid METH-TEMP-001; bad METH-TEMP-01 and meth-temp-001; ordinary path-dependent."
        )
        self.assertEqual(valid, {"METH-TEMP-001"})
        self.assertEqual(malformed, {"METH-TEMP-01", "meth-temp-001"})

    def test_validator_enforces_doi_and_rule_contracts(self) -> None:
        records = [
            {
                "id": "METH-TEMP-001",
                "role": "method",
                "verification_status": "publisher_metadata",
                "access_status": "metadata_only",
                "supports_rule_ids": ["TEMP-SEQUENCE"],
                "limitations": "Scope limited.",
                "official_url": "https://example.test/a",
                "doi": "10.1234/AbC",
                "core": False,
                "language": "en",
            },
            {
                "id": "METH-TEMP-002",
                "role": "method",
                "verification_status": "publisher_metadata",
                "access_status": "metadata_only",
                "supports_rule_ids": ["UNKNOWN-RULE"],
                "limitations": "Scope limited.",
                "official_url": "https://example.test/b",
                "doi": "10.1234/aBc",
                "core": False,
                "language": "en",
            },
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            references = root / "references"
            references.mkdir()
            (references / "literature-catalog.json").write_text(
                json.dumps({"schema_version": "1.0", "records": records}), encoding="utf-8"
            )
            (references / "method-evidence-map.md").write_text("METH-TEMP-001", encoding="utf-8")
            (references / "exemplar-playbook.md").write_text("", encoding="utf-8")
            issues: list[str] = []
            validate_package.validate_literature_catalog(root, issues)
        self.assertTrue(any("duplicate literature doi" in issue for issue in issues))
        self.assertTrue(any("unknown supports_rule_ids" in issue for issue in issues))

    def test_exemplars_have_learning_and_nontransfer_sections(self) -> None:
        path = ROOT / "references/exemplar-playbook.md"
        self.assertTrue(path.is_file(), "missing references/exemplar-playbook.md")
        blocks = exemplar_blocks(path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(blocks), 12)
        for index, block in enumerate(blocks, start=1):
            self.assertEqual(block.count("**Learnable move:**"), 1, f"Exemplar {index}")
            self.assertEqual(block.count("**Do not transfer:**"), 1, f"Exemplar {index}")


if __name__ == "__main__":
    unittest.main()
