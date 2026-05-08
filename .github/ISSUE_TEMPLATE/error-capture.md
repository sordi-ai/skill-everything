---
name: "Document an Error"
about: "Document a mistake made by the agent"
title: "[Error] "
labels: ["bug", "error-capture"]
---

## What Happened?
[Concrete description of the error]

## Context
[In what situation? Which project or module?]

## Root Cause
[Why did it happen? What incorrect assumption was made?]

## Proposed Rule
[Action directive: "Always X before Y" or "Never Z without W"]

## Affected Sub-Skill
[Which file should the rule go into? e.g. references/development/code-quality.md]

## Severity
- [ ] Critical (data loss, security vulnerability)
- [ ] High (production outage, performance issue)
- [ ] Medium (incorrect behavior, extra rework)
- [ ] Low (cosmetic, style violation)
