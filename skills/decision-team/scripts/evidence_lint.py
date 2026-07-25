#!/usr/bin/env python3
"""Evidence gate and citation lint for the decision-team skill.

Two modes:

  Gate (before any role runs) -- counts evidence by type and by independent
  source, and evaluates the hard stops:

      python scripts/evidence_lint.py --gate --evidence 03-evidence.md

  Lint (after a role returns) -- verifies that every claim line carries a tag
  saying what supports it, that cited ids exist in the slice the role was
  actually given, and that unsupported claims stay under the role's ceiling:

      python scripts/evidence_lint.py roles/operator.md --evidence slices/operator.md

  Point --evidence at the role's SLICE, not the full evidence file. A role
  citing an item it was never given is the one automated check on whether the
  isolation held, and it only works against the slice.

Exit code 0 if everything passes, 1 if anything fails, 2 on usage error.

Tags:
    [E3] / [E3,E7]     directly stated in those evidence items
    [INF: E3,E7]       inference going beyond what those items state
    [GIVEN: E3]        a model input taken from evidence (Finance Lead)
    [ASSUMPTION]       not grounded in any evidence given
    [UNKNOWN]          a flagged gap rather than a claim

Assumption ratio = [ASSUMPTION] / (evidence + inference + given + assumption).

[UNKNOWN] is deliberately NOT in that numerator. Flagging a gap is the
behaviour the process wants, and an early version of this script penalised it,
which would have trained roles to stay quiet about what they could not see.
A high [UNKNOWN] share is reported separately as a signal that the slice was
too thin -- a finding about the evidence, not a fault in the deliverable.

The two honesty sections -- "Assumptions I am making" and "Evidence I was not
given but need" -- are excluded from the ratio for the same reason.
"""

import argparse
import re
import sys
from pathlib import Path

CEILINGS = {
    "market-analyst": 0.30,
    "finance-lead": 0.25,
    "customer-strategist": 0.40,
    "operator": 0.40,
    "historian": 0.35,
    "strategy-lead": 0.20,
}
DEFAULT_CEILING = 0.40
MIN_STRONG_SOURCES = 5
MAX_CONTINUATION_LINES = 4
UNKNOWN_SHARE_NOTE = 0.35

EVIDENCE_HEADER = re.compile(r"^##\s+(E\d+)\s*\|", re.IGNORECASE)
EVIDENCE_TYPE = re.compile(r"type:\s*([a-z-]+)", re.IGNORECASE)
EVIDENCE_DATE = re.compile(r"date:\s*(\d{4}(?:-\d{2}){0,2})", re.IGNORECASE)
EVIDENCE_SOURCE = re.compile(r"source:\s*([^|]+)")

LIST_PREFIX = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
TAG_BODY = r"E[\d,\s E]*|INF:[^\]]*|GIVEN:[^\]]*|ASSUMPTION|UNKNOWN"
TAG_AT_START = re.compile(
    r"^\s*(?:(?:[-*+]|\d+[.)])\s+)?\[(" + TAG_BODY + r")\]", re.IGNORECASE
)
ANY_TAG = re.compile(r"\[(" + TAG_BODY + r")\]", re.IGNORECASE)
EID = re.compile(r"E\d+", re.IGNORECASE)
BOLD_META = re.compile(r"^\s*\*\*[^*]+:\*\*")
BOLD_ONLY = re.compile(r"^\s*\*\*[^*]+\*\*\s*$")
SENTENCE_END = re.compile(r"[.!?:;)\"'”’]\s*$")

NO_RATIO_SECTIONS = ("assumptions i am making", "evidence i was not given")
NO_TAG_SECTIONS = ("evidence i was not given",)
STRONG_TYPES = ("primary", "internal-data")


def classify(tag: str) -> str:
    t = tag.strip().upper()
    if t.startswith("ASSUMPTION"):
        return "assumption"
    if t.startswith("UNKNOWN"):
        return "unknown"
    if t.startswith("INF"):
        return "inference"
    if t.startswith("GIVEN"):
        return "given"
    return "evidence"


