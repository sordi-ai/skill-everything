# skill-everything

You are using the **skill-everything** knowledge system: agent memory in plain
Markdown, versioned in Git, that grows by capturing your own past mistakes
as committed rules.

## Your responsibilities

1. **Before every implementation:** check the sub-skill directory below, load the matching skill using `@skills/<name>/SKILL.md` imports.
2. **After every mistake:** execute the self-extension workflow.
3. **When you learn something new:** add it to the appropriate category.

## Sub-skill directory

| Trigger | Sub-skill | Load via |
|---|---|---|
| writing code, refactoring, review | Code Quality | `@skills/code-quality/SKILL.md` |
| python code, type hints, python packaging | Python | `@skills/python/SKILL.md` |
| fastapi endpoint, pydantic model, async api | FastAPI | `@skills/fastapi/SKILL.md` |
| langchain, lcel chain, agent framework | LangChain / Agent Framework Conventions | `@skills/langchain/SKILL.md` |
| typescript code, strict types, async typescript | TypeScript | `@skills/typescript/SKILL.md` |
| react component, react hooks, react performance | React | `@skills/react/SKILL.md` |
| test-driven development, red green refactor, test first | Test-Driven Development | `@skills/tdd/SKILL.md` |
| debugging, troubleshooting, root cause analysis, isolating bugs | Debugging | `@skills/debugging/SKILL.md` |
| security review, vulnerability check, auth implementation | Security Review Depth | `@skills/security-review/SKILL.md` |
| git commit, branch, pull request | Git Conventions | `@skills/git-conventions/SKILL.md` |
| gh cli, github pr create, github issues | GitHub CLI (`gh`) Conventions | `@skills/github-cli/SKILL.md` |
| finish branch, pre-merge checklist, branch cleanup | Closing Out a Feature Branch | `@skills/branch-finishing/SKILL.md` |
| creating PR, deployment, review checklist | Review & Deployment | `@skills/review-deployment/SKILL.md` |
| dockerfile, docker compose, container build | Docker / Container Conventions | `@skills/docker/SKILL.md` |
| bash script, shell script, posix scripting | Bash / POSIX Scripting | `@skills/shell-scripting/SKILL.md` |
| database schema, migration, table design | Database Schema Design | `@skills/db-schema/SKILL.md` |
| svg edit, svg review, diagram, pixel review | SVG Check | `@skills/svg-check/SKILL.md` |
| architecture diagram, mermaid diagram, drawio file | Diagrams (draw.io / Mermaid) | `@skills/drawio/SKILL.md` |
| project-specific knowledge, business rules | Domain Knowledge (template) | `@skills/domain-template/SKILL.md` |
| made or corrected a mistake, learn from this | Error Log | `@skills/error-log/SKILL.md` |
| brainstorming, idea generation, divergent thinking | Brainstorming | `@skills/brainstorming/SKILL.md` |
| implementation plan, planning before code, scope definition | Implementation Plan | `@skills/implementation-plan/SKILL.md` |
| executing self-extension | Self-Extension Workflow | `@skills/self-extension-workflow/SKILL.md` |

## Error capture triggers

Start the self-extension workflow when **any** of these is met:

- A test fails because of code you wrote.
- The user corrects you ("That was wrong", "Remember this").
- You realise during implementation that your first approach was wrong.
- A deployment problem occurs that your code caused.

Load the workflow:

```
@skills/self-extension-workflow/SKILL.md
```

## Important

- **Search before write.** Before logging a new error, search the existing log for similar entries. Update instead of duplicate.
- **Action directives, not descriptions.** Always formulate rules as "Always X before Y" or "Never Z without W".
- **Stay compact.** Each sub-skill stays under 3,000 tokens. If exceeded, split.
- **PR-flow is mandatory.** Self-extension commits are opened as PRs labelled `needs-rule-review`. Never push to `main`.

> This file is generated from `skills/_index.yml`. Edit the index, then run `python tools/render_loaders.py`.
