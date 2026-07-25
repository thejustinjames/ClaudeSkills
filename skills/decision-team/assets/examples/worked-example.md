# Worked examples

Two short runs. The first fails the evidence gate, which is the more common and
more important outcome. The second passes marginally and shows how the ledger
constrains the verdict.

---

## Example A — the gate fails

**The ask:** "Should we launch a self-serve tier? I think there's a big market
of smaller customers we're missing."

**Workspace after the interview:**

`02-decision.md` — Decide whether to build and launch a self-serve tier at
£49/month by 2026-09-30. Alternative considered: keep sales-led only. Desired
outcome: 50 self-serve accounts and £2.5k incremental MRR by year end.

`03-evidence.md` — four items:

- E1 `internal-data` — 62 paying accounts, ARPU £297, 14-month median age
- E2 `internal-data` — 340 trial signups in H1, 11 converted
- E3 `anecdote` — two inbound emails asking "do you have a cheaper plan"
- E4 `secondary` — a blog post about PLG conversion benchmarks

**Gate result: FAIL.** Two independent primary/internal-data sources against a
floor of five, and the decision turns entirely on whether small customers exist
and will pay — with zero conversations with any of them. The two inbound emails
are `anecdote`, not demand: nobody was asked for money.

Running six roles here would have produced a market sizing, a buyer persona, a
three-scenario financial model, and a confident recommendation. Every number in
it would have originated in the model rather than the world, and the memo would
have read exactly like one built on real evidence. That is the failure mode this
gate exists to prevent.

**What was delivered instead:**

```markdown
## Evidence Acquisition Plan — self-serve tier

The gate failed: 2 primary/internal-data items (need 5), and zero conversations
with anyone in the segment the decision is about. A memo built on this would be
inference dressed as analysis.

### 1. Talk to the 329 trials that did not convert
- **Why it matters:** settles whether price was the blocker or the product was.
  If it was the product, a cheaper tier makes the problem cheaper, not smaller.
- **How:** email all 329, offer £50 for 20 minutes, aim for 8 conversations.
- **Cost:** £400 and about 5 hours.
- **What each result means:** if ≥5 of 8 name price, the tier is worth designing.
  If ≥5 name a missing capability, build that instead. Mixed → segment further.

### 2. Put a £49 plan on the pricing page with a waitlist button
- **Why it matters:** measures revealed interest rather than stated interest,
  which is the gap E3 cannot speak to.
- **How:** one afternoon of work, run for two weeks against existing traffic.
- **Cost:** half a day.
- **What each result means:** ≥30 waitlist signups → real pull. <10 → the
  segment is not arriving at your site, and a tier will not change that.

### 3. Check what the 11 conversions have in common
- **Why it matters:** if trial conversion is already concentrated in one profile,
  a self-serve tier may cannibalise rather than expand.
- **How:** read the 11 accounts against the 329. Half a day with E2.
- **Cost:** half a day.

**Come back when:** you have 8 conversations with non-converted trials and two
weeks of waitlist data. That is about a week of work and it will change the
decision either way.
```

The user asked for a strategy memo and left with three things to do. That is the
better trade, and it is worth saying so plainly rather than apologising for it.

---

## Example B — marginal pass, verdict constrained

**The ask:** "Should we raise the price from £380 to £500?"

Evidence: 3 primary, 2 internal-data, 1 secondary, 1 anecdote — 5 strong items
from 5 independent sources. Gate = marginal pass (the 5–8 band), so the verdict
is capped at `test` before the analysis even runs.

Worth noting what the gate is doing here. An earlier version of this run split
one interview round into four well-scoped evidence blocks — correct hygiene,
since it makes each claim citable — and the block count alone would have carried
a near-failure to a comfortable pass. Counting independent sources instead is
what keeps good citation hygiene from manufacturing confidence.

**Five roles ran in isolation.** Two disagreements emerged mechanically, not by
instruction:

| Disagreement | Roles | What would settle it |
|---|---|---|
| Is the segment price-sensitive? | Market Analyst said yes from cost-led switching in interviews; Finance Lead noted the one won deal closed at £380 after asking £500 — a data point about discounting, not sensitivity | Quote £500 to the next 10 qualified buyers without pre-discounting |
| Will existing accounts absorb the increase? | Customer Strategist found no evidence either way; Operator flagged that 41% of support tickets concern the import step, which weakens the value story at a higher price | Offer the new price to the next 20 renewals |

**Lint:** Finance Lead failed on the first pass at 0.38 against a 0.25 ceiling —
it had generated a projected MRR figure with no input evidence. Redone with
break-evens instead of projections, it passed at 0.19 and the output became
useful: *"this needs 47 accounts at £500 to clear the same revenue; you have 62
at £380, so it survives losing up to 15 accounts."* That sentence is checkable
and it reframed the whole decision as a churn question.

**Ledger:** A1 (existing accounts absorb the increase) and A4 (churn stays under
4%) both came out load-bearing at priority 20 and untested. `rank_assumptions.py`
exited 1.

**Red team:** two of three refuters landed surviving refutations on A1.

> **R2 — attacks A1.** Accounts do not churn immediately; they churn at renewal,
> which for the median 14-month account is months away. Early data will look
> fine and the loss will arrive after the decision is treated as settled.
> **Leading indicator (30 days):** of the first 8 renewals offered the new price,
> 2 or more ask for a call before renewing — historically a churn precursor.

**Verdict: TEST**, forced twice over — once by the ledger, once by the kill
condition. The recommendation was not "raise the price"; it was "offer £500 to
the next 20 renewals and the next 10 new buyers, and watch renewal-call requests
as the leading indicator."

**Footer:**

```
Evidence quality: 3 primary · 2 internal-data · 1 secondary · 1 anecdote
Oldest item: 2026-03 (4 months)
Assumption ratio across role deliverables: 0.27
Roles that failed lint on first pass: Finance Lead (0.38 vs 0.25)
Isolation: held — 5 parallel subagents, disjoint slices
Gate: marginal pass — 5 primary/internal items, 2 of 3 interviews from one segment
```

The footer is what lets the reader weigh this against a memo built on twelve
primary items. The prose in both would read the same.