def load_evidence(path: Path):
    """Parse the evidence file. Sources are tracked so the gate can count
    independent sources rather than blocks -- splitting one interview into four
    items is good hygiene for citation and must not inflate the gate."""
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = EVIDENCE_HEADER.match(line)
        if not m:
            continue
        t = EVIDENCE_TYPE.search(line)
        d = EVIDENCE_DATE.search(line)
        s = EVIDENCE_SOURCE.search(line)
        items.append(
            {
                "id": m.group(1).upper(),
                "type": (t.group(1).lower() if t else "untyped"),
                "date": (d.group(1) if d else None),
                "source": (s.group(1).strip().lower() if s else None),
            }
        )
    return items


def gate(items, path: Path, hinges_on_demand=None):
    print(f"evidence file: {path}")
    if not items:
        print("  no evidence items parsed -- check the "
              "'## E<n> | type: ... | source: ... | date: ...' header format")
        return False

    types = {}
    for it in items:
        types[it["type"]] = types.get(it["type"], 0) + 1
    strong = [i for i in items if i["type"] in STRONG_TYPES]
    strong_sources = {i["source"] for i in strong if i["source"]}
    unsourced_strong = [i["id"] for i in strong if not i["source"]]
    dated = sorted(i["date"] for i in items if i["date"])
    undated = [i["id"] for i in items if not i["date"]]

    print(f"  {len(items)} items: " + " · ".join(f"{v} {k}" for k, v in sorted(types.items())))
    print(f"  strong (primary + internal-data): {len(strong)} items "
          f"from {len(strong_sources) + len(unsourced_strong)} distinct source(s)")
    if dated:
        print(f"  oldest dated item: {dated[0]}   newest: {dated[-1]}")
    if undated:
        print(f"  {len(undated)} item(s) with no parseable date ({', '.join(undated[:6])}"
              f"{'...' if len(undated) > 6 else ''}) -- staleness cannot be assessed")
    if unsourced_strong:
        print(f"  {len(unsourced_strong)} strong item(s) with no source field "
              f"({', '.join(unsourced_strong[:6])}) -- counted as independent, verify by hand")

    n_sources = len(strong_sources) + len(unsourced_strong)
    stops, marginal = [], []

    if n_sources < MIN_STRONG_SOURCES:
        stops.append(
            f"only {n_sources} independent primary/internal-data source(s); "
            f"{MIN_STRONG_SOURCES} required"
        )
    elif n_sources <= 8:
        marginal.append(f"{n_sources} independent strong sources (5-8 band)")

    if len(strong) > n_sources:
        marginal.append(
            f"{len(strong)} strong items come from only {n_sources} sources -- "
            "the count is thinner than it looks"
        )

    if types.get("primary", 0) == 0:
        msg = "zero primary items -- nobody outside the room has been asked anything"
        (stops if hinges_on_demand else marginal).append(msg)

    if types.get("internal-data", 0) == 0:
        marginal.append("zero internal-data items -- no grounding in your own numbers")

    print()
    print("  These conditions need your judgement and are not checked here:")
    print("    - does the decision turn on demand, and are there zero conversations")
    print("      with people who would actually BUY it? (in B2B2C, check the user")
    print("      side separately -- buyer interviews do not cover patient demand)")
    print("    - does it turn on unit economics with no internal cost or price data?")
    print("    - is every item older than the last time this market visibly moved?")
    print()

    if stops:
        print("GATE: FAIL")
        for s in stops:
            print(f"  - {s}")
        print()
        print("  Produce an Evidence Acquisition Plan, not a decision memo.")
        print("  See references/evidence-protocol.md. Do not spawn any role.")
        return False

    if marginal:
        print("GATE: MARGINAL PASS -- verdict is capped at 'test'")
        for m in marginal:
            print(f"  - {m}")
        print()
        print("  Say this in the memo. Proceed to slicing.")
        return True

    print("GATE: PASS")
    print("  Proceed to slicing. Kill conditions and the ledger still constrain the verdict.")
    return True


