#!/usr/bin/env python3
"""Validate package structure, metadata, links, and copyright boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import tomllib
from datetime import date
from pathlib import Path


REQUIRED = [
    "SKILL.md",
    "LICENSE",
    "THIRD-PARTY-NOTICES.md",
    "CITATION.cff",
    "VERSION",
    "agent/historical_politics_researcher.toml",
    "agents/openai.yaml",
    "scripts/validate_behavior_reports.py",
]

ALLOWED_AGENT_FIELDS = {
    "name",
    "description",
    "developer_instructions",
    "model",
    "model_reasoning_effort",
    "sandbox_mode",
}

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

LITERATURE_ID_PATTERN = re.compile(r"^[A-Z]+(?:-[A-Z]+)*-\d{3}$")
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$")
LITERATURE_ID_LIKE_PATTERN = re.compile(r"(?<![\w-])[A-Za-z]+(?:-[A-Za-z]+)+-\d+(?![\w-])")

REQUIRED_CATALOG_FIELDS = {
    "id", "core", "title", "authors", "year", "publication_type", "venue",
    "volume", "issue", "pages", "doi", "isbn", "official_url", "language",
    "tradition", "domain_tags", "role", "verification_status", "access_status",
    "supports_rule_ids", "limitations", "verified_via", "verified_at",
}
NULLABLE_STRING_FIELDS = {"volume", "issue", "pages", "doi", "isbn"}
NONEMPTY_STRING_FIELDS = {
    "title", "publication_type", "venue", "language", "tradition", "limitations",
    "official_url", "verified_at",
}


def extract_literature_id_tokens(body: str) -> tuple[set[str], set[str]]:
    """Return valid catalog IDs and ID-like typos without matching ordinary hyphenated prose."""
    candidates = set(LITERATURE_ID_LIKE_PATTERN.findall(body))
    valid = {token for token in candidates if LITERATURE_ID_PATTERN.fullmatch(token)}
    return valid, candidates - valid


def exemplar_blocks(body: str) -> list[str]:
    return [
        block
        for block in re.split(r"(?m)(?=^### Exemplar )", body)
        if block.startswith("### Exemplar ")
    ]


def validate_catalog_records(
    records: list[dict], catalog_verified_at: str, issues: list[str], *, require_rule_coverage: bool = True
) -> None:
    """Validate catalog records using package's canonical schema and integrity rules."""
    try:
        catalog_date = date.fromisoformat(catalog_verified_at)
    except (TypeError, ValueError):
        issues.append("literature catalog verified_at must be an ISO date")
        catalog_date = date.min
    known_ids: set[str] = set()
    seen_dois: set[str] = set()
    covered_rules: set[str] = set()
    chinese_core = non_chinese_core = 0
    for index, record in enumerate(records):
        label = f"literature catalog record {index + 1}"
        missing = sorted(REQUIRED_CATALOG_FIELDS - set(record))
        if missing:
            issues.append(f"{label} missing required fields: {', '.join(missing)}")
        for field in NONEMPTY_STRING_FIELDS:
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                issues.append(f"{label} {field} must be a non-empty string")
        for field in NULLABLE_STRING_FIELDS:
            value = record.get(field)
            if value is not None and not isinstance(value, str):
                issues.append(f"{label} {field} must be a string or null")
        for field in ("authors", "domain_tags", "verified_via"):
            value = record.get(field)
            if not isinstance(value, list) or not value or not all(isinstance(x, str) and x.strip() for x in value):
                issues.append(f"{label} {field} must be a non-empty list of strings")
        if not isinstance(record.get("core"), bool):
            issues.append(f"{label} core must be boolean")
        year = record.get("year")
        if not isinstance(year, int) or isinstance(year, bool) or not 1800 <= year <= catalog_date.year:
            issues.append(f"{label} year must be an integer from 1800 through {catalog_date.year}")
        try:
            verified_date = date.fromisoformat(record.get("verified_at", ""))
            if verified_date > catalog_date:
                issues.append(f"{label} verified_at exceeds catalog verified_at")
        except (TypeError, ValueError):
            issues.append(f"{label} verified_at must be an ISO date")

        record_id = record.get("id")
        if not isinstance(record_id, str) or not LITERATURE_ID_PATTERN.fullmatch(record_id):
            issues.append(f"{label} has invalid id")
        elif record_id in known_ids:
            issues.append(f"duplicate literature id: {record_id}")
        else:
            known_ids.add(record_id)
        if record.get("role") not in ALLOWED_ROLES:
            issues.append(f"{label} has invalid role")
        verification = record.get("verification_status")
        if verification not in ALLOWED_VERIFICATION:
            issues.append(f"{label} has invalid verification_status")
        if record.get("access_status") not in ALLOWED_ACCESS:
            issues.append(f"{label} has invalid access_status")
        supports = record.get("supports_rule_ids")
        if not isinstance(supports, list) or not supports or not all(isinstance(x, str) and x.strip() for x in supports):
            issues.append(f"{label} must have a non-empty supports_rule_ids list")
        else:
            covered_rules.update(supports)
            unknown = sorted(set(supports) - REQUIRED_RULE_IDS)
            if unknown:
                issues.append(f"{label} has unknown supports_rule_ids: {', '.join(unknown)}")
        url = record.get("official_url")
        if not isinstance(url, str) or not url.startswith("https://"):
            issues.append(f"{label} must have an https official_url")
        doi = record.get("doi")
        if doi:
            if not DOI_PATTERN.fullmatch(doi):
                issues.append(f"{label} has invalid doi")
            elif doi.casefold() in seen_dois:
                issues.append(f"duplicate literature doi: {doi}")
            else:
                seen_dois.add(doi.casefold())
        if record.get("core") is True:
            if verification == "needs_verification":
                issues.append(f"{label} is core but needs verification")
            chinese_core += record.get("language") == "zh"
            non_chinese_core += record.get("language") != "zh"
    if require_rule_coverage:
        if chinese_core < 12:
            issues.append(f"literature catalog has {chinese_core} Chinese core records; requires 12")
        if non_chinese_core < 18:
            issues.append(f"literature catalog has {non_chinese_core} non-Chinese core records; requires 18")
        missing_rules = sorted(REQUIRED_RULE_IDS - covered_rules)
        if missing_rules:
            issues.append("literature catalog does not cover required rules: " + ", ".join(missing_rules))


