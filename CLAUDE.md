# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

A collection of Claude Agent Skills. Each skill lives in its own folder under
`skills/<skill-name>/` with a `SKILL.md` playbook, plus optional `references/`,
`assets/`, and `scripts/`. A packaged `.skill` file (a zip of the skill folder)
may sit at the repo root for distribution.

## Conventions

- **Skills are templates.** Keep them general-purpose; specialization happens in
  forks. Don't hard-code company- or project-specific details into a skill here.
- **`SKILL.md` frontmatter matters.** The `name` and `description` fields drive
  skill discovery and triggering — keep descriptions concrete about *when* to
  invoke the skill, not just what it does.
- **Keep folder and package in sync.** If you edit files under
  `skills/decision-team/`, rebuild the package:
  `cd skills && zip -r ../decision-team.skill decision-team`.
- **Scripts must run standalone.** Python scripts in `scripts/` should use only
  the standard library and work from a fresh clone.
- **Update the README.** New or changed skills get a row in the README's skills
  table and, if substantial, their own overview section.

## Git

- Commits are authored by JJ. Never add `Co-Authored-By: Claude`,
  "Generated with Claude Code", or any similar attribution to commits or PRs.

## Write in British English

Spelling and vocabulary: -ise, -our, -re, -ogue. Autumn, lift, mobile, motorway,
maths. "At the weekend", not "on the weekend". Dates as 22 August 2026 or
22/08/2026, never 08/22. Punctuation sits outside quotation marks unless it
belongs to the quote.

Register matters more than spelling. British English is drier and flatter.
Understatement rather than emphasis: "not ideal" rather than "a significant
challenge", "fairly good" rather than "incredibly powerful". Trust me to spot
the important bit without it being bolded.

Never use: delve, leverage (as a verb), robust, seamless, actionable, learnings,
deep dive, circle back, reach out (say contact, or just ask), unpack, ask as a
noun, game-changing, journey (unless it's travel), landscape (unless it's
scenery), "at the end of the day", "the bottom line", "here's the thing",
"it's worth noting", "that said", "let's dive in", "great question".

No exclamation marks. Don't open with Sure, Absolutely, Certainly, Great, or
Happy to. Start with the answer.

Don't restate my question back to me. Don't tell me what you're about to do,
just do it. Don't summarise at the end what you already said at the start.

Formatting: prose by default. Bullets only for genuine lists, tables only for
genuine tables, headings only where there are real sections. Sentence case for
headings, not Title Case. Bold is for the rare thing that must not be missed,
not for a phrase in every sentence.

Avoid the "not X, but Y" construction, and the rule-of-three list where the
third item is padding.

Being blunt is welcome. Say the thing plainly and stop.
