---
id: error-log
version: 1.0.0
tokens_target: 1500
triggers:
  - made or corrected a mistake
  - learn from this
loads_after: []
supersedes: []
---

# Sub-Skill: Error Log
<!-- target: ~1500 tokens (grows with entries) -->

**Purpose:** Central memory for all mistakes the agent has made or observed. Each entry prevents the same mistake from happening twice. Validated by [`tools/validate_rules.py`](../../tools/validate_rules.py) against [`schemas/error-entry.json`](../../schemas/error-entry.json) on every PR.

---

## Format specification

Every error entry follows this YAML format. The schema is enforced — see [`schemas/error-entry.json`](../../schemas/error-entry.json) for the canonical definition.

```yaml
- id: ERR-YYYY-NNN          # Year + sequential number, e.g. ERR-2026-001
  date: YYYY-MM-DD
  last_seen: YYYY-MM-DD     # Last occurrence (update on repeat)
  count: 1                   # How many times this error has occurred
  category: development|git|deployment|security|performance|domain
  severity: critical|high|medium|low
  context: |
    [1-3 sentences: in what situation did the error occur?
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
    Phrased as action directive: "Always X before Y" or "Never Z without W".
    Must start with: Always, Never, Before, After, Prefer, Avoid, Use, Do, or Ensure.]
  target_file: references/[category]/[filename].md
```

---

## Entries

```yaml
errors:

  - id: ERR-2026-001
    date: 2026-04-12
    last_seen: 2026-04-12
    count: 1
    category: development
    severity: high
    context: |
      Adding type-safe API call wrappers to a TypeScript project. tsconfig
      has strictNullChecks enabled. The agent was generating a quick demo
      function, saw a tsc error about possibly-undefined returns, and
      flipped strictNullChecks off in the local file via a triple-slash
      directive to make the demo green.
    what_happened: |
      Agent added a per-file directive disabling strictNullChecks because
      the demo function "didn't need to handle the null path". Locally tsc
      was clean. CI runs the project tsc against the whole tree and the
      directive bled into a downstream import path that did rely on
      strictness. CI failed on a file the agent never touched.
    root_cause: |
      False assumption that "disable a strict check just for this demo"
      is local. In TypeScript, lib-mode and per-file directives interact
      with project graph in non-obvious ways.
    impact: |
      Two CI runs lost. Reviewer reverted the directive. ~25 minutes wasted.
    resolution: |
      Removed the directive, added a real null-check, demo now handles
      both paths.
    new_rule: |
      Never disable strict type-checks "just for this file" to make a demo
      green. Either handle the null path or document why the value is
      provably non-null with a comment.
    target_file: references/development/typescript.md

  - id: ERR-2026-007
    date: 2026-04-21
    last_seen: 2026-04-29
    count: 2
    category: development
    severity: medium
    context: |
      Renaming a public utility function inside a TypeScript monorepo. The
      function was used in 17 places across 5 packages.
    what_happened: |
      Agent renamed the function in the source file and the directly
      adjacent test file, ran the local tests, saw green, and reported the
      rename complete. Four imports in two other packages still referenced
      the old name; tsc passed locally because the agent only watched the
      source package. CI caught the drift.
      The same mistake repeated 8 days later on a different rename in a
      different package — increment of count rather than a new entry.
    root_cause: |
      Treating "tests green here" as proof of "rename complete everywhere".
      In a monorepo, local tsc/test scope hides cross-package refs.
    impact: |
      First occurrence: 35 minutes lost. Second occurrence: caught in
      pre-merge CI before review, ~10 minutes lost.
    resolution: |
      Added a project-wide ripgrep step to the rename checklist:
      `rg -F '<old name>' --type ts` before claiming done.
    new_rule: |
      After any rename, run a project-wide grep for the old name before
      claiming the rename is complete. In monorepos, local tsc scope is
      not enough.
    target_file: references/development/code-quality.md

  - id: ERR-2026-012
    date: 2026-05-04
    last_seen: 2026-05-04
    count: 1
    category: deployment
    severity: high
    context: |
      Deploying a new version of an internal billing service. Release
      notes mentioned a database migration. Agent had access to the
      deploy runbook and ran the deploy command first.
    what_happened: |
      Agent ran `kubectl rollout restart` against the new image before
      running the migration job. The new image expected a column that
      didn't exist yet; the readiness probes failed for ~90 seconds until
      the migration job was completed manually.
    root_cause: |
      The runbook was implicit about ordering ("there's a migration in
      this release"). The agent assumed migrations run as part of the
      pod startup. They don't — they're a separate Job in this project's
      Helm chart.
    impact: |
      90 seconds of failing readiness probes. No data loss. Two billing
      requests retried automatically by the upstream caller. No customer-
      visible impact, but the on-call engineer was paged.
    resolution: |
      Manually triggered the migration Job, waited for completion, then
      re-rolled the deployment. Updated the runbook to say "always run
      the migration Job to completion before any rollout".
    new_rule: |
      Before any deployment that includes a database migration, run the
      migration job to completion first. Do not rely on pod startup to
      apply migrations.
    target_file: references/process/review-deployment.md

  - id: ERR-2026-013
    date: 2026-05-10
    last_seen: 2026-05-10
    count: 1
    category: development
    severity: low
    context: |
      Running tools/render_loaders.py via Docker on a Windows host (Git
      Bash / MSYS environment) to validate render-drift without local
      Python. Repo path was a Windows-style absolute path.
    what_happened: |
      Agent ran `docker run --rm -v "$(pwd):/repo" -w /repo python:3.12`
      from inside Git Bash. Docker exited with: "Error response from
      daemon: the working directory 'C:/Program Files/Git/repo' is
      invalid, it needs to be an absolute path". MSYS had auto-converted
      the Linux-style /repo path to a Windows-style "C:/Program Files/
      Git/repo" before passing it to docker.exe.
    root_cause: |
      MSYS / Git Bash on Windows aggressively converts unquoted Linux
      paths to Windows paths when calling native binaries. Bind-mount
      arguments to docker.exe pass through this layer and get mangled.
      The agent assumed the path syntax that works in plain bash also
      works in Git Bash unmodified.
    impact: |
      One minute lost re-typing the command. No data loss. Confused
      error message that initially looked like a docker volume issue.
    resolution: |
      Re-ran the command with MSYS_NO_PATHCONV=1 prefix:
      `MSYS_NO_PATHCONV=1 docker run --rm -v "<repo-root>:/repo" ...`
      Plus quoted the volume mount with explicit Windows-style absolute
      path on the host side.
    new_rule: |
      Always prefix `docker run -v` calls from Git Bash / MSYS on Windows
      with `MSYS_NO_PATHCONV=1` to disable automatic path conversion.
      Use explicit Windows-style paths on the host side of bind-mounts.
    target_file: references/development/code-quality.md
```

---

## Consolidation

When this file exceeds 50 entries:

1. Merge errors with the same root cause into one entry (increase `count`).
2. Archive entries older than 6 months with `severity: low`.
3. Rules derived from errors remain in their respective sub-skills.

See [`self-extension-workflow.md`](./self-extension-workflow.md) for the full procedure.
