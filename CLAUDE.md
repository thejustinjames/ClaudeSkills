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
