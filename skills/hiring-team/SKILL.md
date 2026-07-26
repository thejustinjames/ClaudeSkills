---
name: hiring-team
description: Run a rigorous multi-role analysis on a hiring decision using isolated role agents, an evidence hierarchy that ranks demonstrated work above claimed credentials, adversarial red-teaming for resemblance bias, and verdicts bound to an assumption ledger. Use whenever someone is weighing a real hiring call — open a new role, choose between finalists, decide on a specific candidate, make a key or exec hire, replace someone, make a first hire, or decide whether to hire at all versus contracting or restructuring. Also use when they want a job description audited for proxies dressed as requirements, a sourcing plan that finds candidates instead of filtering applications, a work-trial designed with pre-committed thresholds, or a red-team critique of a hire they are already leaning toward. Trigger even when the request is casual ("should we bring on a...", "I can't decide between these two", "we need someone senior") as long as a real hire is at stake.
---

# Hiring Team

A harness for making a hiring decision well. Five analytical roles run in
isolation, every claim about a candidate is traced to evidence or flagged as an
assumption, an independent red team attacks the recommendation for resemblance
bias and false negatives, and the verdict is bound to a ledger rather than to
whoever interviewed most recently. The primary output is a short list of cheap,
falsifiable trials — not a gut feel with a scorecard stapled to it.

## The thesis this skill is built on

Most hiring pipelines are machines for converging on the average. The job
description gets written from a template, drifts toward the mean of every role
like it, and then a filter screens for what is *legible* rather than what is
*good* — exact titles, keyword density, unbroken employment — systematically
rejecting the non-standard excellent while waving through the standard
adequate. The people who would elevate a team are, by definition, the ones who
do not match a profile built from the people who came before them.

Two asymmetries keep this invisible:

- **The false-negative asymmetry.** The cost of a bad interview is visible and
  immediately felt, so the pipeline is engineered to minimise it. The cost of
  the brilliant candidate filtered out before any human saw them is real,
  often enormous, and completely unmeasured — you cannot grieve a hire you
  never knew you missed.
- **The accountability asymmetry.** Hiring managers are punished for visible
  bad hires and never for invisible missed ones, so the safest candidate
  becomes the most attractive candidate — not the best one, the least likely
  to create accountability.

This skill exists to price both asymmetries back into the decision. Three
structural properties do most of the work:

1. **An evidence hierarchy with demonstrated work at the top.** A CV is a
   claim. Code, shipped products, writing, talks, a paid work trial, watching
   someone reason through a real problem — that is evidence. The gate refuses
   a "hire" verdict that rests entirely on claims and interview polish.
2. **Isolation.** Roles run as separate agents with disjoint evidence slices,
   so "everyone loved her" cannot happen by contagion. Agreement between
   evaluators who watched the same interview is not converging evidence; it is
   a shared impression wearing five costumes.
3. **Refutation aimed at the known failure modes.** The red team runs
   afterward, in a clean context, and attacks along the three lines hiring
   actually fails on: resemblance dressed as fit, false negatives created by
   proxy requirements, and roles that are really process problems wearing a
   hiring costume.

## Scope and guardrails — read first, non-negotiable

This produces decision support for a named, accountable human. It is not an
applicant screening system and must never be used to bulk-filter or
auto-reject applicants; automated employment screening is regulated in many
jurisdictions (and hiring is a high-risk category under the EU AI Act) — the
output here is analysis for a human decision-maker, and the memo says so.

- **Protected characteristics are out of bounds.** Never request, infer,
  estimate, or use age, sex, gender identity, race, ethnicity, nationality,
  religion, disability, health, pregnancy, sexual orientation, marital status,
  or union membership — not in evidence, not in analysis, not in "culture fit"
  by another name. If supplied material contains them, exclude them from every
  slice and say so in the memo's limitations.
