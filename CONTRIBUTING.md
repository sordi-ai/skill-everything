# Contributing to skill-everything
*Three flows: `learn(errors)`, `feat(skills)`, everything else. The rules apply to maintainers and external contributors alike.*

> **Pull requests are how this project grows.** Every merged `learn(errors):` is a brick in the public agent-memory layer. **From error to rule in one PR.** Welcome.

This is an independent open-source project — see [DISCLAIMER.md](./DISCLAIMER.md). The visual conventions in this file (tables, callouts, code-block language hints) follow the same style as the rest of the repo. Consistency makes review faster.

If something below is unclear or wrong, open an issue or a PR fixing it.

---

## QUICK START
*Five minutes from `git clone` to passing tests.*

```bash
git clone https://github.com/sordi-ai/skill-everything.git
cd skill-everything
pip install -e ".[dev]"
pre-commit install
pytest -q
```

If `pytest` passes locally, you are ready. Branch off `main`, follow the relevant flow below, open a PR.

---

## THREE CONTRIBUTION FLOWS
*One header per flow. Each flow has its own PR template under `.github/PULL_REQUEST_TEMPLATE/`.*

### 1. `learn(errors)` — new rule from a real mistake
*The primary contribution flow. Every rule should be born from a real observed mistake, not from opinion.*

The full procedure with troubleshooting lives at [`skills/self-extension-workflow/SKILL.md`](./skills/self-extension-workflow/SKILL.md).

1. Copy [`skills/error-log/_entry-template.md`](./skills/error-log/_entry-template.md).
2. Search [`skills/error-log/SKILL.md`](./skills/error-log/SKILL.md) for similar entries first. If you find one, increment its `count` and update `last_seen` instead of writing a new entry.
3. If no match: add a new YAML block at the end. Pick the next sequential `ERR-YYYY-NNN`.
4. Add the derived rule to the matching sub-skill (development / git / process / domain / errors). The `target_file` field tells the validator where to look.
5. Branch + commit + PR — never push to `main`:
   ```bash
   git checkout -b learn/ERR-YYYY-NNN
   git add skills/
   git diff --cached            # mandatory self-review
   git commit -m "learn(errors): ERR-YYYY-NNN — <short>

   Co-Authored-By: Real Name <real@email>"
   git push -u origin learn/ERR-YYYY-NNN
   gh pr create --label needs-rule-review
   ```
6. The CI `lint-rules` validator runs against the JSON-Schema and the verb allow-list. The `auto-approve-rule-pr` workflow gates merge on diff-scope and the `Co-Authored-By:` trailer.
7. A maintainer reviews and merges. **Always squash-merge.**

> [!NOTE]
> **CI GATE · lint-rules + auto-approve-rule-pr** — both gates run before any human review on `learn(errors)` PRs.

### 2. `feat(skills)` — new sub-skill
*When the existing sub-skills do not cover an area you need (Go, Rust, Java, IaC, etc.).*

1. Copy [`skills/_template/SKILL.md`](./skills/_template/SKILL.md).
2. Pick a kebab-case `id` and a target file path: `skills/<id>/SKILL.md`.
3. Fill in the YAML frontmatter — the schema is at [`schemas/skill-manifest.json`](./schemas/skill-manifest.json):
   ```yaml
   ---
   id: go
   version: 1.0.0
   tokens_target: 2200      # hard cap: 3000
   triggers:
     - go code
     - go modules
     - error handling
   loads_after:
     - code-quality
   supersedes: []
   ---
   ```
4. Write **at least 8 concrete action-directive rules**, each grounded in a real mistake or convention you have observed.
5. Add an entry to [`skills/_index.yml`](./skills/_index.yml) with the loader strings for `claude`, `gemini`, and `skill_resource`. Then run `python tools/render_loaders.py` so `SKILL.md`, `CLAUDE.md`, and `GEMINI.md` regenerate. Commit those changes — the CI no-drift job verifies them.
6. Branch as `feat/skill-<id>`, PR title `feat(skills): add <id>`, label `new-skill`.

**Sub-skill PR review checklist.** *Six checks. Reviewers can copy-paste from the table into the PR conversation.*

| Check | What | Where verified |
|---|---|---|
| Schema | Frontmatter passes `python tools/validate_rules.py` | `schemas/skill-manifest.json` |
| Token budget | `tokens_target` < 3000 and real count < `tokens_target` | `tools/render_readme_table.py` |
| Verb allow-list | Every rule starts with `Always`, `Never`, `Before`, `After`, `Prefer`, `Avoid`, `Use`, `Do`, or `Ensure` | `tools/validate_rules.py` |
| Cross-reference | At least one link to an existing sub-skill | reviewer reads diff |
| Real grounding | At least one rule has `Reference: ERR-YYYY-NNN`, or a fresh ERR is added in the same PR | `skills/error-log/SKILL.md` |
| Re-mistake test | At least one task added to `tests/eval/tasks/` | `tests/eval/README.md` |

