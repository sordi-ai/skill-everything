# Eval reproduction runbook

This is the runbook that lets a third party reproduce a published
Re-Mistake-Rate number within ±10 percentage points absolute against
the baseline. The procedure is bit-pinned at the input layer
(canonical SHA-256 prompt hash) and statistically reproducible at the
output layer (n ≥ 50 per cell).

> **Until `tests/eval/results/baseline.jsonl` is committed**, no
> Re-Mistake-Rate is published in the README. This runbook documents
> the procedure that will be used at v1.0 promotion. The eval framework
> itself is wired and runs end-to-end in dry-run mode on every push
> (see `.github/workflows/eval.yml`).

## What this reproduces

For every (task, model, temperature, rule_state) cell in the baseline:

- The exact prompt the model received (`prompt_canon_hash` matches byte-for-byte).
- The provider response (statistically, at n ≥ 50).
- The pass/fail verdict (deterministic for Tier-1/2; judge-agreement ≥ 0.95 for Tier-3).
- The aggregate Re-Mistake-Rate within ±10 % absolute of the published value.

## What this does NOT reproduce

- The exact bytes of any single sample. Providers are not deterministic
  at `temperature=0`; only the distribution at `n ≥ 50` is statistically
  stable. See the [methodology contract](../tests/eval/README.md#determinism-claim).
- Cost. Provider pricing changes; the `cost_usd` recorded in the baseline
  is historical. Re-runs are costed against the current `pricebook.yml`.

## Prerequisites

- Git + Docker (or Python ≥ 3.10 + pip).
- API keys for at least the providers covered in the baseline cell you
  want to reproduce. Single-provider reruns are supported (reproduces
  only that provider's rows).
- Budget. The publishability floor (n = 50) is ~$250 for a full
  multi-provider rerun; n = 100 headline is ~$500. Single-cell reruns
  are dollars or less.

## Procedure

### 1. Clone at the exact tag

```bash
git clone https://github.com/sordi-ai/skill-everything.git
cd skill-everything
git checkout v0.75.0    # or the tag the baseline was promoted under
```

### 2. Read the baseline header

```bash
head -1 tests/eval/results/baseline.jsonl
```

Records carry `run_id`, `commit_sha` (the tag commit), `harness_version`,
`prompt_canon_hash` per row, and a footer aggregate record. Spot-check
that `commit_sha` matches `git rev-parse HEAD`.

### 3. Set API keys + budget cap

```bash
export ANTHROPIC_API_KEY="sk-ant-..."     # required for Anthropic cells
export OPENAI_API_KEY="sk-..."            # required for OpenAI cells
export OLLAMA_HOST="http://localhost:11434"  # required for open-weights cells
export EVAL_MAX_USD="500"                 # match or exceed the baseline's cost
```

### 4. Reproduce via Docker (preferred)

```bash
docker run --rm \
  -v "$PWD/tests/eval/results:/out" \
  -e ANTHROPIC_API_KEY \
  -e OPENAI_API_KEY \
  -e OLLAMA_HOST \
  -e EVAL_MAX_USD \
  ghcr.io/sordi-ai/skill-everything-eval:v0.75.0 \
    --profile full \
    --no-dry-run \
    --out /out/rerun.jsonl
```

Or run locally:

```bash
pip install -e ".[dev,eval]"
python tools/run_eval.py --profile full --no-dry-run \
    --max-usd "$EVAL_MAX_USD" \
    --out tests/eval/results/rerun.jsonl
```

### 5. Compare against the baseline

```bash
python tools/compare_eval.py \
    tests/eval/results/baseline.jsonl \
    tests/eval/results/rerun.jsonl \
    --tolerance 0.10
```

Exit 0 means every cell's Re-Mistake-Rate is within ±10 percentage
points absolute of the baseline. Exit 1 prints the cells that diverge.

> `compare_eval.py` is the v1.0 promotion artefact. It is currently a
> stub; the comparator implementation lands alongside the first real
> baseline.

## Single-provider reruns

The baseline JSONL is partition-friendly. Reproduce only the cells you
have keys for:

```bash
# Anthropic-only rerun:
python tools/run_eval.py \
    --profile regression --no-dry-run \
    --max-usd 50 \
    --out tests/eval/results/rerun-anthropic.jsonl
# (the regression profile already covers Anthropic + OpenAI + Ollama;
#  set OPENAI_API_KEY / OLLAMA_HOST to empty to skip those cells —
#  the harness records the skipped cells as status=provider_error)
```

## What success looks like

- `compare_eval.py` exits 0.
- Every cell with `n ≥ 50` reproduces within ±10 pp absolute.
- `prompt_canon_hash` matches byte-for-byte on every reproduced row.
- The aggregate macro-Re-Mistake-Rate is within ±5 pp of the baseline.

## What to do when reproduction fails

1. Confirm the tag matches: `git rev-parse HEAD` vs the baseline's `commit_sha`.
2. Confirm prompts match: every row's `prompt_canon_hash` should match
   the baseline's value for the same cell. If not, a SKILL.md or task
   YAML drifted since the tag — verify `git status`.
3. Confirm provider SKUs match. The methodology requires dated SKUs
   (e.g. `claude-sonnet-4-5-20251022`). A bare `claude-sonnet` is the
   floating tag and may have rotated weights.
4. If a Tier-3 task fails reproduction, check
   `judge_calibration_accuracy` — it must be ≥ 0.90 for the run to
   count.
5. Open a [security issue](../SECURITY.md#reporting-a-vulnerability) if
   the reproduction divergence looks like a methodology break. Otherwise
   a regular GitHub issue is fine.

## Related

- Methodology contract: [`tests/eval/README.md`](../tests/eval/README.md)
- Task fixtures: [`tests/eval/tasks/`](../tests/eval/tasks/)
- Pricebook: [`tests/eval/pricebook.yml`](../tests/eval/pricebook.yml)
- Result schema: [`schemas/eval-result.json`](../schemas/eval-result.json)
- Harness source: [`tools/eval_runner.py`](../tools/eval_runner.py)
- Orchestrator: [`tools/run_eval.py`](../tools/run_eval.py)
- Validator: [`tools/validate_eval_results.py`](../tools/validate_eval_results.py)
