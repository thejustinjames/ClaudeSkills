# Red Team Protocol — Hiring

The red team runs after the memo is drafted, in clean contexts, and its job is
to **break the recommendation**, not to review it. Hiring is the domain where
a warm consensus feels most like evidence, which is why the refuters never see
the reasoning that produced the memo — only the conclusion and the raw
evidence file.

## Contents

- [Setup](#setup)
- [The three lenses](#the-three-lenses)
- [What counts as a refutation](#what-counts-as-a-refutation)
- [Survivability](#survivability)
- [Kill conditions](#kill-conditions)

## Setup

Three refuters, spawned as separate agents (or separate clean sessions), in
parallel. Each receives exactly:

1. The rendered memo (with its per-candidate verdicts)
2. The raw evidence file `03-evidence.md` — the full file, not a slice
3. Its lens brief from this file
4. The guardrails from SKILL.md (protected characteristics excluded;
   evidence-anchored claims only — a refutation built on a character verdict
   is discarded like any other guardrail breach)

Each does **not** receive: the role deliverables, the synthesis, the
assumption ledger, or any account of how the conclusion was reached. A
refuter who can see the reasoning attacks the reasoning's presentation; a
refuter who cannot must attack the conclusion's relationship to the evidence,
which is the attack that matters.

No refuter sees another refuter's output. Convergence between independent
refuters is the signal the survivability rules run on; letting them read each
other manufactures it.

## The three lenses

Fixed, one per refuter. These are the three ways hiring decisions actually
fail, and each lens gets a specialist rather than hoping a generalist notices.

### Lens 1 — Resemblance

Attack the recommendation as pattern-matching wearing the costume of
judgement. Is the recommended candidate recommended because of what they can
do, or because of whom they resemble? Specific attacks:

- Restate the evidence for the top candidate with every similarity-to-us
  signal removed (shared background, shared employers, familiar career
  shape). What actually remains?
- Apply the inverted criterion: what can this candidate do that the last
  good hire could not? If the memo cannot answer from cited evidence, say
  so — that is a refutation.
- Check the losing finalists: is any of them *less* similar but *better*
  evidenced on the differentiating requirement? Name them.
- Check the interview-weight problem: how much of the case rests on
  `interview` items — the native habitat of affinity — versus `demonstrated`?

### Lens 2 — False negative

Attack the comparison set itself. The memo picks the best of who was
considered; this lens asks who was never considered, and whether that
invalidates the pick. Specific attacks:

- Reconstruct the shortlist's provenance from the evidence: what fraction is
  inbound funnel? Which proxies (titles, years, credentials, keywords) were
  used as knockouts upstream, and what would they have excluded?
- Was any finding-plan channel (evidence-of-work search, public record,
  referrals-beyond-the-circle, headhunter) actually worked? If not, the
  claim "best available candidate" is unsupported — a refutation with the
  30-day observable being "work the plan for two weeks and see who appears."
- If a rejected-pile audit exists in `05-history.md`, what did it find last
  time? If none has ever run, the process's false-negative rate is unmeasured
  — attack any memo language implying the shortlist was exhaustive.

### Lens 3 — Wrong problem

Attack the role, not the candidate. The most expensive hire is the right
person for a role that should not exist. Specific attacks:

- Does the internal data support a *hiring* diagnosis? Rebuild the case that
  the gap is a process problem, a scope problem, a tooling problem, or a
  retention problem wearing a hiring costume — and check whether the memo
  ever seriously priced the alternatives.
- Stress the role against the org's trajectory: if the reorg happens, the
  product pivots, or the team's load-bearing person leaves, does this role
  still make sense? A role designed for last quarter's shape of the work is
  a refutation with a fast observable (ask the three people nearest the
  work whether the requirement matches what they see coming).
- Check capacity honestly: per the throughput data, can this team onboard
  anyone right now without the hire making the next two quarters *worse*?

## What counts as a refutation

A refutation must name **a leading indicator observable within about 30
days** — a work-trial result, a specific reference answer, a measurement, two
weeks of a finding channel being worked, an internal answer from the people
nearest the work. "The candidate might not work out" is vague pessimism:
unfalsifiable, therefore free to produce, therefore discarded.

Format per refutation:

```markdown
## R<n> | lens: <resemblance|false-negative|wrong-problem>
Claim attacked: <quote from the memo>
Refutation: <why the conclusion does not follow from the evidence>
Observable: <what could be seen within ~30 days that would confirm this>
Evidence cited: [E<n>, ...]
```

## Survivability

The Talent Lead answers each refutation from the *existing* evidence — no new
claims. A refutation **survives** unless it is directly contradicted by a
cited evidence item. "We considered that" is not an answer; a citation is.

Surviving refutations are delivered unresolved in the output (SKILL.md,
Output section). Resolving one by picking a side and writing smoothly over it
is the most expensive thing this process can do — it is how regretted hires
get made politely.

## Kill conditions

Applied mechanically after survivability is settled:

- **Two or more surviving refutations on the same load-bearing assumption**
  → that candidate's verdict cannot be `hire`; it becomes `trial` (the trial
  that resolves the assumption) or `keep-looking`.
- **A surviving false-negative refutation showing the shortlist was
  funnel-only with proxy knockouts** → `keep-looking` runs alongside any
  per-candidate verdict; the finding plan executes before any offer.
- **A surviving wrong-problem refutation on the role itself** → the verdict
  for the *role* is `reshape` (or close the req), regardless of how strong
  the leading candidate is. Hiring an excellent person into a broken role
  converts one problem into two.

If all three refuters return nothing that survives, treat it as suspicious
rather than reassuring — check that they were genuinely isolated and that
the memo made falsifiable claims at all. A memo no one can attack is usually
a memo that asserts nothing.
