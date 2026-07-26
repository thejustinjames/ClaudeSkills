# Hiring Team

> **📦 You are looking inside a Claude skill.** This folder is the unpacked contents of
> [`hiring-team.skill`](../../hiring-team.skill). [`SKILL.md`](SKILL.md) is the canonical
> playbook Claude loads; [`references/`](references/) holds step-specific depth,
> [`assets/`](assets/) holds templates and worked examples, and [`scripts/`](scripts/)
> holds the deterministic checks. (This README is added for browsing on GitHub and is
> not part of the package.)

**Strategy · Talent · Hiring decisions**

A harness for making a hiring decision well — built as a variant of
[`decision-team`](../decision-team/) using the adaptation procedure in
[`docs/creating-and-adapting-skills.md`](../../docs/creating-and-adapting-skills.md),
and grounded in the thesis of the essay
[*You Cannot Hire the Future Through a Filter Trained on the Past*](https://justinjames.co.uk/journal/hire-the-future/):
the standard pipeline is a machine for converging on the average, and the
people who would elevate a team are precisely the ones it is built to reject.

## What it keeps from `decision-team` (the invariant core)

- **An evidence gate** — no analysis on thin inputs; a failed gate produces an
  Evidence Acquisition Plan (usually: a paid work trial, two structured
  reference calls, or a week measuring the gap) instead of a fictional memo.
- **Isolated roles with sliced evidence** — five analytical perspectives run
  as separate agents so "everyone loved her" cannot happen by contagion.
- **Claim traceability** — every claim about a candidate tagged to evidence or
  flagged as an assumption, enforced by the lint script.
- **Refutation after synthesis** — a clean-context red team, refutations only
  count with a ~30-day observable.
- **A ledger-bound verdict** — hire / reshape / trial / keep-looking,
  constrained by untested load-bearing assumptions, not by interview warmth.

## What it changes (the hiring-specific surface)

- **The evidence hierarchy inverts the pipeline's.** `demonstrated` work
  (code read, things shipped, a paid trial, watching someone reason) and
  conducted `reference` calls outrank `interview` impressions, and CV
  `claimed` items rank last — recorded only so they can be corroborated.
- **A gates-vs-proxies audit** runs before anything else: genuine hard gates
  (right to work, licence, language, true location) are stated first;
  years-of-experience, exact titles, and credentials are demoted from
  knockouts to soft signals.
- **Finding over filtering.** The sourcing plan is part of the decision; a
  shortlist that is 100% inbound funnel invalidates "best available
  candidate" and triggers a keep-looking verdict alongside any per-candidate
  call.
- **The red team's three lenses are hiring's real failure modes:**
  resemblance dressed as fit, false negatives created upstream by proxy
  knockouts, and roles that are process problems wearing a hiring costume.
- **A standing trial card prices the invisible cost:** the quarterly
  rejected-pile audit — the only measurement the false negative ever gets.
- **Hard guardrails:** protected characteristics are out of bounds
  everywhere; claims describe evidence and behaviour, never character; no
  invented psychometrics; decision support for a named human, never bulk
  screening.

## The roles

| Role | Question owned | Notably never sees |
|------|----------------|--------------------|
| Role Architect | What does this role irreducibly need — and is a role the right container? | Any candidate evidence |
| Evidence Assessor | What has each candidate demonstrated, versus claimed? | Team composition, comp data |
| Team Integrator | What would this person make the team capable of that it is not now? | CVs and claimed items |
| Cost & Capacity Analyst | What does this cost, against what alternative? | Candidate evidence |
| Historian | What happened the last times we did this? | Current candidates |
| Talent Lead | Synthesis — carries claims forward, introduces none | Red-team output (runs before it) |

## Quick start

```bash
python scripts/init_workspace.py senior-data-role
# fill 02-decision.md and 03-evidence.md, then:
python scripts/evidence_lint.py --gate --evidence <workspace>/03-evidence.md --stage candidate
```

If the gate fails, the deliverable is the acquisition plan — and that is the
skill working. See [`assets/examples/worked-example.md`](assets/examples/worked-example.md)
for a full run of each path.
