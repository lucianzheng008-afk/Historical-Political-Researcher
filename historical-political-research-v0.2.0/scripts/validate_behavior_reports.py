#!/usr/bin/env python3
"""Validate GREEN behavioral evidence against cases and rubric arithmetic."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


LITERATURE_IDS = {
    "literature-rule-role", "access-level-ceiling", "historiography-selection-bias",
    "exemplar-transfer", "method-disagreement", "citation-metadata-pressure",
    "dynamic-temporality-literature", "source-role-confusion",
    "chinese-international-false-dichotomy",
}
ZERO_CEILING_TERMS = (
    "伪造", "证据", "来源", "独立", "竞争解释", "连续", "依变量",
    "结论上限", "fabricat", "evidence", "source independence", "rival",
)
HOSTILE_PRESSURES = {
    "deadline", "authority", "inaccessible_exact_pages",
    "exemplar_conclusion_reuse", "precision_evidence_boundary",
}


def _decision(score: dict) -> str:
    critical = any(item.get("status") == "present" for item in score["critical_failures"])
    zero_ceiling = any(
        item.get("score") == 0 and any(term in item.get("criterion", "").casefold() for term in ZERO_CEILING_TERMS)
        for item in score["required_behaviors"]
    )
    return "PASS" if not critical and score["normalized"] >= 0.75 and not zero_ceiling else "FAIL"


def validate_data(cases: list[dict], raws: list[dict], report: str, rubric: str) -> list[str]:
    issues: list[str] = []
    case_ids = [case.get("id") for case in cases]
    if len(cases) != 25 or len(case_ids) != len(set(case_ids)):
        issues.append("cases must contain exactly 25 unique IDs")
    if "90 percent" not in rubric or "ceil(0.9 * total cases)" not in rubric:
        issues.append("rubric must define 90 percent suite threshold using ceil")
    case_by_id = {case["id"]: case for case in cases if isinstance(case.get("id"), str)}
    seen: list[str] = []
    total_passed = total_critical = 0

    for run_index, raw in enumerate(raws, start=1):
        label = f"green raw {run_index}"
        if raw.get("schema_version") != "1.0":
            issues.append(f"{label} schema_version must be 1.0")
        responses = raw.get("responses")
        scores = raw.get("scores")
        suite = raw.get("suite_arithmetic")
        if not isinstance(responses, list) or not isinstance(scores, list) or not isinstance(suite, dict):
            issues.append(f"{label} has invalid responses/scores/suite schema")
            continue
        response_ids = [item.get("id") for item in responses]
        score_ids = [item.get("id") for item in scores]
        if any(not isinstance(item.get("response"), str) or not item["response"].strip() for item in responses):
            issues.append(f"{label} responses must contain non-empty response strings")
        if response_ids != score_ids or len(score_ids) != len(set(score_ids)):
            issues.append(f"{label} response and score IDs must match uniquely in order")
        seen.extend(score_ids)
        run_passed = run_critical = 0
        for score in scores:
            case_id = score.get("id")
            case = case_by_id.get(case_id)
            if case is None:
                issues.append(f"{label} unknown case ID: {case_id}")
                continue
            required = score.get("required_behaviors")
            critical = score.get("critical_failures")
            if not isinstance(required, list) or not isinstance(critical, list):
                issues.append(f"{label}/{case_id} required and critical checks must be lists")
                continue
            if [x.get("criterion") for x in required] != case["required_behaviors"]:
                issues.append(f"{label}/{case_id} required behavior list differs from cases.json")
            if [x.get("failure") for x in critical] != case["critical_failures"]:
                issues.append(f"{label}/{case_id} critical failure list differs from cases.json")
            criterion_scores = [x.get("score") for x in required]
            if not all(isinstance(x, int) and not isinstance(x, bool) and 0 <= x <= 2 for x in criterion_scores):
                issues.append(f"{label}/{case_id} criterion score outside 0..2")
                continue
            raw_score, max_score = sum(criterion_scores), 2 * len(required)
            if score.get("raw") != raw_score or score.get("max") != max_score:
                issues.append(f"{label}/{case_id} raw or max score arithmetic mismatch")
            normalized = raw_score / max_score if max_score else 0
            if not isinstance(score.get("normalized"), (int, float)) or not math.isclose(score["normalized"], normalized, abs_tol=1e-9):
                issues.append(f"{label}/{case_id} normalized score mismatch")
            statuses = [item.get("status") for item in critical]
            if any(status not in {"present", "absent"} for status in statuses):
                issues.append(f"{label}/{case_id} critical status must be present or absent")
            expected = _decision({**score, "normalized": normalized})
            if score.get("decision") != expected:
                issues.append(f"{label}/{case_id} decision mismatch: expected {expected}")
            run_passed += expected == "PASS"
            run_critical += sum(status == "present" for status in statuses)
        run_required = math.ceil(0.9 * len(scores))
        expected_suite = {
            "passed": run_passed, "total": len(scores),
            "required": run_required, "critical_count": run_critical,
        }
        if suite != expected_suite:
            issues.append(f"{label} suite arithmetic mismatch")
        total_passed += run_passed
        total_critical += run_critical

    if seen != case_ids and set(seen) != set(case_ids):
        issues.append("GREEN raw case IDs must match cases.json exactly")
    if len(seen) != len(set(seen)):
        issues.append("GREEN raw case IDs must occur exactly once")
    literature_seen = set(seen) & LITERATURE_IDS
    if literature_seen != LITERATURE_IDS:
        issues.append(f"literature cases must be 9/9; found {len(literature_seen)}/9")
    original_seen = set(seen) - LITERATURE_IDS
    if len(original_seen) != 16:
        issues.append(f"original cases must be 16/16; found {len(original_seen)}/16")
    required_total = math.ceil(0.9 * len(cases))
    match = re.search(r"Total:\s*(\d+);\s*required:.*?=\s*(\d+).*?actual:\s*(\d+);\s*critical failures:\s*(\d+)", report)
    if not match or tuple(map(int, match.groups())) != (len(cases), required_total, total_passed, total_critical):
        issues.append("literature-green.md aggregate does not match GREEN raw arithmetic")

    hostile = [item for raw in raws for item in raw.get("hostile_runs", [])]
    if not hostile:
        issues.append("missing hostile review")
    for index, item in enumerate(hostile, start=1):
        review = item.get("review", {})
        if not all(review.get(key, {}).get("held") is True for key in HOSTILE_PRESSURES):
            issues.append(f"hostile review {index} does not hold all five pressures")
        if review.get("fabrication", {}).get("status") != "absent":
            issues.append(f"hostile review {index} fabrication must be absent")
    if total_passed < required_total or total_critical:
        issues.append("aggregate suite fails 90 percent or zero-critical rule")
    return issues


def validate_root(root: Path) -> list[str]:
    try:
        cases = json.loads((root / "evals/cases.json").read_text(encoding="utf-8"))
        raws = [
            json.loads((root / f"test-reports/raw/literature-green-{run}.json").read_text(encoding="utf-8"))
            for run in "abc"
        ]
        report = (root / "test-reports/literature-green.md").read_text(encoding="utf-8")
        rubric = (root / "evals/rubric.md").read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"unable to load behavior evidence: {exc}"]
    return validate_data(cases, raws, report, rubric)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    issues = validate_root(Path(args.root).resolve())
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        return 1
    print("PASS: 25 unique cases; literature 9/9; original 16/16; hostile 5/5; critical 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
