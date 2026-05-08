# Self-Extension Workflow

**Purpose:** Exact prompt and procedure the agent executes after every mistake
to automatically update the skill system.

---

## Trigger Conditions

The agent starts this workflow when **any** of these conditions is met:

- A test fails and the agent wrote the faulty code
- A code review comment corrects the agent
- The agent realizes during implementation that its first approach was wrong
- A deployment problem occurs that the agent caused
- The user explicitly says: "That was wrong" / "Remember this"

---

## Step-by-Step Procedure

### Step 0: Search before Write (MANDATORY)

**Before creating a new error entry**, search the existing error log:

```
1. Read references/errors/error-log.md
2. Search for similar errors (same category + similar context)
3. If a similar entry exists:
   → Increment its `count` field by 1
   → Update `last_seen` to today
   → Supplement the context if needed
   → Do NOT create a new entry
4. Only if no similar entry exists → continue with Step 1
```

### Step 1: Analyze the Error

The agent internally asks itself these questions:

```
1. What exactly did I do? (concrete code/action)
2. What should I have done instead?
3. Why did I do it wrong? (false assumption, missing knowledge, carelessness)
4. Which category applies?
   - development: code error, wrong implementation
   - git: commit/branch mistake
   - deployment: deployment order, configuration
   - security: security vulnerability
   - performance: N+1, missing indexes, datasets too large
   - domain: wrong understanding of business rules
5. How severe was the error? (critical/high/medium/low)
```

### Step 2: Determine New Error ID

```bash
# Find last entry in error-log.md
grep "id: ERR-" references/errors/error-log.md | tail -1
# Take next number: ERR-2025-004 → ERR-2025-005
```

### Step 3: Formulate Error Entry

The agent fills out the template from `references/errors/error-log.md`.
**Critical:** The `new_rule` must be an **action directive**, not a description.

❌ Bad: `"SQL injection is dangerous"`
✅ Good: `"Never concatenate user input directly into SQL. Always use prepared statements."`

### Step 4: Determine Target File

| Error Category | Target File |
|---------------|------------|
| development | `references/development/code-quality.md` |
| git | `references/git/conventions.md` |
| deployment | `references/process/review-deployment.md` |
| security | `references/development/code-quality.md` (Security section) |
| performance | `references/development/code-quality.md` (Performance section) |
| domain | `references/domain/<project>.md` |

### Step 5: Insert Rule

1. Open the target file
2. Find the matching category section
3. Add the new rule at the end of the section
4. Number continues sequentially
5. Add reference: `Reference: ERR-YYYY-NNN`

### Step 6: Commit

```bash
git add references/
git commit -m "learn(errors): ERR-YYYY-NNN — [short description]"
```

The commit message uses the `learn` type — so it's visible in the git log that this was a knowledge update, not a feature or bugfix.

---

## Consolidation Loop

When the error log exceeds 50 entries, the agent performs consolidation:

```
1. Read all entries in references/errors/error-log.md
2. Group by root_cause similarity
3. For groups with same root cause:
   → Keep the most detailed entry
   → Sum up all `count` values
   → Set `last_seen` to the most recent date
   → Delete the duplicates
4. For entries older than 6 months with severity: low:
   → Archive (move to a comment block or separate archive file)
   → The rules derived from them remain in the sub-skills
5. Commit: "chore(errors): consolidate error log (N entries merged)"
```

**When to run:** Every 10th new entry, or when the user explicitly requests it.

---

## Why This Sub-Skill Earns Stars

The agent doesn't just fix errors — it learns from them.
Every mistake makes the system permanently better, and the improvement is traceable, revertable, and reviewable via Git.
