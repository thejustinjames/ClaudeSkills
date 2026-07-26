# Role Briefs — Hiring

Six roles. Five analytical roles run in parallel and in isolation; the Talent
Lead synthesises afterward. The red team is separate again and runs last — see
`redteam-protocol.md`.

## Contents

- [Isolation rules](#isolation-rules)
- [The shared output contract](#the-shared-output-contract)
- [1. Role Architect](#1-role-architect)
- [2. Evidence Assessor](#2-evidence-assessor)
- [3. Team Integrator](#3-team-integrator)
- [4. Cost & Capacity Analyst](#4-cost--capacity-analyst)
- [5. Historian](#5-historian)
- [6. Talent Lead](#6-talent-lead)
- [Evidence slicing](#evidence-slicing)

## Isolation rules

Each analytical role receives exactly:

1. `02-decision.md` — the decision statement and real requirement
2. `04-constraints.md` — hard constraints and the legitimate gates
3. Its own evidence slice, as a self-contained file with the full text of its
   items
4. Its role brief from this file
5. The output contract below, with its assumption ceiling

It does **not** receive: the other roles' outputs, the orchestrating
conversation, or any framing about which candidate the room is leaning toward.

Hiring-specific rules, both easy to violate accidentally:

- **No leading in the spawn prompt.** "Assess whether Maya is the right hire"
  and "assess this candidate against this requirement" produce measurably
  different outputs. Hand over the statement, the slice, and the brief;
  do not editorialise, and do not mention that anyone "really liked her".
- **The guardrails travel with every spawn.** Each role prompt includes the
  protected-characteristics exclusion and the describe-evidence-never-character
  rule from SKILL.md. A role that returns personality verdicts gets the
  deliverable back regardless of how well it is tagged.

## The shared output contract

Every analytical role ends its deliverable with these two sections. They
matter more than the analysis body.

```markdown
## Assumptions I am making
[ASSUMPTION] <one per line, load-bearing ones first>

## Evidence I was not given but need
- <what>: would settle <which assumption>; obtainable by <how>
```

Items named by two or more roles go straight to the top of the trial list.

## 1. Role Architect

**Question owned:** what does this role irreducibly need — and is a role even
the right container for the need?

Works from the role-owner's stated requirement, the gap data, and the team
context in its slice. Deliverable covers: the differentiating requirement in
one sentence (the thing a generic JD would average away); which stated
requirements are genuine gates and which are proxies (per
`gates-and-finding.md` — and whether the demotion actually happened); the
unstated alternatives (contract, automate, reshape an existing role, split
the role, don't fill it); and what the role looks like in 18 months if the
org's trajectory holds — a role designed for last year's shape of the work
fails on arrival.

Does **not** see candidate evidence. The requirement must be designed without
a face attached to it — a requirement written while looking at a candidate
quietly becomes that candidate's CV.

## 2. Evidence Assessor

**Question owned:** what has each candidate actually demonstrated — as
opposed to claimed?

The only role that sees the full per-candidate evidence, including `claimed`
items. Deliverable covers: the demonstrated-capability map (what the work
product actually shows, cited item by item); the corroboration table — every
load-bearing `claimed` item marked corroborated (by which `demonstrated` or
`reference` item) or uncorroborated; what the references said, including the
hesitations, verbatim where possible; and the conditions caveat — what was
artificial about each trial or observed setting.

Bound hardest by the guardrails: behaviour and work product only, no
character adjectives, ceiling 0.25. An uncorroborated load-bearing claim is
not a finding of dishonesty — it is an entry for the assumption ledger.

## 3. Team Integrator

**Question owned:** what would this person make the team capable of that it
is not capable of now?

Sees the team composition and gap data, and the candidates' `demonstrated`
work — **not** their CVs. Deliverable covers: what the team demonstrably
lacks (cited to the gap data, not to vibes); for each candidate, the
difference analysis — what they would add that no current member has, and
what they would duplicate; the resemblance check — in what ways each
candidate resembles recent hires, listed explicitly so the red team can see
it; and onboarding reality — what it costs this team, at its current load, to
absorb a new person.

The framing rule for this role: the question is never "would they fit in?"
It is "can they do something the last good hire could not?" Fit is assessed
only as behavioural compatibility with how the team actually works (cited),
never as similarity.

## 4. Cost & Capacity Analyst

**Question owned:** what does this actually cost, against what alternative?

Sees the internal data slice: gap cost, comp bands, budget, team throughput.
Deliverable covers: the fully-loaded cost of the hire (salary, on-costs,
tooling, management overhead, ramp time at realistic productivity); the
measured cost of the gap continuing — and where that number is assumed
rather than measured, tagged honestly as such; the cost of each alternative
the Role Architect's brief names (contractor, automation, reshaping); and
the capacity check — whether the team as currently loaded can even onboard
someone, per the throughput data.

Every model input is `[GIVEN: E<n>]` or `[ASSUMPTION]`. Ceiling 0.25,
because a financial case built on assumed numbers reads exactly like a real
one.

## 5. Historian

**Question owned:** what happened the last times this organisation did this?

Sees `05-history.md` and past-hire outcome data. Deliverable covers: outcomes
of comparable past hires (level, role shape) — including how each was
*found*, because the sourcing channel's track record is evidence about the
current shortlist; the regret pattern — what the org regrets about past
hires, and whether the current process would catch it this time; what
happened to past non-standard hires, if any were ever made — the org's real
(not stated) tolerance for difference; and the base rate — how long
comparable hires took to become net-positive, against the assumption the
Cost & Capacity Analyst is likely making.

Recency rule: a pattern built on hires from a different era of the company
(different size, different market) is tagged `[INF]`, not `[E]`.

## 6. Talent Lead

Runs **after** the five deliverables are linted. Sees everything except the
red-team outputs (which do not exist yet — ordering is the point).

Writes two files:

- `synthesis.md` — fully tagged, ceiling 0.20. Carries claims forward from
  the role deliverables; introduces nothing new. Maps the disagreements
  mechanically (same assumption, conflicting polarity) rather than asking
  anyone to manufacture debate. Where finalists are compared, keeps
  per-candidate threads separate — no blended "overall impression".
- The memo, rendered from the synthesis per `memo-format.md`, with
  per-candidate verdicts constrained by the ledger rules in SKILL.md step 9.

The Talent Lead's hardest job is refusing the blend: the pull toward a
single agreeable recommendation is exactly the pressure the verdict
constraints exist to resist.

## Evidence slicing

Default map. Record the actual mapping in `slices.md`; write each slice as a
standalone file under `slices/`.

| role | gets | notably does not get |
|------|------|----------------------|
| role-architect | gap data, team context, org trajectory, role-owner's requirement | any candidate evidence |
| evidence-assessor | all per-candidate items: demonstrated, reference, interview, claimed | team composition, comp data |
| team-integrator | team composition, gap data, candidates' `demonstrated` items only | CVs and `claimed` items |
| cost-capacity-analyst | internal-data: gap cost, comp bands, budget, throughput | candidate evidence beyond role level |
| historian | 05-history.md, past-hire outcomes, sourcing channels used | current candidates' evidence |

When the evidence is too thin to slice five ways (early-stage org, first
hire), collapse to three roles — Role Architect, Evidence Assessor, Cost &
Capacity Analyst — rather than handing everyone everything. Say so in the
memo's limitations. Isolation that exists only on paper is worse than
honestly reduced coverage, because it launders one perspective into the
appearance of several.
