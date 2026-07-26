#!/usr/bin/env python3
"""Rank the assumption ledger and apply the verdict constraint.

Reads the markdown table in assumptions.md, sorts by importance x uncertainty,
flags load-bearing assumptions with no trial attached, and applies the rule
that a load-bearing assumption at priority >= 16 with status 'untested' caps
the verdict at 'trial' rather than 'hire'.

Binding the verdict to the ledger is what keeps the analysis honest when the
reader clearly wants to hear yes. Which is why unrecognised values in the two
columns that drive the rule are errors rather than silent defaults -- writing
'in progress' instead of 'testing' would otherwise quietly exempt an
assumption from the only mechanism holding the verdict down.

Usage:
    python scripts/rank_assumptions.py <workspace>/assumptions.md [--threshold 16]

Exit codes: 0 unconstrained, 1 verdict capped at 'trial', 2 ledger unusable.
"""

import argparse
import re
import sys
from pathlib import Path

COLUMNS = ["id", "assumption", "load_bearing", "importance", "uncertainty", "test", "cost", "status"]

STATUS_VALUES = {
    "untested": True, "testing": False, "passed": False,
    "failed": False, "accepted": False,
}
LOAD_BEARING_VALUES = {"yes": True, "no": False}
PLACEHOLDER = re.compile(r"^[\s\-–—<>.]*$")
NON_TESTS = {"tbd", "todo", "none", "n/a", "na", "?", "unknown", ""}


def parse(path: Path):
    rows, in_table, header_seen, blanked = [], False, False, 0
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if set(line) <= set("|-: "):
            continue
        if not in_table:
            in_table = True
            header_seen = any("assumption" in c.lower() for c in cells)
            continue
        if not header_seen or len(cells) < len(COLUMNS):
            continue
        row = dict(zip(COLUMNS, cells[: len(COLUMNS)]))
        row["line"] = n
        if PLACEHOLDER.match(row["assumption"]) or not row["id"]:
            blanked += 1
            continue
        rows.append(row)
    return rows, blanked


def to_int(value, default=0):
    m = re.search(r"\d+", value or "")
    return int(m.group()) if m else default


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ledger", help="path to assumptions.md")
    ap.add_argument("--threshold", type=int, default=16, help="priority capping the verdict at trial")
    args = ap.parse_args()

    path = Path(args.ledger)
    if not path.is_file():
        print(f"error: ledger not found: {path}", file=sys.stderr)
        return 2

    rows, blanked = parse(path)
    if not rows:
        if blanked:
            print(f"The ledger has {blanked} row(s) but no assumption text in any of them.")
            print("This is the empty template -- fill it in before ranking.")
        else:
            print("error: no assumption rows parsed. Expected column order:")
            print("       | " + " | ".join(COLUMNS) + " |")
        return 2

    errors = []
    for r in rows:
        r["I"] = to_int(r["importance"])
        r["U"] = to_int(r["uncertainty"])
        r["priority"] = r["I"] * r["U"]

        lb = r["load_bearing"].strip().lower()
        if lb not in LOAD_BEARING_VALUES:
            errors.append(f"  {r['id']} (line {r['line']}): load_bearing = '{r['load_bearing']}' "
                          f"-- must be one of: {', '.join(sorted(LOAD_BEARING_VALUES))}")
            r["lb"] = True
        else:
            r["lb"] = LOAD_BEARING_VALUES[lb]

        st = r["status"].strip().lower()
        if st not in STATUS_VALUES:
            errors.append(f"  {r['id']} (line {r['line']}): status = '{r['status']}' "
                          f"-- must be one of: {', '.join(sorted(STATUS_VALUES))}")
            r["untested"] = True
        else:
            r["untested"] = STATUS_VALUES[st]

        t = (r["test"] or "").strip().lower()
        r["has_test"] = not (PLACEHOLDER.match(t) or t in NON_TESTS)

        if not 1 <= r["I"] <= 5 or not 1 <= r["U"] <= 5:
            errors.append(f"  {r['id']} (line {r['line']}): importance/uncertainty must be 1-5, "
                          f"got {r['importance']}/{r['uncertainty']}")

    if errors:
        print("Ledger vocabulary errors -- these columns drive the verdict rule, so")
        print("they are not guessed at:")
        for e in errors:
            print(e)
        print("\nUnrecognised values were treated conservatively (load-bearing, untested)")
        print("for the ranking below. Fix the ledger and rerun.\n")

    rows.sort(key=lambda r: (-r["priority"], not r["lb"]))

    width = min(max(max(len(r["assumption"]) for r in rows), 20), 52)
    header = f"{'id':<5}{'pri':>4}  {'LB':<5}{'status':<10}{'test?':<7}assumption"
    print(header)
    print("-" * min(len(header) + width, 100))
    for r in rows:
        forcing = r["lb"] and r["priority"] >= args.threshold and r["untested"]
        text = r["assumption"]
        text = text if len(text) <= width else text[: width - 1].rstrip() + "…"
        print(
            f"{r['id']:<5}{r['priority']:>4}  {('yes' if r['lb'] else 'no'):<5}"
            f"{r['status'][:9]:<10}{('yes' if r['has_test'] else 'NONE'):<7}"
            f"{text}{'   <-- forces trial' if forcing else ''}"
        )

    forcing = [r for r in rows if r["lb"] and r["priority"] >= args.threshold and r["untested"]]
    no_test = [r for r in rows if r["lb"] and not r["has_test"]]

    print()
    if no_test:
        print("Load-bearing assumptions with no trial attached:")
        for r in no_test:
            print(f"  {r['id']}: {r['assumption'][:70]}")
        print("  These are what becomes the regretted hire six months from now. Write")
        print("  a trial for each, or set status to 'accepted' with a reason in the memo.")
        print()

    if forcing:
        print(f"VERDICT CAPPED AT 'TRIAL' -- {len(forcing)} load-bearing assumption(s) "
              f"at priority >= {args.threshold}, untested:")
        for r in forcing:
            print(f"  {r['id']} (priority {r['priority']}): {r['assumption'][:70]}")
        print("  There is no exception for a strong interview. Run the trial first.")
        print("  When comparing finalists, apply this per candidate -- see memo-format.md.")
        return 1

    print(f"No load-bearing assumption at priority >= {args.threshold} is untested.")
    print("The ledger does not constrain the verdict. Red-team kill conditions still apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
