# errors-bench — eval framework

The framework that measures whether the rules committed to
`skills/error-log/SKILL.md` actually prevent the mistakes they claim to
prevent. The `v1.0` stable tag ships only when the numbers below
satisfy the acceptance criteria; until then the project label is
`v0.75 PREVIEW`.

## What it measures

**Re-Mistake-Rate**, defined per cell as:

```
re_mistake_rate = P(mistake | with_rule) / P(mistake | without_rule)
```

Lower is better. `0.0` means the rule fully prevented the mistake;
`1.0` means the rule had no effect; `>1.0` means the rule made things
worse (legitimate outcome worth knowing).

A *cell* is `(task, model, temperature)`. A *Re-Mistake-Rate publication*
quotes a per-cell point estimate plus a 95 % CI, alongside an aggregate
macro-average across model SKUs.

## Methodology contract

Every published number ships with all of the following or it is not
published.

### Sample size & power

| Knob | Floor | Headline |
|---|---|---|
| `n` per cell | ≥ 50 | ≥ 100 |
| Cells per task | 2 rule-states × 2 temperatures × 5 model SKUs = 20 | 20 |
| Total calls per full pass | 5 tasks × 20 cells × 50 samples = **5 000** | 10 000 |

- **CI per cell:** Wilson score 95 %; Clopper–Pearson exact only for
  zero-mistake cells where Wilson under-states uncertainty.
- **CI on the ratio:** bootstrap 95 % (10 000 resamples, BCa).
- **Minimum detectable effect** at n = 50 per cell: ≈ 19 percentage
  points absolute. At n = 100: ≈ 14 pp. The methodology contract uses
  n = 50 as the *publishability* floor and n = 100 for the *headline*
  claim that gates the `v1.0` promotion.

### Multi-model dimension

Reported per-model first; macro-average across model SKUs (each model
weighted equally) is the secondary headline. Never a micro-average
across runs — that biases toward whichever model we sampled most.

The pinned v1.0 model SKUs are dated revisions, not floating tags:

| Slot | SKU |
|---|---|
| Frontier-Anthropic | `claude-opus-4-7-20260301` |
| Workhorse-Anthropic | `claude-sonnet-4-5-20251022` |
| Cross-vendor | `gpt-4o-2024-08-06` |
| Open-weights large | `qwen2.5-coder:32b@<digest>` |
| Open-weights small | `llama-3.1-8b-instruct@<digest>` |

A bare `gpt-4o` is forbidden because OpenAI silently rotates the
underlying weights. If a vendor deprecates an SKU, the cell becomes
*frozen historical* — we do not re-quote it as current; we add a
footnote and re-run on the successor SKU.

### Prompt-hash-pinning

`prompt_canon_hash` is SHA-256 over the byte concatenation of these
ten fields, in this exact order, UTF-8-encoded with `\n` separators:

1. `task_id`
2. `task_yml_sha256` (SHA-256 of the raw bytes of `tasks/<task_id>.yml`)
3. `rule_state` (`with_rule` | `without_rule`)
4. `system_prompt` (verbatim bytes; empty string if none)
5. `user_prompt` (verbatim bytes, after rule injection if `with_rule`)
6. `model_sku` (the dated string from above)
7. `temperature` (formatted `%.3f`)
8. `max_tokens` (decimal int as string)
9. `top_p` (formatted `%.3f`; explicit default if not set)
10. `harness_version` (semver of `tools/eval_runner.py`)

`task_yml_sha256` binds the pass/fail criterion to the hash. If the
regex is edited, the hash changes, and historical numbers cannot be
silently re-used.

### Pass/fail criterion tiers

Declared per task in the YAML.

| Tier | Detection | Used by |
|---|---|---|
| **1** | Deterministic regex / regex_negative | Most code-output tasks (01, 03, 04) |
| **2** | AST + structural check | Tasks needing semantic confirmation (02) |
| **3** | Model-judge fallback | Process-output tasks (05) |

Tier 3 requirements:

- `judge_rubric` in the task YML, bound by `task_yml_sha256`.
- Pinned judge SKU (dated string, recorded as `judge_model_sku`).
- Calibration corpus at `tasks/<task_id>-judge-calibration.jsonl`:
  10 known-pass + 10 known-fail handwritten responses.
- Every run measures the judge's accuracy on the calibration set first;
  if `judge_calibration_accuracy < 0.90`, **the run is invalid** and the
  headline number cannot be quoted.

### Determinism claim

The harness records `prompt_canon_hash` (inputs are bit-reproducible)
and the observed response distribution (outputs are statistically
reproducible at `n ≥ 30`). The honest claim is:

> Bit-reproducible inputs, statistically reproducible outputs.