- **Describe evidence, never character.** Claims about candidates are anchored
  to observed behaviour and work product. Banned in anything composed here:
  personality verdicts ("narcissist", "lazy", "not a leader"), intelligence
  claims, and any medical, psychological, or diagnostic framing. "In the work
  trial, refactored the brief twice before writing code [E4]" is admissible;
  "detail-oriented person" is not — it is a character claim wearing an
  adjective.
- **No invented instruments.** Do not compose quiz-style assessments, score
  personality, or simulate psychometrics. If the organisation uses a formal
  validated occupational instrument, its properly-administered result enters
  as one evidence item like any other — never a knockout, never a diagnosis.
- **Candidate dignity is part of the process, not a courtesy.** Hard gates go
  at the top of the advert before anyone invests an hour of hope. Rejected
  finalists get a reason grounded in evidence. The rejected pile gets audited
  (step 10) — the false negative is the only cost nobody else is measuring.

## Before anything else: which decision is this?

Hiring hides four different decisions, and they have different evidence needs:

- **Open a role?** — is this a hiring problem at all, versus a process gap,
  a scope problem, or work that should be contracted or automated?
- **Where will people come from?** — the sourcing decision; the funnel is a
  choice, not a given.
- **Choose between finalists** — comparative, per-candidate verdicts.
- **Hire this specific person?** — often arrives pre-decided; the red team
  matters most here.

State which one is being made in `02-decision.md`. A run can cover two
adjacent ones (open + sourcing; compare + decide) but never all four at once.

## Workflow

Run these in order. Steps 2–3 can end the run — and when they do, that is the
skill working.

### 1. Build the workspace and state the real requirement

```bash
python scripts/init_workspace.py <role-or-candidate-slug>
```

Fill only `02-decision.md` and `03-evidence.md` now — the gate may end the run.

Interview the **role-owner** — the person who actually understands the work —
for the decision statement, in their own words. Do not accept a template job
description as the requirement, and do not draft one from a generic prompt:
the differentiating requirement dies in translation, one reasonable hand-off
at a time. The statement needs: the specific, irreducible thing this role must
do that the current team cannot; the alternatives (not hiring, contracting,
reshaping an existing role, automating); the date; observable success at six
months; the fully-loaded budget. Mark anything the role-owner cannot supply
`[NOT SUPPLIED]` — those gaps are the first finding.

Watch for the decision arriving as a yes/no on one attached candidate.
"Should we hire X?" nearly always hides "what does this role actually need,
and is X the best of everyone we could *find* — or the best of everyone who
happened to apply?"

### 2. Audit the gates, then plan the finding

Read `references/gates-and-finding.md`, then do both halves:

- **Gates vs. proxies.** List the genuine hard gates (right to work, licence,
  language the work demands, true location requirement) — these go at the top
  of any advert, stated plainly. Then list every requirement that is actually
  a proxy: years-of-experience, exact titles, credential names, "gaps" in
  employment. Proxies are demoted to soft signals. A proxy used as a knockout
  is how the future gets filtered out, and the red team is instructed to
  attack any shortlist built on one.
- **Finding, not just filtering.** Record in `02-decision.md` where candidates
  will come from *besides* inbound applications: evidence-of-work search,
  public record of how people reason, places people do the work rather than
  apply for it, trusted judgement (with the echo-chamber guard), a real
  headhunter if the role warrants one. A shortlist that is 100% funnel is a
  finding the memo must state — the best people are usually employed, not
  applying.

### 3. Load evidence and run the gate

Populate `03-evidence.md` per `references/evidence-protocol.md`: one block per
item, each with an `E<n>` id, a source, and a type from the hiring hierarchy —
`demonstrated` (work product you actually examined; a trial; watching them
reason), `reference` (a structured reference call you conducted),
`internal-data` (your own numbers on the gap and the team), `interview`
(observed in your interviews — rehearsable, mid-weight), `claimed` (CV and
application statements — never sufficient alone), `secondary` (public reports,
salary surveys — carries a URL). Never write an evidence item from your own
priors.

