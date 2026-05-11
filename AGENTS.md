# AGENTS.md
*Cross-tool agent instructions for skill-everything.*

> This file follows the [AGENTS.md convention](https://agents.md) — a universal Markdown file AI coding agents read for project-specific instructions. Generated from `skills/_index.yml`; edit the index, then run `python tools/render_loaders.py`.

## What this project is

Git-versioned agent memory — agents that never make the same mistake twice.

## Sub-skill directory

| Trigger | Sub-skill | Path |
|---|---|---|
| writing code, refactoring, review | Code Quality | `skills/code-quality/SKILL.md` |
| python code, type hints, python packaging | Python | `skills/python/SKILL.md` |
| typescript code, strict types, async typescript | TypeScript | `skills/typescript/SKILL.md` |
| react component, react hooks, react performance | React | `skills/react/SKILL.md` |
| git commit, branch, pull request | Git Conventions | `skills/git-conventions/SKILL.md` |
| creating PR, deployment, review checklist | Review & Deployment | `skills/review-deployment/SKILL.md` |
| svg edit, svg review, diagram, pixel review | SVG Check | `skills/svg-check/SKILL.md` |
| project-specific knowledge, business rules | Domain Knowledge (template) | `skills/domain-template/SKILL.md` |
| made or corrected a mistake, learn from this | Error Log | `skills/error-log/SKILL.md` |
| executing self-extension | Self-Extension Workflow | `skills/self-extension-workflow/SKILL.md` |

## How to use

1. Match your task to a trigger above.
2. Read the matching `skills/<name>/SKILL.md` before writing code.
3. Apply the rules in that sub-skill.
4. After a mistake, follow `skills/self-extension-workflow/SKILL.md`:
   - Search the existing error log for similar entries.
   - If found, increment `count`. If not, add a new entry.
   - Update the matching target sub-skill with the derived rule.
   - Open a PR labelled `needs-rule-review`. CI runs `lint-rules` + `auto-approve-rule-pr` gates; CODEOWNERS approval is required.

## Important

- **Search before write.** Duplicates in the error log destroy the signal.
- **Action directives, not descriptions.** Rules start with: Always, Never, Before, After, Prefer, Avoid, Use, Do, Ensure.
- **Stay compact.** Each sub-skill stays under 3,000 tokens. Split if it grows.
- **PR-flow is mandatory.** Self-extension commits open PRs; never push to `main` directly.
