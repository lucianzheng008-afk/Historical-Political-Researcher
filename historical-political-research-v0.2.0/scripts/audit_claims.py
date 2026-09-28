#!/usr/bin/env python3
"""Audit claim strength against rivals, mechanism steps, evidence, and sources."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


MATURE_STRENGTHS = {"supported", "strong", "necessary_step_passed", "strong_diagnostic"}
ALLOWED_NECESSARY = {"true", "false"}
ALLOWED_STEP_STATUS = {"supported", "partial", "unsupported", "unknown", "not-tested", "contested"}
NON_SUBSTANTIVE_ACCESS = {"metadata", "abstract", "unavailable"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def split_ids(value: str) -> list[str]:
    return [item.strip() for item in value.replace(",", "|").split("|") if item.strip()]


def audit(project: Path) -> list[str]:
    claims = read_rows(project / "claim-register.csv")
    steps = read_rows(project / "mechanism-evidence-matrix.csv")
    explanations = read_rows(project / "theory-rival-matrix.csv")
    evidence = {row["evidence_id"]: row for row in read_rows(project / "evidence-register.csv")}
    sources = {row["source_id"]: row for row in read_rows(project / "source-register.csv")}
    dependence_rows = read_rows(project / "source-dependence-matrix.csv")
    explanation_by_id = {row["explanation_id"]: row for row in explanations}
    steps_by_mechanism: dict[str, list[dict[str, str]]] = {}
    for step in steps:
        steps_by_mechanism.setdefault(step["mechanism_id"], []).append(step)

    issues: list[str] = []
    for step in steps:
        step_id = step.get("step_id", "<missing>")
        necessary = step.get("necessary", "").strip().lower()
        support_status = step.get("support_status", "").strip().lower()
        if necessary not in ALLOWED_NECESSARY:
            issues.append(f"{step_id}: invalid necessary value {necessary!r}")
        if support_status not in ALLOWED_STEP_STATUS:
            issues.append(f"{step_id}: invalid support_status {support_status!r}")
        step_evidence_ids = split_ids(step.get("evidence_ids", ""))
        if support_status == "supported" and not step_evidence_ids:
            issues.append(f"{step_id}: supported step has no evidence")
        for evidence_id in step_evidence_ids:
            item = evidence.get(evidence_id)
            if item is None:
                issues.append(f"{step_id}: unknown evidence {evidence_id}")
            elif support_status == "supported" and item.get("status", "").strip().lower() != "found":
                issues.append(f"{step_id}: supported step uses evidence {evidence_id} that is not found")

    for claim in claims:
        claim_id = claim.get("claim_id", "<missing>")
        strength = claim.get("claim_strength", "").strip().lower()
        if strength not in MATURE_STRENGTHS:
            continue
        rival_ids = split_ids(claim.get("rival_ids", ""))
        if not rival_ids:
            issues.append(f"{claim_id}: mature claim has no linked rival explanation")
        for rival_id in rival_ids:
            rival = explanation_by_id.get(rival_id)
            if rival is None:
                issues.append(f"{claim_id}: unknown rival explanation {rival_id}")
            elif rival.get("role", "").strip().lower() != "rival":
                issues.append(f"{claim_id}: linked explanation {rival_id} is not a rival")
        if not claim.get("scope_conditions", "").strip():
            issues.append(f"{claim_id}: mature claim has no scope conditions")
        mechanism_id = claim.get("mechanism_id", "").strip()
        mechanism_steps = steps_by_mechanism.get(mechanism_id, [])
        if not mechanism_steps:
            issues.append(f"{claim_id}: unknown or empty mechanism {mechanism_id!r}")
        for step in mechanism_steps:
            if step.get("necessary", "").strip().lower() == "true" and step.get(
                "support_status", ""
            ).strip().lower() != "supported":
                issues.append(
                    f"{claim_id}: claim exceeds weakest necessary step {step.get('step_id', '<missing>')}"
                )
        claim_evidence_ids = split_ids(claim.get("evidence_ids", ""))
        if not claim_evidence_ids:
            issues.append(f"{claim_id}: mature claim has no evidence")
        for evidence_id in claim_evidence_ids:
            item = evidence.get(evidence_id)
            if item is None:
                issues.append(f"{claim_id}: unknown evidence {evidence_id}")
                continue
            if item.get("status", "").strip().lower() != "found":
                issues.append(f"{claim_id}: evidence {evidence_id} is not found")
            source_ids = split_ids(item.get("source_ids", ""))
            if not source_ids:
                issues.append(f"{claim_id}: evidence {evidence_id} has no source")
            dependence_states: list[str] = []
            for source_id in source_ids:
                source = sources.get(source_id)
                if source is None:
                    issues.append(f"{claim_id}: evidence {evidence_id} cites unknown source {source_id}")
                elif source.get("access_status", "").strip().lower() in NON_SUBSTANTIVE_ACCESS:
                    issues.append(
                        f"{claim_id}: {source_id} is {source.get('access_status')} only and cannot support a substantive claim"
                    )
                matches = [
                    row for row in dependence_rows
                    if row.get("source_id", "").strip() == source_id
                    and row.get("proposition_id", "").strip() == item.get("proposition_id", "").strip()
                ]
                if not matches:
                    issues.append(
                        f"{claim_id}: evidence {evidence_id} has no dependence record for {source_id}"
                    )
                for match in matches:
                    state = match.get("independence_status", "").strip().lower()
                    dependence_states.append(state)
                    if state == "unknown":
                        issues.append(
                            f"{claim_id}: evidence {evidence_id} has unknown source independence for {source_id}"
                        )
            if dependence_states and all(state == "dependent" for state in dependence_states):
                issues.append(f"{claim_id}: evidence {evidence_id} relies only on dependent source paths")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    project = args.project.expanduser().resolve()
    issues = audit(project)
    if issues:
        for issue in issues:
            print(f"BLOCK: {issue}")
        return 1
    print("PASS: claim strength is within the current evidence ceiling")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
