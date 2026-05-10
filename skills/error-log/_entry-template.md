# Error Entry Template

Copy this block and fill in all fields:

```yaml
  - id: ERR-YYYY-NNN
    date: YYYY-MM-DD
    last_seen: YYYY-MM-DD
    count: 1
    category: development|git|deployment|security|performance|domain
    severity: critical|high|medium|low
    context: |
      [1-3 sentences: situation, task, module]
    what_happened: |
      [What exactly the agent did. Code snippet if relevant.]
    root_cause: |
      [Why it happened. What false assumption?]
    impact: |
      [Consequence: data loss? outage? time wasted?]
    resolution: |
      [What was done to fix the error?]
    new_rule: |
      [Action directive: "Always X before Y" or "Never Z without W".]
    target_file: skills/[name]/SKILL.md
    # Optional: link this entry to real artefacts. Include whatever is verifiable.
    evidence:
      commit_sha: "[full or short hex SHA, e.g. a84741d]"
      pr_number: 0                     # PR where the fix landed
      failing_run_url: "[URL of CI run that reproduces the failing state]"
      fixed_run_url: "[URL of CI run that demonstrates the fix]"
      reproduced_by_test: false        # true if a regression test exists
```

## Checklist Before Inserting

- [ ] Is a similar error already in the error log? → Update instead of new entry
- [ ] Is `new_rule` an action directive (not just a description)?
- [ ] Was the rule added to the matching target file?
- [ ] Is the next available ERR-ID correct?
- [ ] Are evidence fields filled in for fields you can actually verify? (Optional but strengthens the audit trail.)
