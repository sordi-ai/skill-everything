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
| fastapi endpoint, pydantic model, async api | FastAPI | `skills/fastapi/SKILL.md` |
| langchain, lcel chain, agent framework | LangChain / Agent Framework Conventions | `skills/langchain/SKILL.md` |
| typescript code, strict types, async typescript | TypeScript | `skills/typescript/SKILL.md` |
| react component, react hooks, react performance | React | `skills/react/SKILL.md` |
| test-driven development, red green refactor, test first | Test-Driven Development | `skills/tdd/SKILL.md` |
| debugging, troubleshooting, root cause analysis, isolating bugs | Debugging | `skills/debugging/SKILL.md` |
| security review, vulnerability check, auth implementation | Security Review Depth | `skills/security-review/SKILL.md` |
| git commit, branch, pull request | Git Conventions | `skills/git-conventions/SKILL.md` |
| gh cli, github pr create, github issues | GitHub CLI (`gh`) Conventions | `skills/github-cli/SKILL.md` |
| finish branch, pre-merge checklist, branch cleanup | Closing Out a Feature Branch | `skills/branch-finishing/SKILL.md` |
| creating PR, deployment, review checklist | Review & Deployment | `skills/review-deployment/SKILL.md` |
| dockerfile, docker compose, container build | Docker / Container Conventions | `skills/docker/SKILL.md` |
| bash script, shell script, posix scripting | Bash / POSIX Scripting | `skills/shell-scripting/SKILL.md` |
| database schema, migration, table design | Database Schema Design | `skills/db-schema/SKILL.md` |
| svg edit, svg review, diagram, pixel review | SVG Check | `skills/svg-check/SKILL.md` |
| architecture diagram, mermaid diagram, drawio file | Diagrams (draw.io / Mermaid) | `skills/drawio/SKILL.md` |
| project-specific knowledge, business rules | Domain Knowledge (template) | `skills/domain-template/SKILL.md` |
| made or corrected a mistake, learn from this | Error Log | `skills/error-log/SKILL.md` |
| brainstorming, idea generation, divergent thinking | Brainstorming | `skills/brainstorming/SKILL.md` |
| implementation plan, planning before code, scope definition | Implementation Plan | `skills/implementation-plan/SKILL.md` |
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