We do not claim "re-run produces identical bytes." We claim "re-run
produces a statistically indistinguishable distribution at n ≥ 30."
A future re-run from the pinned hashes reproduces every cell's
`criterion_pass` rate within seed-noise (Tier-1/2: exact match;
Tier-3: judge agreement ≥ 0.95).

## Output schema

One JSONL record per provider call. The full record fields are
specified in `schemas/eval-result.json` and enforced by
`tools/validate_eval_results.py`. Every field is mandatory for a
record to count toward a published number.

## Acceptance criteria for v1.0 promotion

The `v1.0` stable tag ships when, against the pinned 5-task corpus,
on all 5 model SKUs, at temperatures 0.0 and 0.7, with **n = 100 per
cell**:

1. **Aggregate macro-Re-Mistake-Rate ≤ 0.40** (mean of per-model
   Re-Mistake-Rates, each model weighted equally) with a bootstrap
   95 % CI upper bound ≤ 0.55. Translation: rules cut mistakes by at
   least 45 %, and we are 95 % confident the true cut is at least 30 %.
2. **Per-model floor:** no individual model has Re-Mistake-Rate ≥ 0.80
   on the macro across tasks. If a model can't use the rule, we say so
   and exclude it explicitly rather than hide it in the macro.
3. **Tier-3 judge gate:** every Tier-3 task in the run has
   `judge_calibration_accuracy ≥ 0.90`. Otherwise the run is invalid.
4. **Reproducibility certificate:** every JSONL row carries
   `prompt_canon_hash`; a re-run of any 10 randomly-sampled rows
   reproduces the original `criterion_pass` within seed-noise (Tier-1/2:
   exact match; Tier-3: judge agreement ≥ 0.95).

### Cost reality

A full headline pass (n = 100): 5 tasks × 2 rule-states × 5 models ×
2 temperatures × 100 samples = **10 000 calls**. At a blended
~$0.05/call (Sonnet + Opus + GPT-4o + open-weights), one pass is
**~$500**. The publishability floor (n = 50) cuts this to ~$250. The
v1.0 headline is a ~$500 measurement, not a free one — budget caps in
`tools/run_eval.py` enforce this explicitly.

## Tasks (Phase 1: 5 of 5 defined)

| ID | Mistake | Tier | Rule it tests |
|---|---|---|---|
| `01-ts-async-without-await` | Returning a Promise instead of awaited value | 1 | Always await async calls before return |
| `02-python-mutable-default` | `def f(x=[])` mutable default | 2 | Never use mutable default arguments |
| `03-react-key-missing` | Mapping over a list without `key` prop | 1 | Always add a stable key in list rendering |
| `04-sql-select-star` | `SELECT *` without LIMIT or projection | 1 | Never SELECT * for paginated lists |
| `05-rename-without-grep` | Rename complete after only-local tests | 3 | After any rename, project-wide grep before claiming done (ERR-2026-007) |

Task definitions live in `tasks/*.yml` and validate against
`schemas/eval-task.json` on every PR.

## Honest current state (v0.75 PREVIEW)

- Tasks defined: 5 of 5.
- Methodology contract: published in this file, schema-validated.
- Schemas defined: `schemas/eval-task.json`, `schemas/eval-result.json`.
- Harness: `tools/eval_runner.py` runs end-to-end in **dry-run mode**;
  real provider calls are stubbed pending v1.0-readiness build-out.
- Pricebook: `pricebook.yml` versioned.
- Validator: `tools/validate_eval_results.py` enforces the JSONL contract.
- CI: `.github/workflows/eval.yml` runs the dry-run smoke profile on
  workflow_dispatch (manual trigger; no API budget impact).
- Reproducibility runbook: `docs/eval-reproduction.md`.
- Automated runner with real providers: **deferred to v1.0**.
- Published Re-Mistake-Rate in README: **none** until the v1.0
  acceptance criteria are met against n = 100 per cell.

If the README ever claims a Re-Mistake-Rate before this section says
"Automated runner with real providers: yes", file an issue. We will be
wrong.

## Files

```
tests/eval/
├── README.md                                  # this file
├── pricebook.yml                              # versioned per-million-token rates
├── tasks/                                     # 5 task fixtures
│   └── 0[1-5]-*.yml
└── results/                                   # populated at promotion
    ├── .gitignore                             # ignore run-*.jsonl
    └── baseline.jsonl                         # the curated v1.0 baseline (when promoted)

schemas/
├── eval-task.json                             # task YML contract
└── eval-result.json                           # JSONL output contract

tools/
├── eval_runner.py                             # the harness (Mira)
├── run_eval.py                                # orchestrator (Kai)
├── validate_eval_results.py                   # JSONL validator
├── render_eval_table.py                       # README integration at promotion
└── compare_eval.py                            # baseline-vs-rerun ±10% comparator

docs/
└── eval-reproduction.md                       # third-party reproduction runbook

.github/workflows/
└── eval.yml                                   # workflow_dispatch + smoke cron
```
