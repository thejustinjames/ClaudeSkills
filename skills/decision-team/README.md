# Decision Team

> **📦 You are looking inside a Claude skill.** This folder is the unpacked contents of
> [`decision-team.skill`](../../decision-team.skill) — a `.skill` file is just a zip of a folder
> like this one. [`SKILL.md`](SKILL.md) is the canonical playbook Claude loads;
> [`references/`](references/) holds step-specific depth, [`assets/`](assets/) holds templates and
> a worked example, and [`scripts/`](scripts/) holds the deterministic checks. (This README is
> added for browsing on GitHub and is not part of the package.)

A harness for making a consequential decision well. Six analytical roles run in
isolation, every claim is traced to evidence or flagged as an assumption, an
independent red team tries to kill the recommendation, and the primary output is
a list of cheap falsifiable tests — not a persuasive memo.

## Why this is built the way it is

The obvious way to do multi-role analysis is to ask one model to play six
characters in one conversation. That produces six voices, not six perspectives.
Same weights, same priors, same context window: the errors are correlated, and
the synthesis step cannot detect correlated error because it looks exactly like
agreement. Worse, agreement between roles that share a prior *feels* like
converging evidence, which is precisely the failure mode a decision process is
supposed to prevent.

Three structural properties fix most of that, and this skill is organised around
them:

1. **Isolation.** Roles run as separate agents with disjoint evidence slices and
   no sight of each other's reasoning. Independence has to be manufactured
   structurally because it will not arise from prompting.
2. **Traceability.** Every claim carries a tag: which evidence item supports it,
   or an explicit admission that nothing does. Fluent unsupported prose is the
   default output of a language model; the tagging plus the lint script make it
   expensive.
3. **Refutation, not review.** The red team runs afterward, in a clean context,
   sees the conclusion and the raw evidence but never the reasoning trace, and is
   asked to break the decision rather than assess it.

The value of this process is not the memo. It is the short list of things that,
if you spent a week finding out, would actually change what you do. Optimise for
that.

## Before anything else: the evidence gate

Analysis cannot manufacture evidence. If the inputs are thin, running six roles
produces a beautifully formatted hallucination with a financial model attached —
which is more dangerous than no analysis, because it feels like diligence.

So the first action after the workspace exists is to check whether there is
enough to work with. Read [`references/evidence-protocol.md`](references/evidence-protocol.md)
for the full rules, but the shape is:

- Count the evidence items that are **primary** (you or the user talked to a
  real buyer, ran the test, shipped the thing) or **internal-data** (your own
  numbers, exported not remembered).
- If fewer than five, or if the decision turns on demand and there are zero
  buyer conversations, **stop**. Do not produce a decision memo.
- Produce an **Evidence Acquisition Plan** instead: the three cheapest things to
  find out this week, what each would settle, and what you would do differently
  depending on the result. Say plainly that a memo now would be fiction.

This gate is the most valuable part of the skill, and the part most likely to be
skipped under pressure to produce something. Do not skip it. A user who came for
a strategy memo and left with three phone calls to make got the better deal.

## Workflow

Run these in order. Steps 4–6 are the parts that need real care.

### 1. Build the workspace and state the decision

```bash
python scripts/init_workspace.py <decision-slug>
```

This creates the context files, the assumption ledger, `slices.md`, and the
output folders. Fill only two things now — `02-decision.md` and
`03-evidence.md` — because the gate may end the run, and interviewing someone
about team capacity for an analysis that is not going to happen wastes the
goodwill you need for the parts that matter. `01-context.md`,
`04-constraints.md`, and `05-history.md` get filled at step 3, after the gate
passes.

Interview the user for the decision statement; do not fill it from inference. A
vague statement poisons everything downstream, because each role will silently
resolve the ambiguity in a different direction. It needs: the specific move, the
alternative it is being weighed against, the date, the desired outcome in
observable terms, the resources actually available, and what would count as
success at six months. Mark anything the user cannot supply `[NOT SUPPLIED]`
rather than filling it in — those gaps are the first finding.

Watch for a decision stated as a yes/no on the one option the user is attached
to. "Should we build X?" usually has three or four unstated alternatives, and
naming them is often worth more than the analysis that follows.

### 2. Load evidence and run the gate

