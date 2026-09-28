#!/usr/bin/env python3
"""Validate a historical-political-research project and its stable IDs."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from audit_claims import ALLOWED_NECESSARY, ALLOWED_STEP_STATUS, audit, split_ids


REQUIRED = {
    "project-metadata.json": None,
    "puzzle-register.csv": "puzzle_id",
    "theory-rival-matrix.csv": "explanation_id",
    "mechanism-evidence-matrix.csv": "step_id",
    "source-register.csv": "source_id",
    "source-dependence-matrix.csv": None,
    "evidence-register.csv": "evidence_id",
    "claim-register.csv": "claim_id",
}

METADATA_KEYS = {"project_id", "task", "target_output", "language", "uncertainty_policy"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate(project: Path) -> list[str]:
    issues: list[str] = []
    for filename in REQUIRED:
        if not (project / filename).is_file():
            issues.append(f"missing required file {filename}")
    if issues:
        return issues

    try:
        metadata = json.loads((project / "project-metadata.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        issues.append(f"invalid project-metadata.json: {exc}")
        metadata = {}
    missing_keys = sorted(METADATA_KEYS - set(metadata))
    if missing_keys:
        issues.append(f"project metadata missing keys: {', '.join(missing_keys)}")

    for filename, id_field in REQUIRED.items():
        if not filename.endswith(".csv") or id_field is None:
            continue
        rows = read_rows(project / filename)
        seen: set[str] = set()
        for row in rows:
            value = row.get(id_field, "").strip()
            if not value:
                issues.append(f"{filename}: blank {id_field}")
            elif value in seen:
                issues.append(f"{filename}: duplicate {id_field} {value}")
            seen.add(value)

    explanation_roles = {
        row.get("role", "").strip().lower()
        for row in read_rows(project / "theory-rival-matrix.csv")
    }
    if "focal" not in explanation_roles:
        issues.append("theory-rival-matrix.csv: missing focal explanation")
    if "rival" not in explanation_roles:
        issues.append("theory-rival-matrix.csv: missing rival explanation")

    allowed_access = {"metadata", "abstract", "full-text", "primary-record", "stipulated", "unavailable"}
    for row in read_rows(project / "source-register.csv"):
        if row.get("access_status", "").strip().lower() not in allowed_access:
            issues.append(f"source-register.csv: invalid access status for {row.get('source_id')}")

    allowed_evidence = {"found", "not-found", "conflicted", "unavailable", "stipulated"}
    evidence_rows = read_rows(project / "evidence-register.csv")
    evidence_ids = {row.get("evidence_id", "").strip() for row in evidence_rows}
    proposition_ids = {row.get("proposition_id", "").strip() for row in evidence_rows}
    source_rows = read_rows(project / "source-register.csv")
    source_by_id = {row.get("source_id", "").strip(): row for row in source_rows}
    for row in evidence_rows:
        if row.get("status", "").strip().lower() not in allowed_evidence:
            issues.append(f"evidence-register.csv: invalid status for {row.get('evidence_id')}")
        source_ids = split_ids(row.get("source_ids", ""))
        if row.get("status", "").strip().lower() == "found" and not source_ids:
            issues.append(f"evidence-register.csv: found evidence {row.get('evidence_id')} has no source")
        for source_id in source_ids:
            if source_id not in source_by_id:
                issues.append(f"evidence-register.csv: {row.get('evidence_id')} cites unknown source {source_id}")

    for row in read_rows(project / "mechanism-evidence-matrix.csv"):
        step_id = row.get("step_id", "<missing>")
        necessary = row.get("necessary", "").strip().lower()
        support_status = row.get("support_status", "").strip().lower()
        if necessary not in ALLOWED_NECESSARY:
            issues.append(f"mechanism-evidence-matrix.csv: invalid necessary for {step_id}")
        if support_status not in ALLOWED_STEP_STATUS:
            issues.append(f"mechanism-evidence-matrix.csv: invalid support_status for {step_id}")
        for evidence_id in split_ids(row.get("evidence_ids", "")):
            if evidence_id not in evidence_ids:
                issues.append(f"mechanism-evidence-matrix.csv: {step_id} cites unknown evidence {evidence_id}")

    allowed_independence = {"independent", "dependent", "partially-independent", "single-family", "unknown"}
    for row in read_rows(project / "source-dependence-matrix.csv"):
        source_id = row.get("source_id", "").strip()
        proposition_id = row.get("proposition_id", "").strip()
        independence = row.get("independence_status", "").strip().lower()
        source = source_by_id.get(source_id)
        if source is None:
            issues.append(f"source-dependence-matrix.csv: unknown source {source_id}")
        elif row.get("family_id", "").strip() != source.get("family_id", "").strip():
            issues.append(f"source-dependence-matrix.csv: family mismatch for {source_id}")
        if proposition_id not in proposition_ids:
            issues.append(f"source-dependence-matrix.csv: unknown proposition {proposition_id}")
        if independence not in allowed_independence:
            issues.append(f"source-dependence-matrix.csv: invalid independence_status for {source_id}")

    explanation_ids = {
        row.get("explanation_id", "").strip()
        for row in read_rows(project / "theory-rival-matrix.csv")
    }
    allowed_claim_types = {"descriptive", "causal", "explanatory", "interpretive", "normative"}
    allowed_testing_status = {"untested", "partially_tested", "tested", "contested", "out_of_scope"}
    for row in read_rows(project / "claim-register.csv"):
        claim_id = row.get("claim_id", "<missing>")
        for evidence_id in split_ids(row.get("evidence_ids", "")):
            if evidence_id not in evidence_ids:
                issues.append(f"claim-register.csv: {claim_id} cites unknown evidence {evidence_id}")
        for rival_id in split_ids(row.get("rival_ids", "")):
            if rival_id not in explanation_ids:
                issues.append(f"claim-register.csv: {claim_id} cites unknown rival {rival_id}")
        if "claim_type" in row and row.get("claim_type", "").strip().lower() not in allowed_claim_types:
            issues.append(f"claim-register.csv: invalid claim_type for {claim_id}")
        if "testing_status" in row and row.get("testing_status", "").strip().lower() not in allowed_testing_status:
            issues.append(f"claim-register.csv: invalid testing_status for {claim_id}")

    issues.extend(audit(project))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    project = args.project.expanduser().resolve()
    if not project.is_dir():
        print(f"BLOCK: project directory does not exist: {project}")
        return 1
    try:
        issues = validate(project)
    except (KeyError, OSError, csv.Error) as exc:
        print(f"BLOCK: could not validate project: {exc}")
        return 1
    if issues:
        for issue in issues:
            print(f"BLOCK: {issue}")
        return 1
    print("PASS: project structure and conclusion ceiling are valid")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
