# Output Formats

Three artefacts: the assumption ledger, the test cards, and the memo. Deliver
them in that order of prominence — the memo is the one people want and the test
cards are the one that changes anything.

## Contents

- [Assumption ledger](#assumption-ledger)
- [Test cards](#test-cards)
- [Decision memo](#decision-memo)
- [Evidence-quality footer](#evidence-quality-footer)

## Assumption ledger

Lives at `<workspace>/assumptions.md`. `scripts/rank_assumptions.py` parses this
table, so keep the column order and the exact vocabulary below —
`load_bearing` accepts only `yes` / `no`, and `status` only `untested` /
`testing` / `passed` / `failed` / `accepted`. The script errors on anything
else rather than guessing, because writing `in progress` instead of `testing`
would otherwise silently exempt an assumption from the one rule holding the
verdict down.

```markdown
| id | assumption | load_bearing | importance | uncertainty | test | cost | status |
|----|-----------|--------------|------------|-------------|------|------|--------|
| A1 | Buyers will pay £500/mo | yes | 5 | 4 | Offer to 20 qualified buyers | 2 days | untested |
| A2 | Team can ship v1 in 6 weeks | yes | 5 | 3 | Timebox a spike on the riskiest integration | 3 days | untested |
| A3 | Reachable via one channel | no | 3 | 4 | £400 of paid to one segment | 1 day | untested |
```

Field notes:

- **load_bearing** — `yes` only if the decision genuinely flips when the
  assumption is false. Marking everything load-bearing destroys the signal, and
  the temptation to do so is strong because every assumption feels important
  while you are writing it down.
- **importance** 1–5 — how much of the outcome rides on it.
- **uncertainty** 1–5 — how little you know. Be honest here specifically; this
  is the field that gets quietly deflated to make a decision look readier than
  it is.
- **test** — a specific action, not a topic. "Interview 5 buyers from the
  segment about budget authority" rather than "validate demand".
- **status** — `untested` / `testing` / `passed` / `failed` / `accepted`.
  `accepted` means proceeding without testing, deliberately, and it needs a
  reason in the memo.

Priority is importance × uncertainty. A load-bearing assumption at priority ≥ 16
with status `untested` forces the verdict to `test` — see SKILL.md step 9.

### Either/or decisions

For an allocation — build A or build B this quarter — keep one ledger and add an
`option` prefix to the ids (`A1-a`, `A1-b`). Run the verdict rule against each
option's assumptions separately and report both: "A: test. B: proceed." is a
real answer. Collapsing two options into one verdict token loses the only thing
the reader asked for. If the analysis finds the framing itself is wrong — both
fail, or the two are not actually exclusive — lead with that and put the
per-option verdicts underneath.

## Test cards

One per assumption you are actually going to test, cheapest first. The
thresholds are written *before* the test runs and carry the date they were set.

```markdown
### T1 — Will buyers pay £500/month?
**Assumption:** A1
**Test:** Offer the £500/mo plan to 20 qualified buyers from the named list.
**Metric:** Number reaching a serious buying conversation — pricing discussed
with the person who signs.
**Sample / duration:** 20 buyers, 2 weeks
**Cost:** ~2 days of selling time

**Thresholds — set 2026-07-25, before running:**
- **Pass (≥4):** proceed to build
- **Modify (2–3):** strong interest with price resistance — retest at £300
- **Fail (≤1):** stop; the segment does not have this budget

**What we do on each result:** <written now, not after>
```

Setting thresholds in advance is the highest-value habit in this whole process,
and it is worth being explicit about why: any result can be read as encouraging
after the fact. Two serious conversations out of twenty is "early traction" or
"a clear no" depending entirely on what you hoped for that morning. The
pre-committed threshold is the only thing standing between a decision process
and an elaborate justification process.

Include the date. It makes retroactive editing visible.

## Decision memo

One page. If it runs longer, the extra length is almost always rationalisation
rather than content.

```markdown
# Decision memo — <decision>
**Date:** <date> · **Decision by:** <deadline> · **Owner:** <name>

## Verdict
**<PROCEED / MODIFY / TEST / STOP>**
<One sentence. If the verdict was constrained by the ledger or a kill condition,
say which — "TEST rather than PROCEED because A1 is load-bearing, priority 20,
and untested.">

## Why
The three strongest pieces of evidence, cited:
1. [E2] ...
2. [E1,E4] ...
3. [E7] ...

## What must be true
The load-bearing assumptions, highest priority first, with status:
- **A1** (priority 20, untested) — ...
- **A2** (priority 15, untested) — ...

## Where the analysis disagreed with itself
<Unresolved conflicts between roles, with what would settle each. If the roles
agreed on everything, say so here and flag it as a warning about correlated
priors rather than as confirmation.>

## Surviving refutations
<Red-team refutations that survived, with their 30-day leading indicators. No
rebuttals — a test or an explicit acceptance, nothing else.>
- **R1** attacks A3 — <scenario>. Leading indicator: <observable>.
  Response: <test T2 / accepted because ...>

## First move (next 48 hours)
<One specific action with a named owner. Not "begin discovery".>

## Kill criteria
We will stop if: <specific, observable, dated>

## Review date
<date> — reopen this memo and check the kill criteria against what happened.

## Limitations
<What the analysis could not see. Roles that failed lint and why. Whether the
isolation actually held. Evidence that was requested and not available.>

---
<evidence-quality footer — see below>
```

## Evidence-quality footer

Every memo ends with this. It is the reader's only means of calibrating what
they are holding, and it is the first thing that gets deleted when a memo is
being made to read well.

```markdown
**Evidence quality:** 6 primary · 4 internal-data · 3 secondary · 1 anecdote ·
0 expert
**Oldest item:** 2026-02-11 (5 months)
**Assumption ratio across role deliverables:** 0.31
**Roles that failed lint on first pass:** Finance Lead (0.38 vs 0.25 ceiling)
**Isolation:** held — 5 roles run as parallel subagents with disjoint slices
**Gate:** marginal pass — 8 primary/internal items, all from one segment
```

Read the difference between a footer showing `12 primary · oldest 6 weeks ·
ratio 0.18` and one showing `1 primary · 9 secondary · oldest 14 months · ratio
0.52`. The memo bodies above them may be equally well written and equally
confident. That is exactly the problem the footer exists to solve.
