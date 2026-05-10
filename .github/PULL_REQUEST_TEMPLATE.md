<!-- Pick one and delete the others. -->

## Type

- [ ] `learn(errors)` — new rule from a real observed mistake (use `.github/PULL_REQUEST_TEMPLATE/rule-learning.md`)
- [ ] `feat(skills)` — new sub-skill (use `.github/PULL_REQUEST_TEMPLATE/sub-skill.md`)
- [ ] `feat(tools)` — automation / generators / validators
- [ ] `fix(security)` — security-relevant change
- [ ] `fix` / `chore` / `docs` / `refactor` / `test` — other

## What does this PR change?

<!-- One paragraph. The "why" matters more than the "what". -->

## Why now?

<!-- What triggered this change? A bug? A user report? An adjacent change? -->

## Risk

<!-- Be specific. "low risk" is not specific. -->

- [ ] Touches `skills/error-log/` (CODEOWNERS required, lint-rules CI)
- [ ] Touches `tools/` or `schemas/` (CODEOWNERS required)
- [ ] Adds/changes `_index.yml` (loaders-and-table-no-drift CI must pass)
- [ ] Affects security posture (please link to the relevant SECURITY.md section)
- [ ] None of the above

## Checklist

- [ ] CI is green locally (`pytest -q` + `ruff check .` + `python tools/render_loaders.py --check`)
- [ ] If this PR adds a rule: a corresponding `tests/eval/tasks/*.yml` test exists or is in a follow-up issue
- [ ] If this PR changes the README: I ran `python tools/render_readme_table.py` if the token table was affected
- [ ] No secrets, prod data, or customer identifiers in the diff
