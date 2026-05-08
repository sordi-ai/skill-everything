# Self-Extension Workflow
<!-- target: ~1100 tokens -->

**Purpose:** Exact prompt and procedure the agent executes after every mistake to update the skill system. **The agent never pushes to `main` directly. Every self-extension is a PR.**

---

## Trigger conditions

The agent starts this workflow when **any** of these conditions is met:

- A test fails and the agent wrote the faulty code.
- A code review comment corrects the agent.
- The agent realises during implementation that its first approach was wrong.
- A deployment problem occurs that the agent caused.
- The user explicitly says: "That was wrong" / "Remember this".

---

## Step-by-step procedure

### Step 0: Search before write (MANDATORY)

Before creating a new error entry, search the existing error log:

```
1. Read references/errors/error-log.md.
2. Search for similar errors (same category + similar context).
3. If a similar entry exists:
   → Increment its `count` field by 1.
   → Update `last_seen` to today.
   → Supplement the context if needed.
   → Do NOT create a new entry.
4. Only if no similar entry exists → continue with Step 1.
```

### Step 1: Analyse the error

The agent internally answers these questions:

```
1. What exactly did I do? (concrete code/action)
2. What should I have done instead?
3. Why did I do it wrong? (false assumption, missing knowledge, carelessness)
4. Which category applies?
   - development: code error, wrong implementation
   - git: commit/branch mistake
   - deployment: deployment order, configuration
   - security: security vulnerability
   - performance: N+1, missing indexes, oversized datasets
   - domain: wrong understanding of business rules
5. How severe was the error? (critical/high/medium/low)
```

### Step 2: Determine new error ID

```bash
# Find last entry in error-log.md
grep "id: ERR-" references/errors/error-log.md | tail -1
# Take next number: ERR-2026-004 → ERR-2026-005
```

### Step 3: Formulate the entry

Use the template at `references/_templates/error-entry.template.md`. The schema at [`schemas/error-entry.json`](../../schemas/error-entry.json) is enforced by CI.

**Critical:** the `new_rule` must be an **action directive**, not a description. It must start with one of: `Always`, `Never`, `Before`, `After`, `Prefer`, `Avoid`, `Use`, `Do`, `Ensure`. The CI validator will reject anything else.

❌ Bad: `"SQL injection is dangerous"`
✅ Good: `"Never concatenate user input directly into SQL queries. Always use prepared statements."`

### Step 4: Determine target file

| Error category | Target file |
|---|---|
| development | `references/development/code-quality.md` |
| git | `references/git/conventions.md` |
| deployment | `references/process/review-deployment.md` |
| security | `references/development/code-quality.md` (Security section) |
| performance | `references/development/code-quality.md` (Performance section) |
| domain | `references/domain/<project>.md` |

### Step 5: Insert the rule

1. Open the target file.
2. Find the matching category section.
3. Add the new rule at the end of the section.
4. Add reference: `Reference: ERR-YYYY-NNN`.

### Step 6: Open a PR (NEVER push to `main` directly)

```bash
git checkout -b learn/ERR-YYYY-NNN
git add references/
git diff --cached            # MANDATORY human review step
git commit -m "learn(errors): ERR-YYYY-NNN — <short description>

Co-Authored-By: <your real name> <your-email@example.com>"
git push -u origin learn/ERR-YYYY-NNN
gh pr create --label needs-rule-review \
             --title "learn(errors): ERR-YYYY-NNN" \
             --body "Auto-generated rule. Reviewer: confirm rule wording and target file. CI \`lint-rules\` must pass."
```

![PR flow — branch, commit, push, PR; lint-rules and auto-approve-rule-pr CI gates run in parallel; CODEOWNERS human gate; squash-merge into main behind branch protection](../../docs/pr-flow.svg)

*Branch through CI gates and CODEOWNERS into a squash-merge on `main`.*

**Why a PR (not a direct commit):**

| Layer | What it gates | Where |
|---|---|---|
| `lint-rules` | Schema + verb allow-list + forbidden patterns | [`schemas/error-entry.json`](../../schemas/error-entry.json) |
| `auto-approve-rule-pr` | Diff scope (`references/errors/**`) and `Co-Authored-By:` trailer | `.github/workflows/auto-approve-rule-pr.yml` |
| Branch protection | CODEOWNERS approval for `references/errors/` | `.github/CODEOWNERS` |
| Human review | Final read of rule wording and target file | maintainer |

> [!NOTE]
> The four-layer gating is what `pr-flow.svg` above shows. Every rule that goes live has been seen by a human. The validator is best-effort, not airtight — see [SECURITY.md](../../SECURITY.md) Limitations section.

The commit type `learn` makes self-extension visible in `git log --grep="learn("`.

---

## False positives in the validator

If the validator rejects a legitimate rule (e.g. a rule about preventing `subprocess` misuse that itself contains the word `subprocess`):

1. Add the new error ID to `references/errors/exceptions.yml`:
   ```yaml
   allow_forbidden_pattern_for:
     - ERR-YYYY-NNN  # rationale: rule must mention `subprocess` to be specific
   ```
2. Open the PR. CODEOWNERS approval is required for `exceptions.yml` changes — the bypass is auditable in git.
3. The verb allow-list still applies even with a bypass entry.

---

## Consolidation loop

When the error log exceeds 50 entries, run consolidation:

```
1. Read all entries in references/errors/error-log.md.
2. Group by root_cause similarity.
3. For groups with the same root cause:
   → Keep the most detailed entry.
   → Sum up all `count` values.
   → Set `last_seen` to the most recent date.
   → Delete the duplicates.
4. For entries older than 6 months with severity: low:
   → Archive (move to a comment block or separate archive file).
   → The rules derived from them remain in the sub-skills.
5. Open a PR: "chore(errors): consolidate error log (N entries merged)".
```

LLM-driven consolidation is non-deterministic. Until the eval framework (Phase 2 roadmap) reports a stable baseline, do consolidation **manually** with diff review. The threshold of 50 entries is a soft signal, not a forced rebuild.

---

## Why this sub-skill matters

The agent doesn't just fix errors — it learns from them, and every lesson is a Git commit you can review, revert, or share. The PR-flow turns "the LLM writes its own rules" from a magic feature into a supply-chain problem with a normal solution: review, lint, branch protection, code owners.
