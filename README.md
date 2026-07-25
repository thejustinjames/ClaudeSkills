# 🛠️ Claude Skills

> A curated collection of [Claude Agent Skills](https://docs.claude.com/en/docs/claude-code) — reusable, structured playbooks that teach Claude how to run complex, repeatable workflows with rigor.

Skills are packaged instructions, reference material, and helper scripts that Claude loads on demand. Instead of re-explaining a process every session, a skill captures the process once — the workflow, the guardrails, the output format — and Claude follows it consistently.

**Every skill in this repo is a template.** They're built to be forked, trimmed, and honed to your specific team, domain, and decisions. Take the structure, swap in your own roles, evidence rules, and output formats, and make it yours.

---

## 📦 Skills in this collection

| Skill | What it does |
|-------|--------------|
| [`decision-team`](skills/decision-team/) | Multi-role strategy analysis for consequential decisions — build vs. buy, pricing, market entry, vendor selection, go/no-go. |

---

## 🎯 Featured skill: `decision-team`

**Strategy · Planning · Buy vs. Build**

A harness for making a consequential decision *well*. When you're weighing a real call — build or buy, raise prices, enter a market, kill a product, sign a contract — this skill runs a structured, adversarial analysis instead of a single-voice opinion.

### How it works

```
        ┌─────────────────────────────────────────────┐
        │  1. Evidence Gate                           │
        │     Thin inputs? Stop. Get facts first.     │
        └──────────────────┬──────────────────────────┘
                           ▼
        ┌─────────────────────────────────────────────┐
        │  2. Six Isolated Role Agents                │
        │     Disjoint evidence slices, no cross-talk │
        └──────────────────┬──────────────────────────┘
                           ▼
        ┌─────────────────────────────────────────────┐
        │  3. Red Team                                │
        │     Clean context. Job: break the decision. │
        └──────────────────┬──────────────────────────┘
                           ▼
        ┌─────────────────────────────────────────────┐
        │  4. Falsifiable Test List                   │
        │     Cheap experiments that would change     │
        │     the answer — not a persuasive memo      │
        └─────────────────────────────────────────────┘
```

### What makes it different

- **🚧 An evidence gate before any analysis.** If the inputs are thin (fewer than five primary/internal-data evidence items), it refuses to write a memo and instead produces an *Evidence Acquisition Plan* — the three cheapest things to find out this week. Analysis cannot manufacture evidence, and a beautifully formatted hallucination is worse than no analysis.
- **🧩 Manufactured independence.** Six analytical roles run as separate agents with disjoint evidence slices. Asking one model to play six characters produces six voices, not six perspectives — isolation is structural, not prompted.
- **🔗 Traceability on every claim.** Each claim is tagged to a specific evidence item or flagged as an assumption. A lint script (`evidence_lint.py`) makes fluent, unsupported prose expensive.
- **⚔️ Refutation, not review.** The red team runs afterward in a clean context, sees only the conclusion and raw evidence — never the reasoning — and is asked to *kill* the recommendation.
- **🧪 The output is tests, not a memo.** The deliverable is a short list of cheap, falsifiable experiments that would actually change what you do.

### What's inside

```
skills/decision-team/
├── SKILL.md                        # The core playbook
├── references/
│   ├── roles.md                    # The six analytical role definitions
│   ├── evidence-protocol.md        # Evidence tiers, citation rules, the gate
│   ├── redteam-protocol.md         # How the adversarial pass runs
│   └── memo-format.md              # Final output structure
├── assets/
│   ├── workspace/                  # Templates: context, decision, evidence…
│   └── examples/worked-example.md  # A full worked example
└── scripts/
    ├── init_workspace.py           # Scaffold a decision workspace
    ├── evidence_lint.py            # Enforce claim → evidence traceability
    └── rank_assumptions.py         # Rank assumptions by impact × uncertainty
```

A packaged, installable version is included as [`decision-team.skill`](decision-team.skill).

**📖 Read the full playbook:** [`skills/decision-team/README.md`](skills/decision-team/README.md) — the complete 10-step workflow, the evidence gate, role isolation, red-teaming rules, and how verdicts are constrained.

---

## 🚀 Using a skill

**Claude Code (this repo as a project):** skills placed under `.claude/skills/` (or referenced from `skills/`) are discovered automatically and invoked when the task matches their description — or explicitly via `/decision-team`.

**Claude apps:** upload the packaged `.skill` file where custom skills are supported.

Then just talk naturally:

> *"Should we build our own billing system or buy Stripe Billing?"*
> *"I'm torn between raising prices and adding a cheaper tier — help me think it through."*

---

## ✂️ Honing a template to your own tasks

These skills are deliberately general. To specialize one:

1. **Fork the skill folder** and rename it (e.g. `vendor-selection`).
2. **Rewrite the `description`** in `SKILL.md` frontmatter — that's what triggers the skill, so make it match *your* recurring task.
3. **Swap the roles and rules.** Replace the analytical roles, evidence tiers, and output formats in `references/` with the ones your domain actually uses.
4. **Tune the templates** in `assets/workspace/` to the context your team always needs captured.
5. **Keep the structure.** The gate → isolated analysis → adversarial pass → testable-output shape transfers to almost any high-stakes recurring workflow.

---

## 📄 Repository

This repository is **public and read-only** — feel free to read, clone, and adapt for your own use. Maintained by **JJ** ([@thejustinjames](https://github.com/thejustinjames)).