Populate `03-evidence.md` in the required format (see
[`references/evidence-protocol.md`](references/evidence-protocol.md)): one block
per item, each with an `E<n>` id, a source, and a type. Evidence comes from the
user, from files, or from tools with retrievable citations. Never write an
evidence item from your own priors — if you researched it with web search, it is
secondary and carries a URL.

```bash
python scripts/evidence_lint.py --gate --evidence <workspace>/03-evidence.md \
    [--hinges-on-demand]
```

The gate counts independent sources, not blocks, so splitting one interview into
four well-scoped items does not inflate it. Pass `--hinges-on-demand` when the
decision turns on whether anyone wants the thing. The script prints the
conditions it cannot check — apply those yourself, particularly the buyer/user
split: in a B2B2C decision, interviews with the people who pay say nothing about
demand from the people who would use it.

If the gate fails, produce the Evidence Acquisition Plan and stop. Do not spawn
a role.

### 3. Fill the rest of the context, then slice

Now interview for `01-context.md`, `04-constraints.md`, and `05-history.md`.

Assign each evidence item to the roles that should see it and record the mapping
in `slices.md`. Write each slice out as a standalone file under `slices/`
containing the full text of its items — a role should never be handed the whole
evidence file with instructions to ignore parts of it.

[`references/roles.md`](references/roles.md) gives the default mapping and the
rule for when the evidence is too thin to slice five ways. Slicing is what buys
independence, and it costs something: a role may miss what it needed. That is
handled in step 4 rather than by giving everyone everything.

### 4. Run the roles in isolation

Spawn each of the five analytical roles as its own agent, in parallel, each
receiving only: `02-decision.md`, `04-constraints.md`, its evidence slice, its
role brief, and the output contract. Not the other roles' outputs. Not this
conversation.

Role briefs are in [`references/roles.md`](references/roles.md). The five are
Market Analyst, Customer Strategist, Operator, Finance Lead, and Historian. (Red
team and synthesis run later and separately — that ordering is the point.)

Every role deliverable ends with a section titled "Evidence I was not given but
need", listing what it would have wanted. Collect those. They are often the most
useful output of the whole step, because they map the information gaps without
anyone having to guess at them.

If subagents are unavailable, run each role in a separate session and paste in
only its slice. Running them as turns in one conversation defeats the design —
if that is the only option, say so in the memo's limitations section rather than
pretending the isolation held.

### 5. Lint the deliverables

Lint each deliverable against its own slice, not the full evidence file:

```bash
python scripts/evidence_lint.py <workspace>/roles/operator.md \
    --evidence <workspace>/slices/operator.md
```

Pointing `--evidence` at the slice is what makes this the one automated check on
whether the isolation held. A role that cites an item it was never given did not
get that id from its slice, and against the full file that goes unnoticed.

The script checks that every claim line carries a tag, that cited ids exist in
the slice, and that the ratio of unsupported claims stays under the role's
ceiling (strictest for Finance Lead and Market Analyst, the roles where
confident fiction does the most damage).

Send ceiling failures and untagged-claim failures back to the role agent to
redo, with the ceiling stated. Do not patch them yourself — you have seen the
other roles' work, so your edits reintroduce exactly the contamination the
isolation was there to prevent.

Two script outputs are notes, not failures: a high `[UNKNOWN]` share means the
slice was too thin for that role, and that belongs in the memo's limitations
rather than in a redo. Re-running an agent to reword an honest gap costs a round
trip and changes no finding.

### 6. Map disagreement mechanically

Do not ask the roles to disagree. Manufactured disagreement is theatre; it reads
as rigour and contains no information. Instead, extract every claim that bears
on the same assumption and find where their polarity conflicts. Those are real
disagreements — they arose from different evidence.

For each one, record: the assumption at stake, what evidence would settle it,
and the cheapest test that would produce that evidence.

If the roles agree on everything, that is a warning, not a green light. It most
likely means they shared a prior or the evidence slices were too similar. Note
it explicitly, and instruct the red team to attack the consensus directly.

### 7. Build the assumption ledger

Every assumption surfaced by any role goes in the ledger with: whether it is
load-bearing (does the decision flip if it is false?), importance 1–5,
uncertainty 1–5, and the cheapest test that would resolve it.

