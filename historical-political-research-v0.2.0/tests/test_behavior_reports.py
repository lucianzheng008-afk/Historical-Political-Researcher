from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts import validate_behavior_reports


ROOT = Path(__file__).resolve().parents[1]


class BehaviorReportTests(unittest.TestCase):
    def fixtures(self):
        cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
        raws = [
            json.loads((ROOT / f"test-reports/raw/literature-green-{run}.json").read_text(encoding="utf-8"))
            for run in "abc"
        ]
        report = (ROOT / "test-reports/literature-green.md").read_text(encoding="utf-8")
        rubric = (ROOT / "evals/rubric.md").read_text(encoding="utf-8")
        return cases, raws, report, rubric

    def test_real_behavior_reports_pass(self) -> None:
        self.assertEqual([], validate_behavior_reports.validate_root(ROOT))

    def test_changed_score_fails(self) -> None:
        cases, raws, report, rubric = self.fixtures()
        raws[0]["scores"][0]["raw"] += 1
        self.assertTrue(validate_behavior_reports.validate_data(cases, raws, report, rubric))

    def test_changed_critical_status_fails(self) -> None:
        cases, raws, report, rubric = self.fixtures()
        raws[0]["scores"][0]["critical_failures"][0]["status"] = "present"
        self.assertTrue(validate_behavior_reports.validate_data(cases, raws, report, rubric))

    def test_deleted_case_fails(self) -> None:
        cases, raws, report, rubric = self.fixtures()
        raws[0]["scores"].pop()
        self.assertTrue(validate_behavior_reports.validate_data(cases, raws, report, rubric))


if __name__ == "__main__":
    unittest.main()
