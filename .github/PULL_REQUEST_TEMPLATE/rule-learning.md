<!--
Use this template when adding a rule from a real observed mistake.
Title: learn(errors): ERR-YYYY-NNN — <short>
Label: needs-rule-review
The auto-approve-rule-pr workflow gates merge on:
  1. Diff scope is references/errors/** only
  2. Head commit carries a Co-Authored-By: trailer
-->

## Error reference

`ERR-YYYY-NNN`

## What did the agent do wrong?

<!-- One paragraph, with a code snippet if relevant. Redact paths,
     customer IDs, secrets BEFORE pasting. -->

## Why did it happen?

<!-- The false assumption. The cognitive shortcut. The missing context. -->

## Impact (real, not theoretical)

<!-- What was the actual cost? Time wasted? CI minutes? Customer impact?
     If you'd write "no impact" — was it really an error? -->

## Proposed rule

```
[Always|Never|Before|After|Prefer|Avoid|Use|Do|Ensure] <action directive>
```

Target file: `references/<category>/<filename>.md`

## Has a similar error been logged before?

- [ ] I searched `references/errors/error-log.md` for similar entries.
- [ ] If a similar entry exists, I incremented `count` instead of opening a new entry.
- [ ] If it's truly new, the next sequential `ERR-YYYY-NNN` is used.

## Self-review

- [ ] CI `lint-rules` passes locally (`python tools/validate_rules.py`)
- [ ] The `new_rule` starts with one of the allowed verbs
- [ ] No URLs, shell binaries, credential paths, or `<script>` tags in the rule (or, if needed, an `exceptions.yml` entry with rationale is included)
- [ ] An eval task in `tests/eval/tasks/` exists that would have caught this mistake (or a follow-up issue is linked)
- [ ] The `Co-Authored-By:` trailer is present in the head commit

## Maintainer review checklist (do not check yourself)

- [ ] Schema and lint validators pass in CI
- [ ] Rule wording survives "what would Sven say on HN" reading
- [ ] No PII / secrets in the entry body
- [ ] If `count > 1`: rationale is convincing, not statistical noise
