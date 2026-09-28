#!/usr/bin/env python3
"""Initialize an auditable historical-political-research project."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATES = PACKAGE_ROOT / "assets/templates"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--template-root", type=Path, default=DEFAULT_TEMPLATES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.template_root.expanduser().resolve()
    target = args.target.expanduser().resolve()
    if not source.is_dir():
        raise SystemExit(f"Template root does not exist: {source}")
    if target == source or source in target.parents or target in source.parents:
        raise SystemExit(f"Refusing overlapping template and target paths: {source} -> {target}")
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"Refusing nonempty target: {target}")
    target.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        destination = target / item.name
        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)
    print(f"Initialized historical-political-research project at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