```bash
python scripts/rank_assumptions.py <workspace>/assumptions.md
```

This sorts by importance × uncertainty and flags load-bearing assumptions that
have no test attached. Those flags are the whole point: a load-bearing
assumption with high priority and no cheap test is the thing that will kill the
decision six months from now.

### 8. Draft the memo, then red-team it

The Strategy Lead writes two files. `synthesis.md` is fully tagged and gets
linted at the 0.20 ceiling — this is where the "introduce no new claims" rule is
enforced. The memo is then rendered from it in readable prose and is not linted;
a one-page memo with a citation tag on every line is unreadable, and an
unreadable memo does not get read. Format in
[`references/memo-format.md`](references/memo-format.md).

Then run the red team per
[`references/redteam-protocol.md`](references/redteam-protocol.md): three
independent refuters, distinct lenses, each given the memo and the raw evidence
file but not the role deliverables or any reasoning trace, each asked to break
the decision rather than review it.

A refutation only counts if it names a leading indicator you could observe
within about 30 days. Vague pessimism is discarded — it is unfalsifiable and
therefore free to produce.

If two or more refuters land a surviving refutation on the same load-bearing
assumption, the recommendation cannot be "proceed". It becomes "test", and the
test is the one that resolves that assumption.

### 9. Set the verdict honestly

The verdict is one of **proceed / modify / test / stop**, and it is constrained
rather than chosen freely:

- Any load-bearing assumption with priority ≥ 16 and no completed test → the
  verdict is **test**, not proceed. There is no exception for a strong
  narrative.
- Two or more surviving red-team refutations on one load-bearing assumption →
  **test** or **stop**.
- Evidence gate passed only marginally → **test**, and say so.

For an either/or allocation — build A or build B with the same quarter — apply
the rule to each option separately and state both verdicts. "A: test. B:
proceed." is a real answer; collapsing it into a single token is not. Where the
framing itself is the problem (both options fail, or the two are not actually
exclusive), say that first and give the per-option verdicts underneath.

This rule exists because the pull toward an agreeable, confident "proceed" is
strong and does not announce itself. Binding the verdict to the ledger is what
keeps the analysis honest when the user clearly wants to hear yes.

### 10. Write the test cards

For each of the top assumptions, a test card: the test, the metric, the sample
or duration, the cost, and — written before the test runs and timestamped — the
pass threshold, the fail threshold, and the band in between that means modify.
Format in [`references/memo-format.md`](references/memo-format.md).

Pre-committing thresholds is the single highest-value habit in this whole
process, because it is the only defence against reinterpreting a bad result as
encouraging. Deliver the test cards even if the user only asked for the memo.

## Output

Deliver, in this order of prominence:

1. **The test list** — three to five cards, cheapest first, with thresholds set.
2. **The decision memo** — one page, per
   [`references/memo-format.md`](references/memo-format.md), with the
   evidence-quality footer intact. The footer reports how many primary and
   internal-data items backed the analysis and what fraction of claims were
   assumptions. Never remove it to make the memo read better; it is the reader's
   only way to calibrate what they are holding.
3. **The assumption ledger** — sorted, with untested load-bearing items flagged.
4. **Open disagreements and surviving refutations** — unresolved, as they are.
   Resolving a real disagreement by picking a side and writing smoothly over it
   is the most expensive thing this process can do.

## Reference files

| File | What it covers | Read before |
|------|----------------|-------------|
| [`references/evidence-protocol.md`](references/evidence-protocol.md) | Evidence format, types, tagging, the gate, lint thresholds | Step 2 |
| [`references/roles.md`](references/roles.md) | The six role briefs, evidence slices, output contracts | Step 4 |
| [`references/redteam-protocol.md`](references/redteam-protocol.md) | Refuter lenses, survivability rules, kill conditions | Step 8 |
| [`references/memo-format.md`](references/memo-format.md) | Memo template, assumption ledger schema, test card format | Step 8 |
| [`assets/examples/worked-example.md`](assets/examples/worked-example.md) | A short end-to-end example, including one that correctly fails the evidence gate | — |

## Scope

This produces decision support, not a decision, and not professional advice. For
choices with legal, tax, regulatory, or clinical exposure, the output is a
structured brief to take to someone qualified — say that in the memo rather than
implying the analysis stands alone.