def role_for(path: Path, override):
    if override:
        return override.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    for role in CEILINGS:
        if role in stem or role.replace("-", "") in stem.replace("-", ""):
            return role
    return "unknown"


def lint(path: Path, evidence_ids, role, ceiling):
    lines = path.read_text(encoding="utf-8").splitlines()
    counts = {"evidence": 0, "inference": 0, "given": 0, "assumption": 0, "unknown": 0}
    untagged, bad_ids, notes = [], [], []
    in_fence = False
    section = ""
    table_header_has_tag = False
    in_table = False
    # A line only continues the one above it when that line was left
    # mid-sentence. Without this, a tagged claim followed by paragraphs of
    # untagged invention passes clean -- which defeats the entire check.
    open_sentence = False
    run = 0

    for n, raw in enumerate(lines, 1):
        stripped = raw.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            open_sentence, run = False, 0
            continue
        if in_fence or not stripped:
            in_table = False
            open_sentence, run = False, 0
            continue
        if stripped.startswith("#"):
            section = stripped.lstrip("#").strip().lower()
            in_table = False
            open_sentence, run = False, 0
            continue
        if stripped.startswith("<!--") or stripped.startswith(">"):
            open_sentence, run = False, 0
            continue
        if set(stripped) <= set("-=_* ") and len(stripped) >= 3:
            open_sentence, run = False, 0
            continue
        if BOLD_META.match(stripped) or BOLD_ONLY.match(stripped):
            # Metadata lines wrap too; allow their continuation.
            open_sentence = not SENTENCE_END.search(stripped)
            run = 0
            continue

        skip_ratio = any(s in section for s in NO_RATIO_SECTIONS)
        skip_tag = any(s in section for s in NO_TAG_SECTIONS)

        if stripped.startswith("|"):
            cells = [c.strip().lower() for c in stripped.strip("|").split("|")]
            open_sentence, run = False, 0
            if not in_table:
                in_table = True
                table_header_has_tag = any("tag" in c for c in cells)
                continue
            if set(stripped) <= set("|-: "):
                continue
            if not table_header_has_tag:
                continue
            found = ANY_TAG.findall(stripped)
            if not found:
                untagged.append((n, stripped[:90]))
                continue
            for tag in found:
                kind = classify(tag)
                if not skip_ratio:
                    counts[kind] += 1
                for eid in EID.findall(tag):
                    if evidence_ids is not None and eid.upper() not in evidence_ids:
                        bad_ids.append((n, eid.upper()))
            continue

        in_table = False
        m = TAG_AT_START.match(stripped)
        if not m:
            is_continuation = (
                open_sentence
                and run < MAX_CONTINUATION_LINES
                and not LIST_PREFIX.match(raw)
            )
            if is_continuation:
                run += 1
                open_sentence = not SENTENCE_END.search(stripped)
                continue
            if not skip_tag:
                untagged.append((n, stripped[:90]))
            open_sentence, run = False, 0
            continue

        tag = m.group(1)
        kind = classify(tag)
        open_sentence = not SENTENCE_END.search(stripped)
        run = 0

        if "assumptions i am making" in section and kind != "assumption":
            notes.append(f"line {n}: '{kind}' tag inside the assumptions section")

        if not skip_ratio:
            counts[kind] += 1
        for eid in EID.findall(tag):
            if evidence_ids is not None and eid.upper() not in evidence_ids:
                bad_ids.append((n, eid.upper()))

    hard = counts["evidence"] + counts["inference"] + counts["given"] + counts["assumption"]
    ratio = (counts["assumption"] / hard) if hard else 0.0
    total = hard + counts["unknown"]
    unknown_share = (counts["unknown"] / total) if total else 0.0

    if unknown_share > UNKNOWN_SHARE_NOTE and counts["unknown"] > 2:
        notes.append(
            f"{counts['unknown']} of {total} tagged lines are [UNKNOWN] "
            f"({unknown_share:.0%}) -- the slice was probably too thin for this "
            "role. That belongs in the memo's limitations, not in a redo."
        )
    if role == "strategy-lead" and counts["assumption"]:
        notes.append(
            f"{counts['assumption']} [ASSUMPTION] line(s) in synthesis -- the "
            "Strategy Lead may only carry claims forward, never introduce them"
        )
    if total == 0:
        notes.append("no tagged claim lines found -- is this a deliverable?")

    ok = not untagged and not bad_ids and ratio <= ceiling and total > 0
    return {
        "path": path, "role": role, "ceiling": ceiling, "counts": counts,
        "hard": hard, "total": total, "ratio": ratio, "untagged": untagged,
        "bad_ids": bad_ids, "notes": notes, "ok": ok,
    }