def validate_literature_catalog(root: Path, issues: list[str]) -> None:
    catalog_path = root / "references/literature-catalog.json"
    method_map_path = root / "references/method-evidence-map.md"
    exemplar_path = root / "references/exemplar-playbook.md"

    records: list[dict] = []
    catalog_records_available = False
    catalog_verified_at = ""
    if not catalog_path.is_file():
        issues.append("missing references/literature-catalog.json")
    else:
        try:
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            issues.append(f"invalid literature catalog: {exc}")
        else:
            if not isinstance(catalog, dict):
                issues.append("literature catalog root must be an object")
            else:
                if catalog.get("schema_version") != "1.0":
                    issues.append("literature catalog schema_version must be 1.0")
                catalog_verified_at = catalog.get("verified_at", "")
                raw_records = catalog.get("records")
                if not isinstance(raw_records, list):
                    issues.append("literature catalog records must be a list")
                else:
                    catalog_records_available = True
                    records = [record for record in raw_records if isinstance(record, dict)]
                    if len(records) != len(raw_records):
                        issues.append("literature catalog records must be objects")

    if catalog_records_available:
        validate_catalog_records(records, catalog_verified_at, issues)
    known_ids = {record.get("id") for record in records if isinstance(record.get("id"), str)}

    if not method_map_path.is_file():
        issues.append("missing references/method-evidence-map.md")
    else:
        used_ids, malformed_ids = extract_literature_id_tokens(method_map_path.read_text(encoding="utf-8"))
        if not used_ids:
            issues.append("method-evidence-map.md must cite at least one literature id")
        if malformed_ids:
            issues.append("method-evidence-map.md has malformed literature ids: " + ", ".join(sorted(malformed_ids)))
        if catalog_records_available:
            unknown_ids = sorted(used_ids - known_ids)
            if unknown_ids:
                issues.append("method-evidence-map.md uses unknown literature ids: " + ", ".join(unknown_ids))

    if not exemplar_path.is_file():
        issues.append("missing references/exemplar-playbook.md")
    else:
        exemplar_body = exemplar_path.read_text(encoding="utf-8")
        blocks = exemplar_blocks(exemplar_body)
        if len(blocks) < 12:
            issues.append("exemplar-playbook.md must contain at least 12 exemplars")
        for index, block in enumerate(blocks, start=1):
            if block.count("**Learnable move:**") != 1:
                issues.append(f"exemplar {index} must contain exactly one Learnable move section")
            if block.count("**Do not transfer:**") != 1:
                issues.append(f"exemplar {index} must contain exactly one Do not transfer section")


