#!/usr/bin/env python3
"""
compare_eval.py - Compare a reproduction JSONL run against the curated
                  baseline. Reports per-cell Re-Mistake-Rate divergences
                  above the tolerance threshold (default +/-0.10 absolute).

This is the v1.0 reproducibility gate. Per the methodology contract in
tests/eval/README.md, any future re-run from the pinned prompts must
produce a Re-Mistake-Rate within +/-10 percentage points absolute of the
baseline for every comparable cell.

Cell key: (task_id, model_sku, temperature). Re-Mistake-Rate per cell:
    rmr = P(mistake | with_rule) / P(mistake | without_rule)

Cells where one side lacks both rule_states are skipped (not failures).
Cells where without_rule mistake_rate == 0 are skipped (RMR is undefined).

Usage:
    python tools/compare_eval.py baseline.jsonl rerun.jsonl
    python tools/compare_eval.py baseline.jsonl rerun.jsonl --tolerance 0.10

Exit codes:
    0  all comparable cells within tolerance
    1  one or more cells diverge beyond tolerance
    2  inputs missing / malformed
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _aggregate(jsonl_path: Path) -> dict[tuple[str, str, float, str], dict[str, float | int]]:
    """Aggregate JSONL records into per-(task, model, temp, rule_state) cells.

    Skips records with status != "ok" (errors don't count toward the rate).
    Returns {cell_key: {"n": int, "mistake_rate": float}}.
    """
    bucket: dict[tuple[str, str, float, str], list[bool]] = defaultdict(list)
    with jsonl_path.open(encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("status") != "ok":
                continue
            key = (
                rec["task_id"],
                rec["model_sku"],
                float(rec["temperature"]),
                rec["rule_state"],
            )
            bucket[key].append(bool(rec["criterion_pass"]))
    out: dict[tuple[str, str, float, str], dict[str, float | int]] = {}
    for key, passes in bucket.items():
        n = len(passes)
        out[key] = {"n": n, "mistake_rate": 1.0 - sum(passes) / n}
    return out


def _re_mistake_rate(
    cells: dict[tuple[str, str, float, str], dict[str, float | int]],
    task_id: str,
    model_sku: str,
    temperature: float,
) -> tuple[float, int, int] | None:
    """Return (rmr, n_with, n_without) for a (task, model, temp) cell, or
    None if either rule_state is missing or without_rule mistake_rate == 0."""
    w_key = (task_id, model_sku, temperature, "with_rule")
    wo_key = (task_id, model_sku, temperature, "without_rule")
    if w_key not in cells or wo_key not in cells:
        return None
    with_rate = float(cells[w_key]["mistake_rate"])
    without_rate = float(cells[wo_key]["mistake_rate"])
    if without_rate == 0:
        return None
    return with_rate / without_rate, int(cells[w_key]["n"]), int(cells[wo_key]["n"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare a reproduction JSONL against the curated baseline.",
    )
    parser.add_argument("baseline", type=Path, help="The curated baseline JSONL.")
    parser.add_argument("rerun", type=Path, help="The reproduction JSONL.")
    parser.add_argument(
        "--tolerance", type=float, default=0.10,
        help="Maximum absolute Re-Mistake-Rate divergence per cell (default 0.10).",
    )
    parser.add_argument(
        "--min-n", type=int, default=30,
        help="Minimum sample count per cell to count toward comparison (default 30).",
    )
    args = parser.parse_args(argv)

    if not args.baseline.exists():
        print(f"missing: {args.baseline}", file=sys.stderr)
        return 2
    if not args.rerun.exists():
        print(f"missing: {args.rerun}", file=sys.stderr)
        return 2

    base = _aggregate(args.baseline)
    rerun = _aggregate(args.rerun)

    # Walk every (task, model, temp) triple that appears in the baseline.
    base_triples: set[tuple[str, str, float]] = {
        (t, m, temp) for (t, m, temp, _state) in base
    }

    matched: list[tuple[str, str, float, float, float, float, int, int]] = []
    diverging: list[tuple[str, str, float, float, float, float, int, int]] = []
    skipped_missing: list[tuple[str, str, float]] = []
    skipped_low_n: list[tuple[str, str, float, int]] = []

    for triple in sorted(base_triples):
        base_rmr = _re_mistake_rate(base, *triple)
        rerun_rmr = _re_mistake_rate(rerun, *triple)
        if base_rmr is None or rerun_rmr is None:
            skipped_missing.append(triple)
            continue
        b_rmr, b_nw, b_nwo = base_rmr
        r_rmr, r_nw, r_nwo = rerun_rmr
        min_n_observed = min(b_nw, b_nwo, r_nw, r_nwo)
        if min_n_observed < args.min_n:
            skipped_low_n.append((*triple, min_n_observed))
            continue
        delta = abs(b_rmr - r_rmr)
        row = (*triple, b_rmr, r_rmr, delta, b_nw, r_nw)
        if delta > args.tolerance:
            diverging.append(row)
        else:
            matched.append(row)

    # --- output ---
    if matched:
        print(f"matched ({len(matched)} cells within ±{args.tolerance:.2f}):")
        for task, sku, temp, b_rmr, r_rmr, delta, b_nw, r_nw in matched:
            print(
                f"  ✓ {task} / {sku} / T={temp:.1f}"
                f"  base={b_rmr:.3f}  rerun={r_rmr:.3f}  Δ={delta:.3f}"
                f"  (n_with: base={b_nw}, rerun={r_nw})"
            )

    if diverging:
        print(f"\nDIVERGING ({len(diverging)} cells, tolerance ±{args.tolerance:.2f}):")
        for task, sku, temp, b_rmr, r_rmr, delta, b_nw, r_nw in diverging:
            print(
                f"  ✗ {task} / {sku} / T={temp:.1f}"
                f"  base={b_rmr:.3f}  rerun={r_rmr:.3f}  Δ={delta:.3f}"
                f"  (n_with: base={b_nw}, rerun={r_nw})"
            )

    if skipped_missing:
        print(f"\nskipped — one side missing rule_state ({len(skipped_missing)}):")
        for task, sku, temp in skipped_missing:
            print(f"  - {task} / {sku} / T={temp:.1f}")

    if skipped_low_n:
        print(f"\nskipped — n < --min-n={args.min_n} ({len(skipped_low_n)}):")
        for task, sku, temp, n in skipped_low_n:
            print(f"  - {task} / {sku} / T={temp:.1f}  (min cell n={n})")

    total_comparable = len(matched) + len(diverging)
    if diverging:
        print(
            f"\nFAIL: {len(diverging)} of {total_comparable} comparable cells diverge "
            f"beyond ±{args.tolerance:.2f}",
            file=sys.stderr,
        )
        return 1
    if total_comparable == 0:
        print(
            "\nNO COMPARABLE CELLS: every cell was skipped (missing rule_state, "
            "low n, or without_rule mistake_rate of 0). Cannot certify reproduction.",
            file=sys.stderr,
        )
        return 1
    print(f"\nclean: all {total_comparable} comparable cells within ±{args.tolerance:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
