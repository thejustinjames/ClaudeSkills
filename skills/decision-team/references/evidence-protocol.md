# Evidence Protocol

Everything downstream is bottlenecked here. A role deliverable is only as good
as the slice it was handed, and a memo is only as good as the weakest link in
the chain of claims that produced it. This file defines the format, the types,
the tagging scheme that makes claims checkable, and the gate that decides
whether analysis should happen at all.

## Contents

- [Evidence file format](#evidence-file-format)
- [Evidence types](#evidence-types)
- [The evidence gate](#the-evidence-gate)
- [Claim tagging](#claim-tagging)
- [Lint thresholds](#lint-thresholds)
- [Evidence hygiene](#evidence-hygiene)

## Evidence file format

`03-evidence.md` holds one block per item. The lint script parses these ids, so
the header line format matters:

```markdown
## E1 | type: primary | source: Interview — CTO, Acme Corp | date: 2026-06-12
Currently spends about £4k/month on the incumbent. Said he would switch for a
30% saving but would need SOC 2. Did not commit to a pilot when asked directly.

## E2 | type: internal-data | source: Stripe export, Q1 2026 | date: 2026-04-02
MRR £18,400 across 62 accounts. Trailing-3-month churn 3.1%/month. Top account
is 11% of MRR.

## E3 | type: secondary | source: https://example.com/2026-market-report | date: 2026-03
Vendor-published estimate of segment size at £240m, growing 12% YoY. Methodology
not disclosed.
```

Rules that matter:

- Ids are `E<n>`, sequential, never reused. If an item is retracted, keep the id
  and mark the body `RETRACTED — <why>`. Silent renumbering breaks every
  citation written before it.
- The date is the date the evidence was *generated*, not the date you wrote it
  down. Stale evidence is a different problem from thin evidence, and only the
  generation date reveals it. Write `date: unknown` when you genuinely do not
  know — the gate counts undated items and reports them rather than quietly
  treating the file as fresh.
- **Blocks must be self-contained.** Never write "same interview round as E1" or
  "one of the respondents in E3". Slices are built by selecting blocks, so a
  cross-reference leaks the existence and partial content of an item the role
  was deliberately not given. Repeat the context instead; the duplication costs
  nothing and the leak costs the isolation.
- The `source:` field is what the gate uses to count independent sources, so
  make it identify the *source*, not the item: two blocks from the same
  interview should carry the same source string.
- Record what was actually said or measured, including the parts that cut
  against the decision. The CTO not committing to a pilot in E1 is the most
  informative sentence in that block.

## Evidence types

The type determines how much weight a role may put on an item, and the gate
counts by type.

| Type | Means | Weight |
|---|---|---|
| `primary` | You directly observed it: interview you ran, test you shipped, customer who paid or refused | Highest. Only type that settles demand questions. |
| `internal-data` | Your own systems, exported: billing, analytics, support tickets, git history, incident log | High for questions about you. Says nothing about the market. |
| `secondary` | Published research, competitor materials, analyst reports, news, anything retrieved | Low. Useful for sizing and context; never sufficient for a demand claim. |
| `anecdote` | Something someone told you second-hand, a conference conversation, a tweet | Very low. Fine as a hypothesis generator, never as support. |
| `expert` | A qualified person's judgement, attributed | Moderate, and only within their actual domain. |

There is deliberately no type for a figure the model produced. A number that
came out of a language model is not evidence, it is an assumption with false
precision, and it must be tagged `[ASSUMPTION]` wherever it appears.

### Typing calls that are easy to get wrong

These come up constantly and the choice moves the gate, so decide them by rule
rather than by feel:

- **A friend or colleague enthusing about the idea, unprompted and in person.**
  This is `anecdote`, not `primary`, however direct it was. The rule:
  *no commitment was requested, so it is anecdote.* Primary evidence about
  demand requires an ask — a price quoted, a pilot proposed, a deposit
  requested — and a recorded answer. Enthusiasm from someone who likes you and
  was never asked for money is the single most over-weighted input in this
  entire process.
- **Something you remember reading but cannot locate.** Not evidence at all.
  Put it in `01-context.md` as background, where it informs questions without
  supporting claims. If it matters, spend ten minutes finding it and it becomes
  `secondary` with a URL.
- **A number the user recalls without checking.** `anecdote` until exported. The
  gap between remembered and actual churn is routinely the size of the decision.
- **An interview where the buyer and the user are different people.** Type it by
  who was actually in the room, and note which side it speaks for. This matters
  at the gate — see below.

## The evidence gate

Run before any role is spawned:

```bash
python scripts/evidence_lint.py --gate --evidence 03-evidence.md [--hinges-on-demand]
```

The script counts **independent sources**, not blocks. "One claim per item" is
correct hygiene for citation, but it means a single interview round can become
four blocks — and a gate that counted blocks would let good hygiene manufacture
a pass. The `source:` field is what makes the two compatible.

**Hard stops** — produce an Evidence Acquisition Plan, not a memo:

- Fewer than 5 independent `primary` or `internal-data` sources. *(checked)*
- Zero `primary` items on a decision that turns on demand. *(checked with
  `--hinges-on-demand`)*
- The decision turns on unit economics and there is no `internal-data` on
  current cost or price. *(your call)*
- Every item older than the last time this market visibly moved. *(your call —
  and the script tells you how many items are undated, which is its own
  problem)*

**The buyer/user split.** In any B2B2C decision — you sell to clinics, patients
use it; you sell to schools, students use it — the demand stop applies to each
side separately. Seven interviews with the people who pay is zero evidence about
whether the people who would use it want it. The script cannot detect this
because it cannot know who the users are, so it prints the reminder and leaves
the call to you. It is the most common way a decision with a comfortable-looking
evidence count is actually unevidenced.

**Marginal pass** — proceed, but the verdict is capped at `test` and the memo
says why:

- 5–8 independent strong sources.
- Strong items outnumber their sources substantially — the count is thinner
  than it looks.
- Primary items all come from one segment, one channel, or one relationship.
- Any load-bearing question supported only by `secondary` and `anecdote`.

### The Evidence Acquisition Plan

When the gate fails, this replaces the memo. It is short and it is not a
consolation prize — for a genuinely under-evidenced decision it is worth more
than any analysis could be.

```markdown
## Evidence Acquisition Plan — <decision>

The gate failed: <which condition, with counts>. A decision memo built on this
would be inference dressed as analysis. Here is what to find out first.

### 1. <What to find out>
- **Why it matters:** which assumption it settles, and what flips if it is false
- **How:** the specific action — "call these 5 named people", not "do research"
- **Cost:** time and money
- **What each result would mean:** if X, then <do this>. If Y, then <do that>.

### 2. ...
### 3. ...

**Come back when:** <the specific condition that clears the gate>
```

Three items, cheapest first. If two of them can be done in an afternoon, say so
— the main reason people skip evidence gathering is that they imagine it takes
a quarter.

## Claim tagging

Every claim line in every role deliverable opens with a tag. This is what makes
the lint mechanical, and mechanical checking is the only kind that survives
contact with a fluent generator.

| Tag | Means |
|---|---|
| `[E3]` or `[E3,E7]` | Directly stated in those evidence items |
| `[INF: E3,E7]` | Inference that goes beyond what those items state |
| `[ASSUMPTION]` | Not grounded in any evidence given |
| `[UNKNOWN]` | A gap being flagged rather than a claim being made |

Example of a well-tagged fragment:

```markdown
### Demand signal
[E1,E4] Two of five interviewed buyers named cost as the trigger for switching.
[E1] One named SOC 2 as a hard requirement and did not commit to a pilot.
[INF: E1,E4] Cost-driven switching suggests price sensitivity, so a premium
position is unlikely to work in this segment.
[ASSUMPTION] The other three buyers, who did not name a trigger, are also
cost-driven.
[UNKNOWN] Nothing in the slice indicates how long their procurement takes.
```

The discipline this enforces is visible in that last `[ASSUMPTION]` line. Untagged,
it would have been written as "the segment is cost-driven" and read as a finding.

Notes:

- Tag the claim, not the sentence. If one bullet makes two claims with different
  support, split it.
- `[INF: ...]` is not a way to launder an assumption. If the inference needs a
  premise that is not in the cited items, that premise is its own
  `[ASSUMPTION]` line.
- Headings, blank lines, table rows, and code blocks are not claim lines and are
  not tagged.

## Lint thresholds

`scripts/evidence_lint.py` computes an assumption ratio —
`[ASSUMPTION] / (evidence + inference + given + assumption)` — and fails a
deliverable that exceeds its role's ceiling.

`[UNKNOWN]` is deliberately outside that numerator. Flagging a gap is the
behaviour this whole process wants; counting it as a defect would teach roles to
stay quiet about what they could not see, which is the opposite of useful. A
high `[UNKNOWN]` share is reported as a **note**: it means the slice was too
thin for that role, which belongs in the memo's limitations rather than in a
redo.

Lint each deliverable against the role's **slice file**, not the full evidence
file. A role citing an id it was never given is the only automated signal that
the isolation leaked, and it is invisible when validated against the full set.

| Role | Ceiling | Why |
|---|---|---|
| Market Analyst | 0.30 | Ungrounded market claims are the most confidently wrong output in the set |
| Finance Lead | 0.25 | Numbers carry unearned authority; a plausible model with invented inputs is worse than no model |
| Customer Strategist | 0.40 | |
| Operator | 0.40 | |
| Historian | 0.35 | Working from a record; little excuse for ungrounded claims |
| Strategy Lead | 0.20 | Synthesis must not introduce new unsupported claims — it may only carry forward what the roles surfaced |

The Strategy Lead ceiling applies to its tagged `synthesis.md`, not to the memo.
A one-page memo carrying a citation tag on every line is unreadable, and an
unreadable memo does not get read — so the discipline is enforced upstream, in
the file the memo is rendered from.

A failing deliverable goes back to its own role agent to redo with the ceiling
stated. Do not patch it yourself: you have seen the other roles' work, and your
edits would reintroduce the correlation the isolation exists to prevent.

If a role cannot get under its ceiling after one redo, that is a finding, not a
formatting problem. It means the slice was too thin to support the analysis, and
it belongs in the memo's limitations section by name.

## Evidence hygiene

- **Never write an evidence item from your own knowledge.** If you searched for
  it, it is `secondary` with a URL. If you cannot cite it, it is not evidence.
- **Record the disconfirming parts.** The value of an interview is concentrated
  in what the buyer declined to say yes to.
- **One claim per item.** An evidence block asserting five things cannot be
  cited precisely, so it will be cited loosely.
- **Retract, don't delete.** A retracted item that other claims cited is a
  finding about those claims.
- **Watch the age.** Print the oldest generation date in the memo footer. A
  decision resting on a market read from two years ago should look uncomfortable
  on the page.