def validate(root: Path) -> list[str]:
    issues: list[str] = []
    for name in REQUIRED:
        if not (root / name).is_file():
            issues.append(f"missing {name}")
    if issues:
        return issues

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n") or "name: historical-political-research" not in skill:
        issues.append("SKILL.md has invalid or missing frontmatter")
    if "description: Use when" not in skill:
        issues.append("SKILL.md description must begin with Use when")

    agent = tomllib.loads((root / "agent/historical_politics_researcher.toml").read_text(encoding="utf-8"))
    for key in ("name", "description", "developer_instructions"):
        if not agent.get(key):
            issues.append(f"Agent TOML missing {key}")
    unknown_agent_fields = sorted(set(agent) - ALLOWED_AGENT_FIELDS)
    if unknown_agent_fields:
        issues.append(f"Agent TOML has unsupported fields: {', '.join(unknown_agent_fields)}")
    if agent.get("name") != "historical_politics_researcher":
        issues.append("Agent TOML has unexpected name")

    ui = (root / "agents/openai.yaml").read_text(encoding="utf-8")
    for needle in (
        "interface:",
        "display_name:",
        "short_description:",
        "default_prompt:",
        "$historical-political-research",
        "policy:",
        "allow_implicit_invocation: true",
    ):
        if needle not in ui:
            issues.append(f"agents/openai.yaml missing {needle}")

    citation = (root / "CITATION.cff").read_text(encoding="utf-8")
    for needle in ("cff-version: 1.2.0", "title:", "authors:", "version:", "license: MIT"):
        if needle not in citation:
            issues.append(f"CITATION.cff missing {needle}")
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if f"version: {version}" not in citation:
        issues.append("CITATION.cff version does not match VERSION")

    skill_links = re.findall(r"\[[^]]+\]\(([^)]+)\)", skill)
    for link in skill_links:
        if link.startswith(("http://", "https://", "#")):
            continue
        if not (root / link).exists():
            issues.append(f"broken Skill link: {link}")
    for required_route in (
        "references/method-evidence-map.md",
        "references/exemplar-playbook.md",
    ):
        if required_route not in skill_links:
            issues.append(f"SKILL.md missing required route: {required_route}")

    metadata_path = root / "assets/templates/project-metadata.json"
    if metadata_path.exists():
        try:
            json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(f"invalid project metadata template: {exc}")

    for path in (root / "assets/templates").glob("*.csv") if (root / "assets/templates").exists() else []:
        with path.open(encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle), [])
        if len(header) < 3 or any(not cell.strip() for cell in header):
            issues.append(f"invalid CSV header: {path.relative_to(root)}")

    forbidden_book_names = [
        path for path in root.rglob("*.md")
        if path.stat().st_size > 200_000 and "docs/superpowers" not in str(path)
    ]
    if forbidden_book_names:
        issues.append("possible copyrighted full-text inclusion: " + ", ".join(str(p) for p in forbidden_book_names))
    validate_literature_catalog(root, issues)
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    issues = validate(root)
    if issues:
        for issue in issues:
            print(f"BLOCK: {issue}")
        return 1
    print("PASS: package structure and boundaries are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
