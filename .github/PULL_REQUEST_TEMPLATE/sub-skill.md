<!--
Use this template when adding a new sub-skill (e.g. references/development/go.md).
Title: feat(skills): add <id>
Label: new-skill
-->

## Sub-skill identity

| | |
|---|---|
| `id` | `<kebab-case-id>` |
| Path | `references/<category>/<id>.md` |
| `tokens_target` | `<n>` (max 3000) |
| Real token count | `<n from python tools/render_readme_table.py>` |
| `triggers` | `<comma-separated short phrases>` |
| `loads_after` | `<other skill ids that should load first>` |

## Why this skill?

<!-- What gap does it fill? Show that you've checked the existing sub-skills
     and that this isn't a duplicate. -->

## Rule provenance

For each rule in the new file, fill one row. **Each rule must be grounded in either a real `ERR-YYYY-NNN` reference or a documented convention.**

| Rule # | Action directive (short) | Grounding |
|---|---|---|
| 1 | Always X before Y | `ERR-2026-…` |
| 2 | Never Z without W | "team convention since X" / cite |
| … | | |

## Loader sync

- [ ] Added entry to `references/_index.yml` with `claude` / `gemini` / `skill_resource` loader strings
- [ ] Ran `python tools/render_loaders.py` and committed regenerated `SKILL.md` / `CLAUDE.md` / `GEMINI.md`
- [ ] Ran `python tools/render_readme_table.py` and committed the README table update

## Eval coverage

- [ ] Added at least one task to `tests/eval/tasks/` that would surface a typical mistake this skill prevents
- [ ] Task includes a mistake-signature regex or AST query and a pass-signature
- [ ] (Optional) ran the task by hand and noted the result in the PR description

## Self-review

- [ ] Frontmatter passes `python tools/validate_rules.py`
- [ ] Real token count is below `tokens_target`, and `tokens_target` is below 3000
- [ ] At least one cross-reference to an existing sub-skill
- [ ] All rules start with one of the allowed verbs
- [ ] No URLs, shell binaries, or credentials in any rule

## Maintainer review checklist

- [ ] Token-budget enforced in CI
- [ ] Real-world groundings are convincing (not "any tutorial would say this")
- [ ] Action-directive phrasing throughout
- [ ] Eval task is meaningful, not a tautology
- [ ] No category collision with an existing sub-skill
