# Skill-Everythink

You are using the **Skill-Everythink** knowledge system. It contains accumulated knowledge from past mistakes, project conventions, domain knowledge, and processes.

## Your Responsibilities

1. **Before every implementation:** Check if relevant sub-skills exist and load them using `@references/...` imports.
2. **After every mistake:** Execute the self-extension workflow (see below).
3. **When you learn something new:** Add it to the appropriate category.

## Sub-Skill Directory

Load the matching sub-skill when the context applies:

| Context | Sub-Skill | Load via |
|---------|-----------|----------|
| Writing, refactoring, or reviewing code | Code Quality | `@references/development/code-quality.md` |
| Git operations, commits, branches, PRs | Git Conventions | `@references/git/conventions.md` |
| Project-specific knowledge needed | Domain Knowledge | `@references/domain/template.md` |
| Creating PRs, deployment, review | Review & Deployment | `@references/process/review-deployment.md` |
| Made or corrected a mistake | Error Log | `@references/errors/error-log.md` |

## Error Capture Triggers

Start the self-extension workflow when:

- A test fails because of your code
- The user corrects you ("That was wrong", "Remember this")
- You realize your first approach was wrong
- A deployment issue occurs

**Load workflow:** `@references/errors/self-extension-workflow.md`

## Consolidation Rule

When `references/errors/error-log.md` has more than 50 entries:
1. Merge similar errors (same root cause → one entry with `count`)
2. Archive errors older than 6 months with `severity: low`
3. Rules derived from errors remain in their respective sub-skills

## Important

- **Search before Write:** Before logging a new error, search the error log for similar entries. Update instead of duplicate.
- **Action directives, not descriptions:** Always formulate rules as "Always X before Y" or "Never Z without W".
- **Stay compact:** Each sub-skill should stay under 3000 tokens. If exceeded → split.
