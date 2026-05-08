---
name: skill-everything
description: Git-versioned agent memory — agents that never make the same mistake twice.
version: 1.2.0
---

# skill-everything

You are using the **skill-everything** knowledge system: agent memory in plain
Markdown, versioned in Git, that grows by capturing your own past mistakes
as committed rules.

## Your responsibilities

1. **Before every implementation:** check the sub-skill directory below,
   load the matching skill via `skill_resource(...)`.
2. **After every mistake:** execute the self-extension workflow.
3. **When you learn something new:** add it to the appropriate category.

## Sub-skill directory

| Trigger | Sub-skill | Load via |
|---|---|---|
| writing code, refactoring, review | Code Quality | `skill_resource(skill_name="skill-everything", relative_path="references/development/code-quality.md")` |
| python code, type hints, python packaging | Python | `skill_resource(skill_name="skill-everything", relative_path="references/development/python.md")` |
| typescript code, strict types, async typescript | TypeScript | `skill_resource(skill_name="skill-everything", relative_path="references/development/typescript.md")` |
| react component, react hooks, react performance | React | `skill_resource(skill_name="skill-everything", relative_path="references/development/react.md")` |
| git commit, branch, pull request | Git Conventions | `skill_resource(skill_name="skill-everything", relative_path="references/git/conventions.md")` |
| creating PR, deployment, review checklist | Review & Deployment | `skill_resource(skill_name="skill-everything", relative_path="references/process/review-deployment.md")` |
| project-specific knowledge, business rules | Domain Knowledge (template) | `skill_resource(skill_name="skill-everything", relative_path="references/domain/template.md")` |
| made or corrected a mistake, learn from this | Error Log | `skill_resource(skill_name="skill-everything", relative_path="references/errors/error-log.md")` |
| executing self-extension | Self-Extension Workflow | `skill_resource(skill_name="skill-everything", relative_path="references/errors/self-extension-workflow.md")` |

## Error capture triggers

Start the self-extension workflow when **any** of these is met:

- A test fails because of code you wrote.
- The user corrects you ("That was wrong", "Remember this").
- You realise during implementation that your first approach was wrong.
- A deployment problem occurs that your code caused.

Load the workflow:

```
skill_resource(skill_name="skill-everything", relative_path="references/errors/self-extension-workflow.md")
```

## Important

- **Search before write.** Before logging a new error, search the existing log for similar entries. Update instead of duplicate.
- **Action directives, not descriptions.** Always formulate rules as "Always X before Y" or "Never Z without W".
- **Stay compact.** Each sub-skill stays under 3,000 tokens. If exceeded, split.
- **PR-flow is mandatory.** Self-extension commits are opened as PRs labelled `needs-rule-review`. Never push to `main`.
- **Without `skill_resource`?** If your agent doesn't have the tool, load files directly via filesystem access from the `references/` folder.

> This file is generated from `references/_index.yml`. Edit the index, then run `python tools/render_loaders.py`.