def report(r):
    status = "PASS" if r["ok"] else "FAIL"
    print(f"\n{status}  {r['path'].name}   role={r['role']}  ceiling={r['ceiling']:.2f}")
    c = r["counts"]
    print(
        f"      evidence={c['evidence']}  inference={c['inference']}  given={c['given']}"
        f"  assumption={c['assumption']}  unknown={c['unknown']}"
    )
    print(f"      assumption ratio = {r['ratio']:.2f}  ({c['assumption']}/{r['hard']})")
    if r["ratio"] > r["ceiling"]:
        print("      ceiling exceeded -- send it back to its own role agent with the")
        print("      ceiling stated. Do not patch it yourself; you have seen the other")
        print("      roles' work and your edits reintroduce the correlation.")
    if r["untagged"]:
        print(f"      {len(r['untagged'])} untagged claim line(s):")
        for n, text in r["untagged"][:12]:
            print(f"        line {n}: {text}")
        if len(r["untagged"]) > 12:
            print(f"        ... and {len(r['untagged']) - 12} more")
    if r["bad_ids"]:
        uniq = sorted({e for _, e in r["bad_ids"]})
        print(f"      cited ids absent from the file given: {', '.join(uniq)}")
        print("      If --evidence pointed at the role's slice, this means the role")
        print("      cited something it was never given -- the isolation leaked.")
    for note in r["notes"]:
        print(f"      note: {note}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("files", nargs="*", help="role deliverables to lint")
    ap.add_argument("--evidence", help="evidence file, or the role's slice when linting")
    ap.add_argument("--gate", action="store_true", help="run the evidence gate and stop")
    ap.add_argument("--hinges-on-demand", action="store_true",
                    help="the decision turns on whether anyone wants it (stricter gate)")
    ap.add_argument("--role", help="override role detection for all files")
    ap.add_argument("--ceiling", type=float, help="override the assumption ceiling")
    args = ap.parse_args()

    items, evidence_ids = None, None
    if args.evidence:
        ep = Path(args.evidence)
        if not ep.is_file():
            print(f"error: evidence file not found: {ep}", file=sys.stderr)
            return 2
        items = load_evidence(ep)
        evidence_ids = {i["id"] for i in items}

    if args.gate or not args.files:
        if items is None:
            print("error: --gate needs --evidence <03-evidence.md>", file=sys.stderr)
            return 2
        return 0 if gate(items, Path(args.evidence), args.hinges_on_demand) else 1

    results = []
    for f in args.files:
        p = Path(f)
        if not p.is_file():
            print(f"error: not a file: {p}", file=sys.stderr)
            return 2
        role = role_for(p, args.role)
        ceiling = args.ceiling if args.ceiling is not None else CEILINGS.get(role, DEFAULT_CEILING)
        results.append(lint(p, evidence_ids, role, ceiling))

    if evidence_ids:
        print(f"validating ids against {args.evidence} ({len(evidence_ids)} items)")
    for r in results:
        report(r)

    failed = [r for r in results if not r["ok"]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