### 3. `feat` / `fix` / `chore` — tooling, docs, infrastructure
*The normal open-source flow. Conventional Commits as below; PR titles describe the why, not the what.*

For everything that is not a rule — fixes to `tools/`, docs, CI — the normal flow applies.

---

## COMMIT CONVENTIONS
*Conventional Commits with a small custom set of types.*

| Type | Use for |
|---|---|
| `learn(errors)` | A rule generated by the self-extension workflow |
| `feat(skills)` | New or expanded sub-skill |
| `feat(tools)` | New or expanded automation |
| `fix(security)` | Security-relevant fix |
| `fix` / `feat` / `chore` / `docs` / `test` / `refactor` | Standard |

Subject in the imperative. ≤ 72 characters. Body explains *why*, not *what*.

```text
learn(errors): ERR-YYYY-NNN — never inherit from concrete React components
```

(Replace `ERR-YYYY-NNN` with the next sequential error ID from `skills/error-log/SKILL.md`.)

---

## VALIDATOR FALSE-POSITIVE BYPASS
*The CI `lint-rules` validator is best-effort, not airtight. See [SECURITY.md](./SECURITY.md).*

When a legitimate rule has to mention a forbidden pattern (e.g. a rule about preventing `subprocess` misuse that names `subprocess`):

1. Add the new ERR-ID to [`skills/error-log/exceptions.yml`](./skills/error-log/exceptions.yml) with a one-line rationale.
2. CODEOWNERS approval is required to merge changes to that file. The bypass is auditable in git.
3. The verb allow-list still applies even with a bypass entry.

If you are not sure whether to bypass, ask in the PR — false positives are usually fixed by rephrasing.

---

## EVAL CONTRIBUTIONS
*Re-mistake tests live with the rules they cover.*

When a new rule lands, please add a re-mistake test to [`tests/eval/tasks/`](./tests/eval/) so future runs measure whether the rule actually prevents the mistake. The contract for what counts as a published Re-Mistake-Rate is in [`tests/eval/README.md`](./tests/eval/README.md). **Until that contract is met, no Re-Mistake-Rate goes into the README — n = 3 isn't an evaluation, it's a vibe check.**

---

## CO-MAINTAINER ONBOARDING
*Five steps before your first push, if you become one of us.*

> [!WARNING]
> **CODEOWNERS gate · employer compliance disclosure** — Compliance disclosure required before first push. If your employer has a personal-open-source disclosure policy, file it first. We will not ship a PR signed by your work account.

1. **Compliance check.** File a personal-open-source disclosure with your employer. The `DISCLAIMER.md` is the public-facing doc; the disclosure is the private one.
2. **Use a personal GitHub account** with your real name. Pseudonymous co-maintainer commits are not accepted — `git shortlog -sne` is the first thing skeptical readers check.
3. **Add yourself to `.github/CODEOWNERS`** under the `@sordi-ai/maintainers` team and confirm with the existing maintainer.
4. **Read the threat model** in [SECURITY.md](./SECURITY.md). The self-extension workflow runs against `.github/CODEOWNERS`. You are responsible for the CODEOWNERS approval gate on the paths assigned to your handle.
5. **Workload expectation.** Split: code + eval (existing maintainer) and sub-skill content + issue triage (new co-maintainer). Coordinate on `skills/error-log/` so concurrent edits don't conflict.

---

## FOLDER STRUCTURE
*Where things live. Adding a new top-level category needs two-of-two maintainer review.*

```text
skills/
├── _index.yml                       # source of truth for SKILL/CLAUDE/GEMINI/.cursorrules
├── _template/SKILL.md               # copy this folder to start a new skill
├── code-quality/SKILL.md            # generic code rules
├── python/SKILL.md
├── typescript/SKILL.md
├── react/SKILL.md
├── git-conventions/SKILL.md         # commit, branch, PR conventions
├── review-deployment/SKILL.md       # review + deployment checklists
├── domain-template/SKILL.md         # template for project-specific knowledge
├── error-log/
│   ├── SKILL.md                     # YAML entries, schema-validated
│   ├── exceptions.yml               # validator bypass list
│   └── _entry-template.md           # error entry template
└── self-extension-workflow/SKILL.md # six-step self-extension workflow
```

Adding a new top-level category? Open a PR that updates this README, `skills/_index.yml`, and the relevant template.

---

## WHAT MAKES A GOOD CONTRIBUTION
*Concrete beats clever. Real beats hypothetical. Reviewed by humans, growing by Git commits — that's the deal.*

| Good | Bad |
|---|---|
| Concrete rules from real projects | Generic tips you would find in any tutorial |
| Action directives | Descriptions ("X is dangerous") |
| Error entries with a real `count` ≥ 1 from observation | Hypothetical examples |
| Domain knowledge no LLM has by default | Personal opinions without grounding |
| Cross-references to existing skills | Duplicates or near-duplicates |

Thanks. Pull requests are how this project grows.
