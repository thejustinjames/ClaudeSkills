# Worked examples

Two short end-to-end runs: one that correctly fails the gate and produces a
work-trial design instead of an offer recommendation, and one that runs to a
constrained verdict. Details are illustrative, not a transcript.

---

## Example 1 — "Should we hire Dana?" (gate fails, correctly)

A 14-person product company. The CTO asks: "We interviewed Dana for the
senior data role — everyone loved her. Should we make the offer?"

### Step 1 — decision statement

Interviewing the CTO surfaces that "the senior data role" has no written
requirement beyond a template JD. The irreducible requirement, in the CTO's
own words after some pushing: *"someone who can make our ingestion pipeline
stop paging us and make the analytics trustworthy enough to put in front of
customers."* Alternatives never considered until asked: contracting the
pipeline stabilisation; promoting the mid-level engineer who already owns
half of it. Both go in `02-decision.md`.

### Step 3 — evidence and the gate

What actually exists:

```markdown
## E1 | type: claimed | source: Dana's CV | date: 2026-07-10
Senior data engineer, 6 yrs; "built streaming platform handling 2B events/day".

## E2 | type: interview | source: Panel interview, 4 staff, notes same-day | date: 2026-07-14
Strong system-design discussion; articulate on tradeoffs; the panel's notes
all describe her as "a great fit with the team".

## E3 | type: interview | source: CTO 1:1 | date: 2026-07-15
Described debugging approach convincingly; no artifacts examined.

## E4 | type: claimed | source: LinkedIn profile | date: 2026-07-10
Endorsements; conference talk listed (not watched).
```

```
$ python scripts/evidence_lint.py --gate --evidence 03-evidence.md --stage candidate
GATE: FAIL
  - only 0 independent demonstrated/reference/internal-data source(s); 5 required
  - zero demonstrated items -- no actual work has been examined; the analysis
    would run on claims and interview polish
```

Four evidence items, all claims and interviews. Note also E2's "great fit"
— resemblance already at work, and no role has even run.

### The Evidence Acquisition Plan (the actual deliverable)

1. **Watch the talk, read the public work** (2 hours, free). Settles whether
   the 2B-events claim has any visible substance. If nothing public exists,
   that is not disqualifying — it moves the weight to item 2.
2. **Paid half-day work sample** (~£400): give Dana the actual worst
   ingestion incident from last month (sanitised) and ask her to diagnose
   and propose the fix, talking aloud with the engineer who owns the
   pipeline. Rubric written first: identifies the real root cause; proposes
   something implementable within the team's constraints; how she handles
   being wrong. Settles the irreducible requirement directly.
3. **Two structured reference calls** (2 hours): the specific questions —
   "walk me through the hardest production incident she owned"; "would you
   hire her again, for what exactly, and for what not?" Settles whether the
   claimed platform work was hers.

Stated plainly in the plan: *a memo now would be fiction. Everyone loving
her is the situation the process exists to check, not evidence.*

---

## Example 2 — "Ana vs. Ben for the platform lead" (constrained verdict)

Same company, three months later, better habits. Two finalists for a platform
lead role. Evidence includes: paid work samples from both (E1, E2), two
conducted references each (E3–E6), sprint/gap exports (E7, E8), Ana's
open-source maintainership read directly (E9), past-hire history (E10).
Gate: PASS (`--stage candidate`; 7 strong items, 6 sources).

### What the isolated roles produced (compressed)

- **Role Architect** (no candidate evidence): the irreducible requirement is
  *operating the platform through the next doubling* — and flags that the JD's
  "10 years experience" was a proxy already demoted. Names a live risk: the
  role assumes the ingestion rewrite lands.
- **Evidence Assessor**: Ana's trial output strongest on incident diagnosis
  [E1]; her maintainership shows sustained review quality [E9]. Ben's trial
  strong on design, weaker on execution under constraint [E2]; his reference
  hesitated on "operating at scale" — verbatim captured [E5]. Ben's CV claim
  of "scaled platform 10x" is uncorroborated by either reference →
  ledger.
- **Team Integrator** (no CVs): the team demonstrably lacks incident
  discipline [E7]; Ana's demonstrated work adds exactly that; Ben duplicates
  design strength the team already has [E8]. Resemblance check: Ben's
  background closely matches the last two hires.
- **Cost & Capacity Analyst**: both in band; the gap costs ~1.5 engineer-days
  /week in pages [GIVEN: E7]; onboarding capacity exists after this sprint
  [E8].
- **Historian**: the org's regret pattern is hiring for design polish and
  regretting execution [E10]; both prior platform hires were funnel-sourced,
  as are both finalists.

### Red team (three clean-context refuters)

- **Resemblance lens**: attacks *Ben's* candidacy — his case rests mostly on
  interview and design-taste signals matching the last two hires; survives.
- **False-negative lens**: both finalists came from the funnel; the
  evidence-of-work channel was never worked. Survives — with the 30-day
  observable "work the channel for two weeks."
- **Wrong-problem lens**: attacks the role's dependence on the ingestion
  rewrite landing; partially answered from E7, does not survive as a role
  killer but adds assumption A4 to the ledger.

### Ledger and verdict

`rank_assumptions.py`: A2 ("Ben actually operated, not just designed, the
scaled platform") — load-bearing, priority 20, untested → his verdict is
capped.

The memo's verdicts:

- **Ana: hire.** No forcing rule triggered; load-bearing claims rest on
  demonstrated and reference evidence.
- **Ben: trial** — if wanted for a different seat later; the trial card is a
  reference call with his platform's actual SRE lead.
- **Alongside both: the finding-plan card runs anyway** — two weeks of
  evidence-of-work search before the *next* req opens, because the
  false-negative refutation survived and the Historian showed a
  funnel-only track record.
- **Standing card:** first-ever rejected-pile audit scheduled; `05-history.md`
  currently says "no audit has ever run."

The footer states: 7 strong items; load-bearing claims on
demonstrated/reference evidence: 5 of 6; uncorroborated claimed items still
load-bearing: E11 (Ben's 10x claim). What made this run honest was not the
recommendation — it was that Ben's polished interviews could not outrank
Ana's demonstrated work, because the structure never let them compete in the
same currency.
