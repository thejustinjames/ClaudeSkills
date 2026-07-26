#!/usr/bin/env python3
"""Scaffold a hiring-decision workspace.

Usage:
    python scripts/init_workspace.py <role-or-candidate-slug> [--dir PARENT]

Creates <parent>/<slug>/ with the context file templates, the assumption
ledger, and the output folders the workflow writes into.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "assets" / "workspace"
SUBDIRS = ["slices", "roles", "redteam", "tests", "output"]

SLICES_STUB = """# Evidence slices

Which role saw which items. The memo states this so a reader can tell what each
role was working from.

Write each slice to `slices/<role>.md` as a standalone file containing the full
text of its items. Handing a role the whole evidence file with instructions to
read only part of it is not isolation.

| role | evidence ids | rationale |
|------|--------------|-----------|
|      |              |           |
"""


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "hire"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="short name for the role or hiring decision")
    parser.add_argument("--dir", default=".", help="parent directory")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args()

    if not TEMPLATE_DIR.is_dir():
        print(f"error: templates not found at {TEMPLATE_DIR}", file=sys.stderr)
        return 1

    root = Path(args.dir).expanduser().resolve() / slugify(args.slug)
    root.mkdir(parents=True, exist_ok=True)

    copied, skipped = [], []
    for template in sorted(TEMPLATE_DIR.glob("*.md")):
        dest = root / template.name
        if dest.exists() and not args.force:
            skipped.append(dest.name)
            continue
        shutil.copy2(template, dest)
        copied.append(dest.name)

    for sub in SUBDIRS:
        (root / sub).mkdir(exist_ok=True)

    slices = root / "slices.md"
    if not slices.exists() or args.force:
        slices.write_text(SLICES_STUB, encoding="utf-8")
        copied.append("slices.md")

    print(f"workspace: {root}")
    if copied:
        print("  created: " + ", ".join(sorted(copied)))
    if skipped:
        print("  kept existing: " + ", ".join(skipped) + "  (use --force to overwrite)")
    print("  folders: " + ", ".join(SUBDIRS))
    print()
    print("Next: fill 02-decision.md and 03-evidence.md only, then run the gate:")
    print(f"  python scripts/evidence_lint.py --gate --evidence {root}/03-evidence.md \\")
    print("      --stage role|candidate")
    print("The other context files wait until the gate passes -- it often does not,")
    print("and a failed gate producing a work-trial design instead of a memo is the")
    print("skill working, not failing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
