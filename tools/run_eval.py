#!/usr/bin/env python3
"""
run_eval.py - Orchestrator over tools/eval_runner.py.

Fans out one full eval pass across (tasks, models, temperatures,
rule_states). Enforces a fail-fast budget cap so a runaway loop can't
silently spend $500 in API credits. Emits a single JSONL file with one
record per call.

Profiles (CLI shorthand for common matrix combinations):

    --profile smoke      n=2, dry-run, all 5 tasks x 1 model x 1 temp x 2 rule-states
                         = 20 records. Free; used by CI on workflow_dispatch.
    --profile full       n=100, all 5 tasks x 5 SKUs x 2 temps x 2 rule-states
                         = 10 000 records. The v1.0 headline pass.
    --profile regression n=30, the publishability floor. Used between full passes.

Real providers are stubbed in v0.75 PREVIEW; --profile full + --no-dry-run
will fail with NotImplementedError from eval_runner. The pipeline shape is
final — the wire-call implementation lands in v1.0.

Usage:
    python tools/run_eval.py --profile smoke --out tests/eval/results/run-001.jsonl
    python tools/run_eval.py --profile full  --max-usd 500 --no-dry-run --out ...
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
import time
import uuid
from pathlib import Path

# Local import — tools/ is on sys.path when invoked from repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import eval_runner

PROFILES = {
    "smoke": {
        "tasks": ["01-ts-async-without-await", "02-python-mutable-default",
                  "03-react-key-missing", "04-sql-select-star", "05-rename-without-grep"],
        "models": [("dry_run", "dry-run-stub-1.0.0")],
        "temperatures": [0.0],
        "rule_states": ["with_rule", "without_rule"],
        "n": 2,
        "dry_run_forced": True,
    },
    "regression": {
        "tasks": ["01-ts-async-without-await", "02-python-mutable-default",
                  "03-react-key-missing", "04-sql-select-star", "05-rename-without-grep"],
        "models": [
            ("anthropic", "claude-sonnet-4-5-20251022"),
            ("openai",    "gpt-4o-2024-08-06"),
            ("ollama",    "qwen2.5-coder:32b"),
        ],
        "temperatures": [0.0, 0.7],
        "rule_states": ["with_rule", "without_rule"],
        "n": 30,
        "dry_run_forced": False,
    },
    "full": {
        "tasks": ["01-ts-async-without-await", "02-python-mutable-default",
                  "03-react-key-missing", "04-sql-select-star", "05-rename-without-grep"],
        "models": [
            ("anthropic", "claude-opus-4-7-20260301"),
            ("anthropic", "claude-sonnet-4-5-20251022"),
            ("openai",    "gpt-4o-2024-08-06"),
            ("ollama",    "qwen2.5-coder:32b"),
            ("ollama",    "llama-3.1-8b-instruct"),
        ],
        "temperatures": [0.0, 0.7],
        "rule_states": ["with_rule", "without_rule"],
        "n": 100,
        "dry_run_forced": False,
    },
}


def estimate_pass_cost(profile_name: str) -> float:
    """Rough upper-bound USD estimate for a full pass of the named profile.

    Used as a pre-flight gate so --max-usd has a number to compare against
    before any API call lands.
    """
    p = PROFILES[profile_name]
    if p["dry_run_forced"]:
        return 0.0
    book, _ = eval_runner.load_pricebook()
    n_cells = len(p["tasks"]) * len(p["models"]) * len(p["temperatures"]) * len(p["rule_states"])
    n_calls = n_cells * p["n"]
    # Assume 800 in, 400 out per call as an upper-bound shape.
    in_tok, out_tok = 800, 400
    # Use the most expensive model in the profile as the cost ceiling.
    rates = []
    for prov, sku in p["models"]:
        key = f"{prov}/{sku}"
        if key in book:
            rates.append(book[key])
    if not rates:
        return 0.0
    max_rate = max(rates, key=lambda r: r["input_per_mtok"] + r["output_per_mtok"])
    per_call = (in_tok * max_rate["input_per_mtok"] + out_tok * max_rate["output_per_mtok"]) / 1_000_000
    return n_calls * per_call


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Orchestrate a full eval pass.")
    parser.add_argument("--profile", choices=list(PROFILES.keys()), required=True)
    parser.add_argument(
        "--out", default=None,
        help="JSONL output path (default: tests/eval/results/run-<id>.jsonl)",
    )
    parser.add_argument("--max-usd", type=float, default=5.0,
                        help="Fail-fast budget cap. Default 5 USD; smoke profile ignores it.")
    parser.add_argument("--no-dry-run", action="store_true",
                        help="Use real providers (requires API-key env vars). Default: dry-run.")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args(argv)

    profile = PROFILES[args.profile]
    # Respect profile dry-run forcing; smoke is always dry-run.
    dry_run = profile["dry_run_forced"] or not args.no_dry_run

    # Budget pre-flight (skip for dry-run).
    if not dry_run:
        est = estimate_pass_cost(args.profile)
        if est > args.max_usd:
            print(
                f"refusing to start: estimated upper-bound cost ${est:.2f} > "
                f"--max-usd ${args.max_usd:.2f}. Bump --max-usd or pick a smaller profile.",
                file=sys.stderr,
            )
            return 2
        print(f"pre-flight estimate: ${est:.2f} (cap ${args.max_usd:.2f}). proceeding.")

    run_id = args.run_id or uuid.uuid4().hex[:16]
    out_path = Path(args.out) if args.out else (
        eval_runner.ROOT / "tests" / "eval" / "results" / f"run-{run_id}.jsonl"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    n_records = 0
    total_cost = 0.0
    t0 = time.monotonic()
    with out_path.open("w", encoding="utf-8") as f:
        for task_id in profile["tasks"]:
            task = eval_runner.load_task(task_id)
            for provider, model_sku in profile["models"]:
                for temp in profile["temperatures"]:
                    for rule_state in profile["rule_states"]:
                        spec = eval_runner.ModelSpec(
                            provider=provider if not dry_run else "dry_run",
                            model_sku=model_sku,
                            temperature=temp,
                            max_tokens=1024,
                            top_p=1.0,
                        )
                        results = eval_runner.run_task(
                            task, spec, profile["n"], rule_state, run_id, dry_run=dry_run,
                        )
                        for r in results:
                            f.write(json.dumps(dataclasses.asdict(r), ensure_ascii=False) + "\n")
                            n_records += 1
                            total_cost += r.cost_usd
                            if not dry_run and total_cost > args.max_usd:
                                print(
                                    f"budget exhausted at ${total_cost:.2f} > "
                                    f"--max-usd ${args.max_usd:.2f}. aborting.",
                                    file=sys.stderr,
                                )
                                return 3
    elapsed = time.monotonic() - t0
    try:
        display_path = out_path.relative_to(eval_runner.ROOT)
    except ValueError:
        display_path = out_path
    print(
        f"wrote {n_records} records to {display_path} "
        f"in {elapsed:.1f}s (total cost ${total_cost:.4f}, "
        f"profile={args.profile}, dry_run={dry_run})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
