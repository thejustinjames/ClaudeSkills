# Evidence Protocol — Hiring

Everything downstream is bottlenecked here. A hiring analysis is only as good
as the weakest link in the chain of claims that produced it, and hiring is the
domain where the weakest links are the most fluent: a polished CV, a rehearsed
interview answer, a warm feeling after a good conversation. This file defines
the hierarchy that keeps those in their place.

## Contents

- [The hierarchy](#the-hierarchy)
- [Evidence file format](#evidence-file-format)
- [The gate](#the-gate)
- [Claim tagging](#claim-tagging)
- [Lint thresholds](#lint-thresholds)
- [Evidence hygiene](#evidence-hygiene)

## The hierarchy

Six types, in strength order. The top three are **strong**; the gate counts
only those.

| type | what it is | why it ranks here |
|------|-----------|-------------------|
| `demonstrated` | Work product you actually examined: code read, things shipped, writing, talks, open-source, a paid work trial, watching them reason through a real problem live | The actual work, visible, and hard to fake. Demonstrated beats described, every time |
| `reference` | A structured reference conversation **you conducted**, with specific questions (see memo-format.md for the protocol) | Judgement from someone who watched them work — texture no filter captures. A written letter is not this |
| `internal-data` | Your own numbers, exported not remembered: what the gap costs now, team throughput, comp bands, past-hire outcomes | Grounds "we're drowning" and "we can afford it" in something checkable |
| `interview` | Behaviour you observed in your own interviews | Real but rehearsable, and the native habitat of resemblance bias — mid-weight, never load-bearing alone |
| `claimed` | CV, application, LinkedIn statements | A claim, not evidence. Recorded so it can be checked against `demonstrated` — never sufficient on its own |
| `secondary` | Public reports, salary surveys, market data — carries a URL | Context for the role decision, not for the person |

The inversion this table exists to prevent: pipelines screen on `claimed`
(legible, keyword-matchable) and mostly ignore `demonstrated` (illegible to a
parser). That rewards continuous employment, exact titles, and keyword
density, and punishes non-linear paths and unusual combinations — the exact
signature of the person who elevates a team. The hierarchy here is the
pipeline's, inverted back the right way up.

## Evidence file format

`03-evidence.md` holds one block per item. The lint script parses the header
line, so the format matters:

```markdown
## E1 | type: demonstrated | source: Candidate's PR review on acme/parser, read 2026-07-20 | date: 2026-07-20
Read four merged PRs. Refactors before extending; commit messages explain why,
not what. Flagged a race condition in review that two maintainers had missed.

## E2 | type: reference | source: Call — former eng manager at Priorco, 30 min | date: 2026-07-22
"Best debugger on the team, wanted the gnarly tickets." On weaknesses:
"deadlines slip when the problem is interesting." Would hire again: yes,
"for depth, not for a delivery-lead seat."

## E3 | type: internal-data | source: Sprint export Q2 2026 | date: 2026-07-01
Team closed 61% of committed points; the two data-heavy epics slipped twice.
On-call load: 9 pages/week, 6 of them from the ingestion service.

## E4 | type: claimed | source: CV, section 2 | date: 2026-07-15
States "led migration of billing platform, 40% cost reduction." No artifact
offered; not yet checked against E1/E2.
```

Rules that matter:

- Ids are `E<n>`, sequential, never reused. Retracted items keep their id,
  body marked `RETRACTED — <why>`.
- One source per item. Splitting one reference call into four well-scoped
  items is good citation hygiene; the gate counts sources, so it does not
  inflate anything.
- **Strip protected characteristics on entry.** If source material mentions
  age, health, family status, or anything else on the out-of-bounds list, the
  evidence item records the work-relevant content only, and the memo's
  limitations note that material was excluded. This is not optional.
- Never write an item from your own priors. Researched context is `secondary`
  with a URL. There is no evidence type for "everyone knows".

## The gate

Run before any role is spawned:

```bash
python scripts/evidence_lint.py --gate --evidence 03-evidence.md --stage role
python scripts/evidence_lint.py --gate --evidence 03-evidence.md --stage candidate
```

Both stages require **five strong items (demonstrated + reference +
internal-data) from independent sources**. On top of that:

- `--stage role` ("should this role exist?") **fails** on zero
  `internal-data`: nobody has measured what the gap costs, so the case is
  "we're drowning" — a feeling, not a finding. The cheapest acquisition is
  almost always a week of measurement.
- `--stage candidate` ("should we hire this person / which finalist?")
  **fails** on zero `demonstrated` items: the analysis would run entirely on
  claims and interview polish, which is the resemblance machine with extra
  paperwork. The cheapest acquisition is almost always a paid work sample or
  two artifact-reads.

A failed gate produces an **Evidence Acquisition Plan**: the three cheapest
things to learn this week, what each would settle, and what you would do
differently depending on the answer. Typical entries: export and read the
sprint/gap data; design a half-day paid work trial around the role's actual
hardest problem; conduct two structured reference calls; read the candidate's
public work for an hour. Say plainly that a memo now would be fiction. A user
who came for "should we hire her?" and left with a work-trial design got the
better deal.

The script prints what it cannot check — apply those yourself, particularly:
does the decision hinge on a capability no evidence item demonstrates, and
is every reference from the candidate's own curated list? (References the
candidate hand-picked are still `reference` type, but the gate's independence
count is the reason to find one back-channel who is not on the list — where
that is appropriate and lawful in your jurisdiction.)

## Claim tagging

Identical scheme to the decision-team skill, enforced by the same linter:

- `[E3]` / `[E3,E7]` — directly stated in those items
- `[INF: E3,E7]` — inference beyond what the items state
- `[GIVEN: E3]` — a model input taken from evidence (Cost & Capacity Analyst)
- `[ASSUMPTION]` — grounded in nothing given; goes to the ledger
- `[UNKNOWN]` — a flagged gap, not a claim; never penalised

The hiring-specific rule: **a claim about a person tagged only to `claimed`
evidence is still a claim.** "Led the billing migration [E4]" where E4 is the
CV records that the CV says so — the Evidence Assessor's job is to note which
`claimed` items have a corroborating `demonstrated` or `reference` item and
which are load-bearing yet uncorroborated. Uncorroborated-but-load-bearing
goes straight to the assumption ledger.

## Lint thresholds

Assumption ratio = `[ASSUMPTION]` / (evidence + inference + given +
assumption), per deliverable, linted against the role's own slice:

| role | ceiling | why |
|------|---------|-----|
| evidence-assessor | 0.25 | Confident fiction about capability is the costliest failure in hiring |
| cost-capacity-analyst | 0.25 | A financial case built on assumed numbers reads exactly like a real one |
| role-architect | 0.35 | Requirement design needs room to hypothesise |
| team-integrator | 0.40 | Reasoning about complements is inherently inferential |
| historian | 0.35 | Pattern claims must cite actual past hires |
| talent-lead | 0.20 | Synthesis carries claims forward, never introduces them |

`[UNKNOWN]` share above ~35% is a note, not a failure: the slice was too thin
for that role, and that belongs in the memo's limitations.

## Evidence hygiene

- Date everything. A reference from three jobs ago describes a person who may
  no longer exist; the Historian weighs recency explicitly.
- An interview impression written down the next day is already fiction.
  Capture `interview` items same-day or mark the delay in the item.
- The work trial is evidence about the trial's conditions too. Note what was
  artificial (time pressure, unfamiliar codebase, audience) so the Evidence
  Assessor can weigh it rather than discover it.
- When comparing finalists, every candidate needs the same evidence types
  collected with the same effort. An analysis where candidate A has a work
  trial and candidate B has a warm referral is comparing apples to
  enthusiasm — the memo must say so if it cannot be fixed.
