# errors-bench (skeleton)

A small evaluation harness for measuring whether the rules committed to
`references/errors/error-log.md` actually prevent the mistakes they claim
to prevent.

## Why this exists

The killer pre-launch hostile-reader question:

> "Re-Mistake-Rate < 20 % after rule" — compared to what baseline? On what
> model? n = 3 isn't an evaluation, it's a vibe check.

Right. This skeleton is the bare minimum a Phase 2 launch needs to
ship before claiming Re-Mistake-Rate numbers. **Until this evolves into a
running tool, the README does not claim a Re-Mistake-Rate.**

The skeleton exists in the main repo so reviewers can see the
methodology. The actual eval runner — automated against the Anthropic /
Google / OpenAI APIs with cost tracking — moves to its own repo
`errors-bench` when Phase 2 starts (see [Versions](../../README.md#versions)).

## What it measures

**Re-Mistake-Rate**, defined per task as:

```
re_mistake_rate = P(mistake_with_rule) / P(mistake_without_rule)
```

Lower is better. 0.0 means the rule fully prevented the mistake;
1.0 means the rule had no effect.

For each task we define:

- A coding prompt that has historically triggered the mistake.
- The expected mistake signature (a regex or AST query against the
  generated code).
- The rule that should prevent the mistake (a real entry from
  `references/errors/error-log.md`).
- A "with rule" prompt that includes the rule in context, and a
  "without rule" prompt that doesn't.

## Methodology contract

When this becomes a running tool, every published number must include:

| Dimension | Value to report |
|---|---|
| n per cell | ≥ 30 (no n=3 vibe checks) |
| Models | At least Claude Sonnet, GPT-4-class, and one open-weights model |
| Temperature | 0.0 and 0.7 reported separately (rules behave differently under sampling) |
| Prompt hash | SHA-256 of the exact prompt incl. rule for reproducibility |
| Pass/fail criterion | The mistake-detector regex / AST query, versioned alongside the task |

Without all five, a Re-Mistake-Rate is a vibe check. SECURITY.md and
README link here so the contract is public.

## Tasks (Phase 1: skeleton only)

| ID | Mistake | Rule it tests |
|---|---|---|
| `01-ts-async-without-await` | Returning a Promise instead of awaited value | `Always await async calls before return` |
| `02-python-mutable-default` | `def f(x=[])` mutable default | `Never use mutable default arguments` |
| `03-react-key-missing` | Mapping over a list without `key` prop | `Always add a stable key in list rendering` |
| `04-sql-select-star` | `SELECT *` without LIMIT or projection | `Never SELECT * for paginated lists` |
| `05-rename-without-grep` | Rename complete after only-local tests | `After any rename, project-wide grep before claiming done` (ERR-2026-007) |

The task definitions live in `tasks/*.yml`. Run them by hand for now;
copy the prompt into your editor of choice and inspect the output
against the mistake regex. Manual is fine in Phase 1 — what matters is
that the methodology is documented and reproducible.

## Honest current state (Phase 1)

- Tasks defined: 5 of planned 5.
- Prompt hashes pinned: yes.
- Mistake-detection regex / AST: defined.
- Automated runner: **not yet** — manual at this stage.
- Reported Re-Mistake-Rate in README: **none** until Phase 2 produces n ≥ 30 per cell.
- Repo split-out: planned for Phase 2 launch.

If the README ever claims a Re-Mistake-Rate before this section says
"Automated runner: yes", file an issue. We will be wrong.
