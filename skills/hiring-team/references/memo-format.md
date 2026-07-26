# Memo Format — Hiring

The memo is one page. It is rendered from the tagged `synthesis.md` and is
not itself linted — a page with a citation tag on every line is unreadable,
and an unreadable memo does not get read. The synthesis it came from is the
auditable artifact.

## Contents

- [The decision memo](#the-decision-memo)
- [The evidence-quality footer](#the-evidence-quality-footer)
- [The assumption ledger](#the-assumption-ledger)
- [Trial cards](#trial-cards)
- [The structured reference protocol](#the-structured-reference-protocol)
- [Candidate communication](#candidate-communication)

## The decision memo

```markdown
# <Role / decision> — decision memo
Date: <date>   Decision-maker: <named human>   Analysis: hiring-team run <slug>

## Decision being made
<One sentence: which of the four decisions this is, and the alternative it
was weighed against.>

## The irreducible requirement
<The differentiating thing this role must do, in the role-owner's words —
one sentence. This is the sentence a template JD would have averaged away.>

## Verdict
<Per candidate, where finalists are compared:>
- <Candidate A>: hire | reshape | trial | keep-looking — <one-line reason,
  naming the binding constraint from the ledger or red team>
- <Candidate B>: ...
<And for the role itself, when stage=role or a wrong-problem refutation
survived: open | reshape | close.>

## What this rests on
<The 3–5 load-bearing claims, each with its evidence character stated in
prose: "demonstrated in the work trial", "corroborated by two references",
"assumed — trial card T2".>

## What would change it
<The top untested assumptions, straight from the ledger, each pointing at
its trial card.>

## Surviving refutations and open disagreements
<Unresolved, as they are. Lens and observable for each.>

## Limitations
<Isolation compromises, excluded material (protected characteristics),
thin slices, asymmetric evidence across finalists, funnel-only shortlist.>
```

Verdict vocabulary, constrained by SKILL.md step 9:

- `hire` — allowed only when no forcing rule triggered
- `reshape` — the offer, the role scope, or the level changes first
- `trial` — the default under uncertainty: a specific card, not a vibe
- `keep-looking` — the comparison set was inadequate; the finding plan runs

## The evidence-quality footer

Every memo ends with this block, verbatim format. Never remove it to make
the memo read better — it is the reader's only way to calibrate what they
are holding:

```markdown
---
Evidence: <n> items — <d> demonstrated, <r> reference, <i> internal-data,
<v> interview, <c> claimed, <s> secondary, from <k> independent sources.
Load-bearing claims resting on demonstrated/reference evidence: <x> of <y>.
Uncorroborated claimed items still load-bearing: <list of E-ids, or "none">.
Assumption share of synthesis: <ratio>. Gate: PASS | MARGINAL | (stage).
This analysis supports a decision by a named human. It is not an automated
screening result and must not be used to reject applicants in bulk.
---
```

## The assumption ledger

Same schema as the decision-team skill; `scripts/rank_assumptions.py` parses
it and applies the forcing rule (load-bearing, priority ≥ 16, untested →
verdict capped at `trial`).

| id | assumption | load_bearing | importance | uncertainty | test | cost | status |
|----|-----------|--------------|------------|-------------|------|------|--------|

Hiring examples of load-bearing assumptions worth writing down explicitly:
"can operate at our scale, not just their last company's", "wants to build,
not just advise", "the role survives the reorg", "comp band is actually
competitive for this profile", "the team has onboarding capacity this
quarter".

## Trial cards

The primary deliverable. Three to five, cheapest first. Thresholds are
written **before** the trial runs and timestamped — pre-commitment is the
only defence against reinterpreting a disappointing result as encouraging.

```markdown
## T<n> — <name>
Resolves: A<n> (<assumption>)
Trial: <exactly what will be done>
Cost: <money and hours, including the candidate's — paid where it is their time>
Sample/duration: <how much, how long>
Committed <date>:
  Pass:    <observable threshold — proceed on this assumption>
  Reshape: <the band between — what changes>
  Fail:    <observable threshold — the assumption is false>
```

The standard hiring trials, in rough cost order:

1. **Artifact read** (hours, free): read the candidate's actual work — code,
   documents, talks — against the irreducible requirement, notes taken
   before any discussion.
2. **Structured reference calls** (hours): protocol below. Two minimum;
   pass/fail thresholds set on the answers to the specific questions, not on
   overall warmth.
3. **Paid work sample** (half-day to two days, paid at a fair rate): a real
   problem from the role's actual queue, scoped so it is completable;
   evaluation rubric written before the candidate starts. Note what is
   artificial about the conditions.
4. **Build-together session** (two hours): reason through a live problem
   with the team members closest to the work. Evaluates judgement in
   motion; the rubric is about how they think, evidenced by what they said
   and did, not how they made anyone feel.
5. **Structured probation / 30-60-90** (for post-offer assumptions): the
   checkpoints are observable deliverables written into the plan before the
   start date — a probation period without pre-committed checkpoints is a
   vibe with a calendar.

**The standing card — the rejected-pile audit.** Included in every run's
output regardless of verdict:

```markdown
## T-standing — Rejected-pile audit
Resolves: the process's unmeasured false-negative rate
Trial: once a quarter, a human (the role-owner, not a screener) reads a
  random sample of 20 rejected applications from the period, looking for
  the non-standard excellent — unusual combinations, non-linear paths,
  demonstrated work the filter could not parse.
Committed thresholds: >=2 candidates in the sample worth a conversation →
  the screening criteria are rejecting talent; the proxies get re-audited
  (gates-and-finding.md) before the next req opens.
Feeds: 05-history.md for every subsequent run.
```

## The structured reference protocol

References are `reference`-type evidence only when conducted like this:

- **You make the call.** A forwarded letter or a LinkedIn endorsement is
  `claimed`, not `reference`.
- **Specific questions, decided in advance**, aimed at the load-bearing
  assumptions — not "what are they like?" but "walk me through the hardest
  thing they shipped — what was their actual contribution?", "what work
  should they not be given?", "would you hire them again — for what role
  specifically, and what role not?"
- **Record hesitations verbatim.** The pause before "...yes" is evidence;
  the Evidence Assessor weighs it, so it must be captured, not smoothed.
- **Ask for behaviour, accept no character verdicts.** If the referee says
  "brilliant but difficult", the follow-up is "tell me about a specific time
  that difficulty showed up — what happened?" The behaviour goes in the
  evidence item; the adjective does not.
- Candidate-supplied referees are fine but noted as such; independence in
  the gate count comes from at least one referee found through the work
  itself (the co-author, the maintainer who reviewed their PRs) — where
  appropriate and lawful in the jurisdiction, and never behind the
  candidate's back at their current employer.

## Candidate communication

The process's dignity rules produce two concrete artifacts:

- **The advert opens with the gates.** Every genuine hard gate, plainly
  stated, in the first lines — before anyone spends an hour on an
  application they were never eligible to make.
- **Rejected finalists get an evidence-grounded reason.** One or two
  sentences, anchored to the requirement ("we hired for depth on X; your
  demonstrated strength is Y") — never a character judgement, never
  boilerplate. Anyone who reached a work trial or reference stage gave real
  time; the reason is what that time purchased.
