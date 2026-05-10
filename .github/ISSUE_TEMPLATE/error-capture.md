---
name: "Document an Error"
about: "Document a mistake made by the agent"
title: "[Error] "
labels: ["bug", "error-capture"]
---

> **Redaction reminder.** Before pasting logs, stack traces, or code:
> - Redact API keys, JWTs, customer IDs, internal hostnames, file paths from your home directory.
> - Once committed, `git revert` does NOT remove a secret from history. You will need `git filter-repo` and a force-push (see SECURITY.md → "Recovery runbook").

## What Happened?
[Concrete description of the error. Code snippet if relevant — redacted.]

## Context
[In what situation? Which project or module?]

## Root Cause
[Why did it happen? What incorrect assumption was made?]

## Proposed Rule
[Action directive: "Always X before Y" or "Never Z without W"]

## Affected Sub-Skill
[Which file should the rule go into? e.g. skills/code-quality/SKILL.md]

## Severity
- [ ] Critical (data loss, security vulnerability)
- [ ] High (production outage, performance issue)
- [ ] Medium (incorrect behavior, extra rework)
- [ ] Low (cosmetic, style violation)
