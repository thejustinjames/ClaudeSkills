# 🧰 Creating Skills & Adapting the Decision-Team Template

This guide covers two things:

1. **[Part 1 — How to create a Claude skill from scratch](#part-1--creating-a-claude-skill-from-scratch)** — anatomy, frontmatter, references, scripts, packaging, and testing.
2. **[Part 2 — How to adapt `decision-team` to other strategic decisions](#part-2--adapting-decision-team-to-other-strategic-decisions)** — the skill ships tuned for build-vs-buy, but the harness generalises to pricing, hiring, market entry, vendor selection, kill decisions, and more.

---

## Part 1 — Creating a Claude skill from scratch

A skill is a folder of instructions, reference material, templates, and helper
scripts that Claude loads on demand. Instead of re-explaining a process every
session, the skill captures it once and Claude follows it consistently.

### Anatomy of a skill

```
my-skill/
├── SKILL.md              # Required. Frontmatter + the core playbook.
├── references/           # Optional. Deep detail, loaded only when needed.
│   └── protocol.md
├── assets/               # Optional. Templates, examples, boilerplate.
│   ├── workspace/
│   └── examples/
└── scripts/              # Optional. Deterministic helpers Claude runs.
    └── check.py
```

Only `SKILL.md` is required. Everything else exists to keep `SKILL.md` short —
Claude reads the playbook up front and pulls in reference files only at the
step that needs them. This is called **progressive disclosure**, and it is the
single most important design principle: a skill that front-loads everything
burns context on material that may never be used.

### Step 1 — Write the frontmatter (this is what triggers the skill)

`SKILL.md` starts with YAML frontmatter:

```yaml
---
name: my-skill
description: >
  What the skill does, and — critically — WHEN to use it. Name the concrete
  situations, the kinds of requests, and the casual phrasings that should
  trigger it ("should we...", "help me think through...").
---
```

The `description` is the only thing Claude sees before deciding whether to load
the skill. Treat it as a trigger specification, not a summary:

- **Name the situations**, not just the capability. Compare `decision-team`'s
  description: it lists *build or buy, raise prices, enter a market, hire,
  pivot, kill a product, pick a vendor* — and the casual phrasings too
  (*"should we…", "I'm torn between…", "is this worth doing"*).
- **Include trigger words users actually say.** If people ask for a
  "pre-mortem" or a "go/no-go", put those words in.
- **State when *not* to trigger** if the boundary is fuzzy (e.g. "only when the
  stakes are real").

### Step 2 — Write the playbook body

The body of `SKILL.md` is instructions to Claude. What works:

- **Explain *why* the process is shaped the way it is.** `decision-team` opens
  with "Why this is built the way it is" — because a model that understands the
  rationale applies the rules correctly in situations the author didn't
  anticipate. Rules without rationale get pattern-matched and misapplied.
- **Put gates early.** If there's a condition under which the whole run should
  stop (thin evidence, missing prerequisites, wrong kind of problem), make
  checking it the first step, and be explicit that stopping is a *success*
  outcome, not a failure.
- **Number the workflow.** Sequential steps with clear entry/exit conditions
  beat prose descriptions. Point each step at the reference file it needs
  ("Read `references/roles.md` before step 4").
- **Name the failure modes.** The most valuable sentences in a skill are the
  ones that describe what going wrong looks like: *"Manufactured disagreement
  is theatre"*, *"Do not patch them yourself — your edits reintroduce exactly
  the contamination the isolation was there to prevent."*
- **Define the output contract.** Say exactly what gets delivered, in what
  order, and what must never be dropped (e.g. the evidence-quality footer).

### Step 3 — Move depth into `references/`

Anything Claude only needs at a specific step goes in a reference file:
protocols, format specifications, role briefs, threshold tables. Keep each
reference file self-contained with a table of contents, and tell the playbook
*when* to read it. Rule of thumb: if a section of `SKILL.md` is only relevant
to one step, it belongs in `references/`.

### Step 4 — Add `assets/` templates and worked examples

- **Templates** (`assets/workspace/`) give every run the same starting
  structure, which makes outputs comparable across runs and makes the scripts'
  parsing reliable.
- **A worked example** (`assets/examples/`) is worth more than a page of
  abstract instruction — include at least one example of the skill *correctly
  refusing to proceed* (e.g. failing the evidence gate), because refusal paths
  are the ones models skip under pressure.

### Step 5 — Script the checks a model will fudge

Scripts exist for the things a language model does unreliably: counting,
enforcing thresholds, validating formats, sorting by computed priority.
`decision-team` ships three, and each guards a known failure mode:

| Script | Guards against |
|--------|----------------|
| `init_workspace.py` | Inconsistent workspace structure between runs |
| `evidence_lint.py` | Fluent unsupported prose; citations of evidence a role was never given |
| `rank_assumptions.py` | Vibes-based prioritisation; load-bearing assumptions with no test |

Guidelines: standard library only, runnable from a fresh clone, clear pass/fail
output, and — crucially — the script should print *what it cannot check* so
Claude applies those conditions manually rather than assuming the script
covered everything.

### Step 6 — Package and install

```bash
cd skills && zip -r ../my-skill.skill my-skill
```

A `.skill` file is just a zip of the skill folder. To use it:

- **Claude Code:** place the folder under `.claude/skills/` in a project (or
  `~/.claude/skills/` for all projects). It's discovered automatically and can
  be invoked explicitly with `/my-skill`.
- **Claude apps:** upload the `.skill` file where custom skills are supported.

### Step 7 — Test the triggers, the happy path, and the refusal path

1. **Trigger test:** phrase requests the way a real user would — casually,
   without naming the skill — and check it activates. If not, the
   `description` needs more trigger phrases.
2. **Happy path:** run a realistic case end-to-end and check the output
   matches the contract.
3. **Refusal path:** feed it inputs that *should* stop the run (thin evidence,
   out-of-scope request) and verify it stops. This is the test that matters
   most and gets run least.

---

## Part 2 — Adapting `decision-team` to other strategic decisions

`decision-team` ships tuned for build-vs-buy, but nothing about the harness is
specific to that decision. The structure generalises to any consequential,
hard-to-reverse call made under uncertainty.

### What to keep (the invariant core)

These five properties are *why the skill works*. Every variant keeps them:

1. **The evidence gate** — analysis never runs on thin inputs; the skill
   produces an Evidence Acquisition Plan instead of a fictional memo.
2. **Isolated roles with sliced evidence** — independence is manufactured
   structurally, never prompted.
3. **Claim traceability** — every claim tagged to evidence or flagged as an
   assumption, enforced by the lint script.
4. **Refutation after synthesis** — a red team in a clean context tries to
   *break* the recommendation, and refutations must name a ~30-day observable.
5. **A verdict bound to the ledger** — proceed/modify/test/stop is constrained
   by untested load-bearing assumptions, not chosen by narrative strength.

If a variant drops any of these, it isn't an adaptation — it's a different
(and weaker) skill.

### What to swap (the variant surface)

| Component | Where it lives | What changes per variant |
|-----------|----------------|--------------------------|
| Trigger description | `SKILL.md` frontmatter | The decision types and phrasings that activate it |
| Role cast | `references/roles.md` | Which five perspectives analyse, and their briefs |
| Evidence types & gate | `references/evidence-protocol.md` | What counts as "primary", and the stop conditions |
| Evidence slicing map | `references/roles.md` | Which evidence each role sees |
| Red-team lenses | `references/redteam-protocol.md` | The three angles of attack |
| Workspace templates | `assets/workspace/` | The context the decision always needs captured |
| Verdict constraints | `SKILL.md` step 9 | Domain-specific conditions that force "test" or "stop" |

### The adaptation procedure

1. **Copy the folder** and rename it: `cp -r skills/decision-team skills/pricing-decision`.
2. **Rewrite the frontmatter** `name` and `description` for the new decision
   type — this is what makes the variant trigger on the right requests.
3. **Recast the roles.** Keep five analytical roles + Strategy Lead + red team.
   Replace briefs to cover the perspectives that matter for *this* decision.
   Keep the shared output contract ("Assumptions I am making" / "Evidence I was
   not given but need") verbatim — it's role-agnostic and load-bearing.
4. **Redefine "primary evidence" and the gate.** Each decision type has its own
   version of "you talked to a real buyer". Define it, and set the gate's stop
   condition around the evidence that decision *hinges* on.
5. **Re-aim the red team.** Pick the three refuter lenses that match how this
   kind of decision actually fails.
6. **Add domain verdict constraints.** Keep the generic ones (priority ≥ 16
   untested → test) and add the domain-specific forcing rules.
7. **Update the worked example** — including one that fails the gate.
8. **Repackage:** `cd skills && zip -r ../pricing-decision.skill pricing-decision`.

### Variant sketches

Starting points for five common strategic decisions. Each row assumes the
invariant core stays intact.

#### 💰 Pricing decision (raise, lower, restructure, add a tier)

- **Roles:** Pricing Analyst (elasticity, competitor pricing) · Customer
  Strategist (willingness-to-pay signals, churn risk by segment) · Finance Lead
  (revenue bridge, margin impact) · Operator (billing/migration mechanics,
  grandfathering) · Historian (past pricing changes and what actually happened).
- **Primary evidence:** willingness-to-pay conversations with paying customers;
  your own churn/expansion data by segment; results of past price changes.
- **Gate addition:** if the decision hinges on elasticity and there are zero
  customer conversations about price → stop.
- **Red-team lenses:** churn cascade (which accounts leave first), competitive
  response, silent-damage lens (customers who don't complain, just stop
  expanding).

#### 🧑‍💼 Key hire / org decision (hire an exec, build a team, reorg)

- **Roles:** Talent Analyst (market for the role, comp benchmarks) · Operator
  (what breaks without the hire; onboarding cost) · Finance Lead (fully-loaded
  cost vs. alternatives) · Culture/Team Strategist (team impact, reporting
  lines) · Historian (past hires at this level — outcomes, regret rate).
- **Primary evidence:** structured references you actually called; internal
  data on what the gap is costing now; outcomes of comparable past hires.
- **Gate addition:** if the case rests on "we're drowning" with no measurement
  of what the gap costs → stop and measure first.
- **Red-team lenses:** wrong-problem lens (is this a process gap wearing a
  hiring costume?), integration failure, opportunity cost of the comp budget.

#### 🌍 Market entry (new segment, geography, or product line)

- **Roles:** Market Analyst (size, growth, competitive density) · Customer
  Strategist (demand signals from the *new* segment, not the current one) ·
  Operator (localisation, support, compliance load) · Finance Lead (CAC
  assumptions, payback under entry pricing) · Historian (past expansion
  attempts).
- **Primary evidence:** conversations with buyers *in the target market* —
  current-market enthusiasm is explicitly non-evidence here.
- **Gate addition:** zero target-market buyer conversations → automatic stop,
  regardless of how strong the home-market data looks.
- **Red-team lenses:** incumbent response, regulatory/compliance surprise,
  focus dilution on the core business.

#### 🤝 Vendor / platform selection (pick a vendor, sign a contract, migrate)

- **Roles:** Technical Evaluator (fit, integration surface, exit cost) ·
  Operator (migration path, downtime risk, support burden) · Finance Lead
  (total cost of ownership vs. contract price) · Risk Analyst (lock-in, vendor
  viability, data egress) · Historian (past vendor relationships and
  migrations).
- **Primary evidence:** a real proof-of-concept on your own workload; reference
  calls with current customers of the vendor at your scale; your own usage data
  for sizing.
- **Gate addition:** no PoC and no reference calls → stop; a demo run by the
  vendor's sales engineer is secondary evidence at best.
- **Red-team lenses:** exit-cost lens (price the divorce before the wedding),
  scale cliff (works at pilot size, fails at production), contract-term traps.

#### 🪦 Kill / sunset decision (kill a product, feature, or initiative)

- **Roles:** Customer Strategist (who actually uses it; migration paths) ·
  Finance Lead (true cost of keeping vs. killing, including maintenance drag) ·
  Operator (deprecation mechanics, support tail) · Market Analyst (strategic
  value beyond revenue — wedge, moat, distribution) · Historian (how past
  sunsets went; trust damage).
- **Primary evidence:** usage data per account (exported, not remembered);
  conversations with the heaviest users; real maintenance-cost accounting.
- **Gate addition:** if nobody has talked to the top users of the thing being
  killed → stop.
- **Red-team lenses:** hidden-dependency lens (who breaks that you can't see),
  trust contagion (what churns *because* of the signal killing this sends),
  sunk-cost inversion (are we killing it just to feel decisive?).

### The one rule that transfers everywhere

Every variant exists to answer the same question the original does: **what is
the short list of cheap, falsifiable tests that would actually change what you
do?** If an adaptation starts optimising for a more persuasive memo instead of
a better test list, it has lost the plot — no matter how good the role briefs
are.