```bash
python scripts/evidence_lint.py --gate --evidence <workspace>/03-evidence.md \
    --stage role|candidate
```

`--stage role` is for "should we open this?" — it fails hard when there is no
internal data on what the gap costs, because "we're drowning" with no
measurement is how roles get opened that shouldn't exist. `--stage candidate`
is for deciding on people — it fails hard when there are zero `demonstrated`
items, because a decision built on claims plus interview polish is exactly the
resemblance machine this skill exists to break.

If the gate fails, produce an **Evidence Acquisition Plan** — the three
cheapest things to learn this week (measure the gap; design a paid work
trial; make two structured reference calls; go watch the candidate build
something) — and stop. Do not spawn a role.

### 4. Fill the rest of the context, then slice

Now interview for `01-context.md` (team composition and what it lacks),
`04-constraints.md`, and `05-history.md` (past hires at this level, how each
was found, the regret rate — the funnel's own track record is evidence).

Assign evidence to roles per the map in `references/roles.md` and write each
slice as a standalone file under `slices/`. The slicing rule that matters
here: **no role except the Evidence Assessor gets the CV.** The Team
Integrator reasons from the team's gaps and the candidate's demonstrated
work; the Cost & Capacity Analyst from the numbers; the Historian from past
hires. What each would conclude *without* the credential story is the point
of the isolation.

### 5. Run the roles in isolation

Spawn the five analytical roles as separate agents, in parallel, each
receiving only: `02-decision.md`, `04-constraints.md`, its slice, its brief
from `references/roles.md`, and the output contract. The five are **Role
Architect**, **Evidence Assessor**, **Team Integrator**, **Cost & Capacity
Analyst**, and **Historian**. (The Talent Lead synthesises later; the red team
runs after that — the ordering is the point.)

Every deliverable ends with "Evidence I was not given but need." Collect
these; items named by two or more roles go straight to the trial list.

If subagents are unavailable, run each role in a separate session with only
its slice. Running them as turns in one conversation defeats the design — if
unavoidable, say so in the memo's limitations rather than pretending the
isolation held.

### 6. Lint the deliverables

```bash
python scripts/evidence_lint.py <workspace>/roles/evidence-assessor.md \
    --evidence <workspace>/slices/evidence-assessor.md
```

Lint each deliverable against its own slice — the one automated check that
the isolation held. Ceilings are strictest for the Evidence Assessor and the
Cost & Capacity Analyst, the two roles where confident fiction does the most
damage. Ceiling and untagged-claim failures go back to the role agent to
redo, ceiling stated; do not patch them yourself — you have seen the other
roles' work, and your edits reintroduce exactly the contamination the
isolation prevents. A high `[UNKNOWN]` share is a note for the limitations
section, not a redo.

### 7. Map disagreement, build the ledger

Extract every claim that bears on the same assumption across roles and find
polarity conflicts — real disagreements, arising from different evidence. If
the roles agree on everything, treat it as a warning (shared prior, or slices
too similar) and aim the red team at the consensus.

Every assumption goes into the ledger with load-bearing status, importance,
uncertainty, and the cheapest trial that would resolve it:

```bash
python scripts/rank_assumptions.py <workspace>/assumptions.md
```

The flags it raises are the whole point: a load-bearing assumption with high
priority and no cheap trial attached — "she can operate at this scale", "he
wants to build, not just advise", "this role will still make sense after the
re-org" — is the thing that becomes a regretted hire six months from now.

### 8. Draft the memo, then red-team it

The Talent Lead writes a fully-tagged `synthesis.md` (linted at the 0.20
ceiling; carries claims forward, never introduces them) and renders the memo
from it per `references/memo-format.md` — including per-candidate verdicts
when finalists are being compared, and the evidence-quality footer, which
states how much of the analysis rests on demonstrated work versus claims.

Then run the red team per `references/redteam-protocol.md`: three independent
refuters, clean contexts, given the memo and raw evidence but never the role
deliverables. Their lenses are fixed:

- **Resemblance** — is this recommendation "reminds us of the last good
  hire" wearing the costume of fit? Would this candidate survive if the
  criterion were *can do something the last good hire could not*?
- **False negative** — reconstruct who the process never saw. Was the
  shortlist created by proxy knockouts, keyword legibility, or a
  funnel-only sourcing decision? Name who is missing, not just what.
- **Wrong problem** — attack the role itself. Is this a process gap, a
  scope problem, or a retention problem wearing a hiring costume? Would the
  role survive contact with the org as it actually is?

A refutation counts only if it names something observable within about 30
days (a trial result, a reference answer, a measurement of the gap). Vague
pessimism is discarded. Two or more surviving refutations on the same
load-bearing assumption cap the verdict below "hire".

### 9. Set the verdict honestly

The verdict is one of **hire / reshape / trial / keep-looking**, per
candidate where finalists are compared, and it is constrained rather than
chosen:

- Any load-bearing assumption at priority ≥ 16 with no completed trial → the
  verdict is **trial**, not hire. There is no exception for a strong
  interview.
- Zero `demonstrated` evidence for a candidate → that candidate's verdict
  cannot be hire; the best available is **trial**, and the trial is the one
  that produces the missing evidence.
- Two or more surviving refutations on one load-bearing assumption →
  **trial** or **keep-looking**.
- Shortlist 100% funnel-sourced with proxies used as knockouts →
  **keep-looking** runs alongside any per-candidate verdict: the finding
  plan executes before an offer, because the comparison set was never valid.
- Gate passed only marginally → **trial**, and say so.

"A: trial. B: keep-looking." is a real answer. So is "close the req and fix
the process instead." The pull toward hiring the agreeable finalist who is
*present* is strong and does not announce itself; binding the verdict to the
ledger is what resists it.

### 10. Write the trial cards — and schedule the audit

For each top assumption, a trial card per `references/memo-format.md`: the
trial (a paid work sample with a real problem; a structured reference
protocol with the exact questions; a two-hour build-together session; a
30-60-90 with observable checkpoints), the cost, and — written before the
trial runs, timestamped — pass, fail, and the reshape band between. Deliver
the trial cards even if the user only asked "so should we hire her?"

One standing card is always included: **the rejected-pile audit.** Once a
quarter, a human reads a sample of what the process rejected, looking for the
non-standard excellent. It is the only measurement the false negative will
ever get, and its results feed `05-history.md` for the next run.

## Output

Deliver, in this order of prominence:

1. **The trial list** — three to five cards, cheapest first, thresholds
   pre-committed.
2. **The decision memo** — one page, per-candidate verdicts, evidence-quality
   footer intact (demonstrated vs. claimed share stated). Never remove the
   footer to make the memo read better.
3. **The assumption ledger** — sorted, untested load-bearing items flagged.
4. **Open disagreements and surviving refutations** — unresolved, as they
   are. Writing smoothly over a real disagreement about a person is how
   regretted hires get made politely.

## Reference files

- `references/evidence-protocol.md` — the hiring evidence hierarchy, tagging,
  the gate, lint thresholds. Read before step 3.
- `references/gates-and-finding.md` — legitimate gates vs. proxies; the
  finding-over-filtering sourcing playbook. Read before step 2.
- `references/roles.md` — the six role briefs, slicing map, output contracts.
  Read before step 5.
- `references/redteam-protocol.md` — the three lenses, survivability rules,
  kill conditions. Read before step 8.
- `references/memo-format.md` — memo template, ledger schema, trial cards,
  candidate-communication notes. Read before step 8.
- `assets/examples/worked-example.md` — an end-to-end run, including one that
  correctly fails the gate and produces a work trial instead of an offer.

## Scope

Decision support, not a decision, and not legal advice. Employment law varies
by jurisdiction (notice, discrimination, automated-decision rules); anything
with legal exposure goes to counsel. The analysis informs a named human
decision-maker; it never replaces one.
