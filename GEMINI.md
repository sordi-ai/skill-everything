# skill-everything

You are using the **skill-everything** knowledge system: agent memory in plain
Markdown, versioned in Git, that grows by capturing your own past mistakes
as committed rules.

## Your responsibilities

1. **Before every implementation:** check the sub-skill directory below, reference the matching skill via `@skills/<name>/SKILL.md` (Gemini imports merge file content into context — see "Token reality" note below; this is modularization, not lazy loading).
2. **After every mistake:** execute the self-extension workflow.
3. **When you learn something new:** add it to the appropriate category.

Use `/memory show` to verify the loaded context. Use `/memory refresh` after edits.

> **Token reality (Gemini-specific).** `@skills/<name>/SKILL.md` references modularize this file; Gemini parses GEMINI.md with the imported sub-skill content included, not lazily on demand. The token saving comes from the compact router (~800 tokens vs `10,000+` monolithic), not selective sub-skill loading. See README → [Per-tool token reality](./README.md#per-tool-token-reality).

## Sub-skill directory

| Trigger | Sub-skill | Load via |
|---|---|---|
| writing code, refactoring, review | Code Quality | `@skills/code-quality/SKILL.md` |
| python code, type hints, python packaging | Python | `@skills/python/SKILL.md` |
| typescript code, strict types, async typescript | TypeScript | `@skills/typescript/SKILL.md` |
| react component, react hooks, react performance | React | `@skills/react/SKILL.md` |
| git commit, branch, pull request | Git Conventions | `@skills/git-conventions/SKILL.md` |
| creating PR, deployment, review checklist | Review & Deployment | `@skills/review-deployment/SKILL.md` |
| svg edit, svg review, diagram, pixel review | SVG Check | `@skills/svg-check/SKILL.md` |
| project-specific knowledge, business rules | Domain Knowledge (template) | `@skills/domain-template/SKILL.md` |
| made or corrected a mistake, learn from this | Error Log | `@skills/error-log/SKILL.md` |
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
