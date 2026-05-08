# Sub-Skill: Error Log

**Purpose:** Central memory for all mistakes the agent has made or observed.
Each entry prevents the same mistake from happening twice.

---

## Format Specification

Every error entry follows exactly this YAML format:

```yaml
- id: ERR-YYYY-NNN          # Year + sequential number, e.g. ERR-2025-001
  date: YYYY-MM-DD
  last_seen: YYYY-MM-DD     # Last occurrence (update on repeat)
  count: 1                   # How many times this error has occurred
  category: development|git|deployment|security|performance|domain
  severity: critical|high|medium|low
  context: |
    [1-3 sentences: In what situation did the error occur?
    What task was being worked on? Which project/module?]
  what_happened: |
    [Concrete description of what the agent did.
    Code snippet if relevant.]
  root_cause: |
    [Why did it happen? What false assumption was the cause?]
  impact: |
    [What was the consequence? Data loss? Security breach? Time wasted?]
  resolution: |
    [What was done to fix the error?]
  new_rule: |
    [The concrete rule derived from this error.
    Phrased as action directive: "Always X before Y" or "Never Z without W".]
  target_file: references/[category]/[filename].md   # Where the rule was added
```

---

## Example Entries

```yaml
errors:

  - id: ERR-2025-001
    date: 2025-03-14
    category: deployment
    severity: critical
    context: |
      Deploying a new API version for the OrderFlow service.
      The new version contained a DB migration that renames a column.
    what_happened: |
      Agent deployed the new backend first, then ran the migration.
      Between deployment and migration (~45 seconds), the new code
      ran against the old schema and threw 500 errors for all orders.
    root_cause: |
      False assumption: "Migration can run after deployment."
      Reality: When code expects new column names, migration MUST run FIRST.
    impact: |
      45 seconds of production downtime. ~200 failed API requests.
      No data loss, but customer complaints.
    resolution: |
      Immediately rolled back to old version. Ran migration.
      Then deployed new version. No errors this time.
    new_rule: |
      Always run additive DB migrations BEFORE deployment.
      For rename migrations: First add new column (additive),
      update code to use new column, then remove old column (separate deployment).
    target_file: references/process/review-deployment.md

  - id: ERR-2025-002
    date: 2025-03-18
    category: development
    severity: medium
    context: |
      Implementing a user search feature with filter by status.
    what_happened: |
      Agent wrote `SELECT * FROM users WHERE status = '${userInput}'`
      instead of using a parameterized query.
    root_cause: |
      Agent defaulted to string interpolation for "simplicity."
      Didn't consider that user input could contain SQL injection.
    impact: |
      Security vulnerability. Caught in code review before production.
    resolution: |
      Rewritten with prepared statement:
      `db.query('SELECT * FROM users WHERE status = $1', [userInput])`
    new_rule: |
      Never concatenate user input directly into SQL queries.
      Always use prepared statements or ORM query builders.
    target_file: references/development/code-quality.md
```

---

## Consolidation

When this file exceeds 50 entries:
1. Merge errors with the same root cause into one entry (increase `count`)
2. Archive entries older than 6 months with `severity: low`
3. Rules derived from errors remain in their respective sub-skills
