# Red Team Protocol

The red team runs last, in a clean context, and is asked to break the decision
rather than assess it.

## Why it is separated

A critic that runs inside the same context as the analysis it is criticising has
the entire reasoning trace in front of it, including every justification already
constructed. It will find the weaknesses that the trace already acknowledged and
miss the ones the trace was built to avoid. This is not a prompting problem —
"be harsh" does not fix it — because the material that would need to be
questioned is exactly the material that has already been accepted as premise.

So the red team gets a deliberately impoverished input: what was concluded, and
what was actually observed. Nothing about how the conclusion was reached.

## Inputs

Each refuter receives:

- The draft decision memo
- `03-evidence.md` in full — raw evidence, not any role's reading of it
- The assumption ledger
- Its lens (below)

It does **not** receive: role deliverables, the disagreement map, the
orchestrating conversation, or any indication of what the user hopes to hear.

Run three refuters in parallel, in separate contexts. In series they contaminate
each other; the second refuter that sees the first one's work will elaborate it
rather than open a new line of attack.

## The three lenses

Distinct lenses rather than three copies of "find problems". Identical refuters
sample the same failure mode three times, which produces the illusion of
convergence. Different lenses cover different parts of the space.

### Lens A — Demand

*"Nobody wants this badly enough to change what they do."*

Attack the buyer side. The alternative to consider hardest is inertia: doing
nothing is free, familiar, and has no procurement cycle. Look for stated
preference being read as behaviour, enthusiasm from people who do not control
budget, and interest that never survived a request for commitment.

### Lens B — Execution

*"This team cannot deliver it in this window at this quality."*

Attack the delivery side. Look for the bottleneck the plan does not name,
dependencies on one person or one integration, work that quietly stops for this
to happen, and elapsed-time estimates with no basis in the team's actual
history. Check whether the timeline assumes nothing else goes wrong.

### Lens C — Economics

*"The numbers do not survive contact with reality."*

Attack the model. Look for inputs that are assumptions wearing decimal points,
missing costs (support, onboarding, sales time, the cost of the thing failing),
a cash trough the endpoint hides, sensitivity to one input that has no evidence
behind it, and break-evens that require a step change in a metric that has been
flat.

Add a fourth lens when the decision has a specific exposure — regulatory,
security, key-person, single-customer concentration, platform dependency. Name
it explicitly rather than hoping one of the three covers it.

## Survivability

The output of a refuter is a set of refutations. Most pessimism is free to
produce and therefore worthless, so a refutation only counts if it is
falsifiable on a short horizon.

A refutation **survives** only if it names:

1. **The load-bearing assumption it attacks** — by ledger id
2. **A concrete failure scenario** — specific enough that someone could
   recognise it happening
3. **A leading indicator observable within ~30 days** — the thing you would see
   first if this refutation were correct

Required shape:

```markdown
### R1 — attacks A3 (buyers will pay £500/month)
**Failure scenario:** Buyers agree to the price in conversation, then stall at
procurement because there is no line item for this category, and the deal dies
in month four with no explicit no.
**Leading indicator (30 days):** Of the first 10 qualified conversations, fewer
than 3 will name an existing budget line the spend would come from.
**Evidence basis:** [E1] the one buyer asked directly declined to commit to a
pilot; [E4] no interviewee named a current vendor in this category.
```

A refutation without a leading indicator is discarded. Not softened — discarded.
Keeping unfalsifiable objections in the memo makes the analysis look thorough
and gives the reader nothing to act on, which is the exact trade this process
exists to refuse.

## Kill conditions

Apply mechanically after collecting the surviving refutations:

| Condition | Effect on verdict |
|---|---|
| ≥2 refuters land surviving refutations on the **same** load-bearing assumption | Cannot be `proceed`. Becomes `test`, and the test is the one that resolves that assumption. |
| A surviving refutation attacks an assumption with no test in the ledger | That test gets written and goes to the top of the list. |
| All three refuters fail to land anything survivable | Note it, and treat it as weak positive evidence only. It is at least as likely that the memo was too vague to attack — check whether the memo makes any falsifiable claim at all. |
| A refutation's leading indicator is already observable in existing evidence | Halt the run and re-synthesise. This is not a risk to test, it is a finding the analysis missed, and the memo is currently recommending something against evidence already in the file. The verdict after re-synthesis is usually `stop` or `modify`, but reach it by redoing the synthesis rather than by overriding the token. |

That last row is worth watching for. It happens more than expected: a refuter
predicts a signal that, checked against `03-evidence.md`, is already sitting
there in an interview note nobody weighted.

## Handling the results

Surviving refutations go into the memo **unresolved**. Do not write a rebuttal
paragraph after each one. A refutation answered in the same document by the
author of the thing being refuted is not answered, it is absorbed, and the
reader loses the ability to weigh it independently.

The correct response to a surviving refutation is a test, or an explicit
acceptance: "we are proceeding despite R2 because <reason>, and we will know we
were wrong if <leading indicator>." Written that way it stays visible, and in
six weeks someone can check it.
