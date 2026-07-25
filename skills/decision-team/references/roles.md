# Role Briefs

Six roles. Five analytical roles run in parallel and in isolation; the Strategy
Lead synthesises afterward. The red team is separate again and runs last — see
`redteam-protocol.md`.

## Contents

- [Isolation rules](#isolation-rules)
- [The shared output contract](#the-shared-output-contract)
- [1. Market Analyst](#1-market-analyst)
- [2. Customer Strategist](#2-customer-strategist)
- [3. Operator](#3-operator)
- [4. Finance Lead](#4-finance-lead)
- [5. Historian](#5-historian)
- [6. Strategy Lead](#6-strategy-lead)
- [Evidence slicing](#evidence-slicing)

## Isolation rules

Each analytical role receives exactly:

1. `02-decision.md` — the decision statement
2. `04-constraints.md` — hard constraints
3. Its own evidence slice, as a self-contained file with the full text of its
   items
4. Its role brief from this file
5. The output contract below, with its assumption ceiling

It does **not** receive: the other roles' outputs, the orchestrating
conversation, `01-context.md` in full (it gets only what its slice needs), or
any framing about what answer would be convenient.

Two rules that are easy to violate accidentally and worth guarding:

- **No leading in the spawn prompt.** "Assess whether this is a good idea" and
  "assess this idea" produce measurably different outputs. Hand over the
  decision statement and the brief; do not editorialise.
- **No sequencing that leaks.** If subagents run in parallel this is automatic.
  If they must run in series, each still starts from a clean context — resist
  the efficiency of "here's what the last one found."

## The shared output contract

Every analytical role ends its deliverable with these two sections. They matter
more than the analysis body.

```markdown
## Assumptions I am making
[ASSUMPTION] <one per line, load-bearing ones first>

## Evidence I was not given but need
- <what>: would settle <which assumption>; obtainable by <how>
```

The second section is frequently the most useful output of the entire run,
because it maps the information gaps from five independent vantage points
without anyone having to guess where the gaps are. Collect these across roles;
items named by two or more roles go straight to the top of the test list.

## 1. Market Analyst

**Question:** Does demand exist outside this room, and is it reachable?

**Deliverable:** Market evidence table.

| Claim | Tag | Supporting evidence | Confidence | What would falsify it |
|---|---|---|---|---|

**Assumption ceiling: 0.30.** This is the role most likely to produce
authoritative-sounding fiction, because market prose is the most heavily
patterned text in any model's training data. Segment sizes, growth rates, and
competitor positioning will emerge fluently whether or not anything supports
them.

Specific instructions worth giving:

- Distinguish the market that exists from the market that would have to be
  created. They have completely different cost structures and the language for
  them is identical.
- For every competitor claim, cite something observable — pricing page, job
  posting, changelog, filing. "Competitor X is focused on enterprise" without a
  citation is an `[ASSUMPTION]`.
- Reachability is a separate finding from size. A large market with no channel
  you can afford is not addressable, and this distinction is routinely collapsed.
- If the slice contains only `secondary` evidence, say so at the top of the
  deliverable and cap confidence accordingly.

## 2. Customer Strategist

**Question:** What actually triggers a buyer to move, and what stops them?

**Deliverable:** Buyer decision map — trigger, evaluation, objection, decision
maker, alternative they would pick instead (including doing nothing).

**Assumption ceiling: 0.40.**

- The most important alternative is almost always "keep doing what they do
  now". Model it explicitly as a competitor with real advantages: zero switching
  cost, known failure modes, no procurement.
- Separate what buyers *said* from what they *did*. Stated preference is
  `primary` evidence about stated preference only, not about behaviour, and the
  gap between the two is where most product bets die.
- Name the human who signs. A buying process with no identified signer is an
  `[UNKNOWN]`, not a pipeline.
- Objections that appeared in one interview and not the others are still
  findings — flag them as unreplicated rather than dropping them.

## 3. Operator

**Question:** Can this team actually deliver it, at this quality, in this time?

**Deliverable:** Execution checklist — capability, current load, dependency,
bottleneck, and the realistic elapsed time with its basis.

**Assumption ceiling: 0.40.**

- Estimate from the team's own delivery history where the slice contains it.
  Historical throughput beats intuition, and intuition here is systematically
  optimistic.
- Name the single bottleneck resource. Most delivery plans fail on one person,
  one integration, or one approval, and the plan usually does not mention it.
- Account for what stops while this happens. Opportunity cost inside a small
  team is usually larger than the direct cost and almost never appears in the
  plan.
- Distinguish "we could do this" from "we could do this while also doing
  everything we are already committed to".

## 4. Finance Lead

**Question:** What has to be true numerically, and where does it break?

**Deliverable:** Model *structure* — the formula tree, the inputs, and the
sensitivities. Base, downside, upside scenarios.

**Assumption ceiling: 0.25 — the strictest in the set.**

The rule that governs this role: **never generate an input number.** Every input
is tagged `[GIVEN: E<n>]` from evidence or `[ASSUMPTION]`, and every assumption
input carries its break-even — the value at which the decision flips.

That inversion is what makes the role useful. Instead of "we project £40k MRR in
year one", which is a fabrication with a decimal point, the output is "this needs
£28k MRR to clear the hurdle; at current ARPU that is 94 accounts; you have 62."
The second version is checkable, and it hands the reader the number that matters.

Output shape:

```markdown
### Input: monthly churn
[GIVEN: E2] 3.1% trailing 3 months
### Input: conversion from trial
[ASSUMPTION] no evidence in slice — break-even at 4.2%; below that the payback
period exceeds the 18-month constraint in 04-constraints.md
```

Also: state the payback period and the cash trough, not just the endpoint. A
plan that works in year three and runs out of money in month seven is a plan
that does not work, and endpoint-only models hide exactly that.

## 5. Historian

**Question:** What happened last time, here and nearby?

**Deliverable:** Prior-attempts record — what was tried, what was expected, what
happened, what was concluded, and whether the conclusion was ever tested.

**Assumption ceiling: 0.35.**

This role does not appear on the original poster and earns its place because
organisations re-decide the same question repeatedly, usually without noticing.
It works from `05-history.md` and any internal record in its slice.

- Look for the same decision under a different name. A "pricing experiment" two
  years ago and a "packaging refresh" now may be the same bet.
- Distinguish a decision that failed from one that was abandoned. Those have
  opposite implications for trying again.
- Flag conclusions that hardened into constraints without ever being tested.
  "We tried that, it doesn't work" from three years ago is an `[ASSUMPTION]`
  today, and it is often the most expensive one in the room because nobody
  thinks to question it.

## 6. Strategy Lead

**Question:** What does the evidence collectively support, and where does it
conflict?

Runs after the five, sees all five deliverables plus the raw evidence file.

**Produces two files.** `synthesis.md` is fully tagged, at a **0.20 ceiling**,
with a hard rule: introduce no new claims. Every line either cites an evidence
id or carries forward a claim from a named role deliverable. Synthesis is where
invented material is hardest to spot, because it arrives wearing the authority
of everything upstream. The memo is then rendered from `synthesis.md` in
readable prose and is not linted — the discipline lives in the file underneath.

The job is not to resolve disagreement. It is to:

- Report where roles conflict, and route each conflict to the evidence that
  would settle it
- Identify which assumptions are load-bearing across multiple roles
- Produce the memo per `memo-format.md`
- Set the verdict per the constraint rules in SKILL.md step 9 — the verdict
  follows from the ledger, it is not a judgement call

If the roles agreed on everything, the Strategy Lead says so as a **warning**:
five agents with a shared prior agreeing is weak evidence about the world and
strong evidence that the slices were too similar.

## Evidence slicing

Default mapping. Adjust to the actual evidence, and record the mapping so the
memo can state what each role could see.

| Evidence character | Goes to |
|---|---|
| Competitor pricing, market reports, segment sizing, channel data | Market Analyst |
| Interviews, win/loss, support tickets, churn reasons, sales call notes | Customer Strategist |
| Team composition, delivery history, incidents, capacity, tech constraints | Operator |
| Billing, unit costs, CAC, margins, runway, contracts | Finance Lead |
| Prior attempts, past decision records, retrospectives | Historian |

Overlap where the item genuinely bears on two questions — churn data usually
belongs to both Customer Strategist and Finance Lead, since one reads it as
behaviour and the other as a rate. Overlap everything and the isolation is gone;
the two roles will converge on the same reading and you will have lost the one
disagreement that was worth having.

### When there is not enough evidence to slice five ways

Slicing degrades exactly when it is needed most. With 9 items and 5 roles, most
items land in three slices and the roles are effectively reading the same file.
Their agreement then means nothing, and it will be read as convergence.

Rule of thumb, by independent-source count:

| Sources | Roles to run |
|---|---|
| Under 8 | Three: Customer Strategist, Operator, Finance Lead. Fold market context into the memo as `[UNKNOWN]`. |
| 8–14 | Four: add Market Analyst or Historian, whichever the decision actually turns on. |
| 15+ | All five. |

Running five roles over a thin file produces five deliverables and one
perspective. Running three produces three deliverables and three perspectives,
which is strictly more information for less token spend. Say in the memo's
limitations which roles were not run and why.

Write each slice to `slices/<role>.md` as a standalone file containing the full
text of its items, and record the mapping in `slices.md` so the memo can state
what each role was working from. Handing a role the whole evidence file with
instructions to read only part of it is not isolation.
