from __future__ import annotations

import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests/fixtures"


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def rewrite_cell(path: Path, column: str, value: str, row_index: int = 0) -> None:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0])
    rows[row_index][column] = value
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class ScriptTests(unittest.TestCase):
    def test_init_project_copies_every_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "new-project"
            result = run_script(
                "init_project.py",
                str(target),
                "--template-root",
                str(FIXTURES / "valid-project"),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            expected = sorted(p.name for p in (FIXTURES / "valid-project").iterdir())
            actual = sorted(p.name for p in target.iterdir())
            self.assertEqual(actual, expected)

    def test_init_project_rejects_nonempty_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing"
            target.mkdir()
            (target / "keep.txt").write_text("user data", encoding="utf-8")
            result = run_script(
                "init_project.py",
                str(target),
                "--template-root",
                str(FIXTURES / "valid-project"),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((target / "keep.txt").read_text(encoding="utf-8"), "user data")

    def test_validate_project_accepts_valid_fixture(self) -> None:
        result = run_script("validate_project.py", str(FIXTURES / "valid-project"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_validate_project_rejects_invalid_fixture(self) -> None:
        result = run_script("validate_project.py", str(FIXTURES / "invalid-project"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCK", result.stdout)
        self.assertIn("rival", result.stdout.lower())

    def test_duplicate_ids_are_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            shutil.copytree(FIXTURES / "valid-project", target)
            with (target / "puzzle-register.csv").open("a", encoding="utf-8") as handle:
                handle.write("PUZ-1,duplicate,expected,observed,stake,unknown\n")
            result = run_script("validate_project.py", str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate", result.stdout.lower())

    def test_claim_cannot_exceed_unsupported_necessary_step(self) -> None:
        result = run_script("audit_claims.py", str(FIXTURES / "invalid-project"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("weakest necessary step", result.stdout.lower())

    def test_mature_claim_requires_evidence_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            shutil.copytree(FIXTURES / "valid-project", target)
            rewrite_cell(target / "claim-register.csv", "evidence_ids", "")
            result = run_script("audit_claims.py", str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no evidence", result.stdout.lower())

    def test_evidence_requires_source_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            shutil.copytree(FIXTURES / "valid-project", target)
            rewrite_cell(target / "evidence-register.csv", "source_ids", "")
            result = run_script("audit_claims.py", str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no source", result.stdout.lower())

    def test_mechanism_step_rejects_unknown_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            shutil.copytree(FIXTURES / "valid-project", target)
            rewrite_cell(target / "mechanism-evidence-matrix.csv", "evidence_ids", "E-404")
            result = run_script("validate_project.py", str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown evidence", result.stdout.lower())

    def test_dependence_matrix_rejects_unknown_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            shutil.copytree(FIXTURES / "valid-project", target)
            rewrite_cell(target / "source-dependence-matrix.csv", "source_id", "SRC-404")
            result = run_script("validate_project.py", str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown source", result.stdout.lower())

    def test_necessary_is_a_controlled_boolean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            shutil.copytree(FIXTURES / "valid-project", target)
            rewrite_cell(target / "mechanism-evidence-matrix.csv", "necessary", "treu")
            result = run_script("validate_project.py", str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid necessary", result.stdout.lower())

    def test_mature_claim_requires_linked_rival(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            shutil.copytree(FIXTURES / "valid-project", target)
            rewrite_cell(target / "claim-register.csv", "rival_ids", "")
            result = run_script("audit_claims.py", str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no linked rival", result.stdout.lower())

    def test_mature_claim_rejects_unknown_source_independence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            shutil.copytree(FIXTURES / "valid-project", target)
            rewrite_cell(target / "source-dependence-matrix.csv", "independence_status", "unknown")
            result = run_script("audit_claims.py", str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown source independence", result.stdout.lower())

    def test_mature_claim_rejects_only_dependent_source_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            shutil.copytree(FIXTURES / "valid-project", target)
            rewrite_cell(target / "source-dependence-matrix.csv", "independence_status", "dependent")
            result = run_script("audit_claims.py", str(target))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("only on dependent source paths", result.stdout.lower())

    def test_init_project_force_cannot_overwrite_nonempty_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing"
            target.mkdir()
            keep = target / "keep.txt"
            keep.write_text("user data", encoding="utf-8")
            result = run_script(
                "init_project.py",
                str(target),
                "--template-root",
                str(FIXTURES / "valid-project"),
                "--force",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(keep.read_text(encoding="utf-8"), "user data")

    def test_init_project_rejects_target_inside_template_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "templates"
            shutil.copytree(FIXTURES / "valid-project", source)
            target = source / "nested-output"
            result = run_script(
                "init_project.py",
                str(target),
                "--template-root",
                str(source),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
