#!/usr/bin/env python3
"""
render_eval_table.py - Render the RE-MISTAKE RATE table in README.md from
                       the curated baseline at tests/eval/results/baseline.jsonl.

Sibling to render_readme_table.py / render_loaders.py. Writes the Markdown
table between the markers:

    <!-- eval-table:start -->
    ...
    <!-- eval-table:end -->

Until tests/eval/results/baseline.jsonl is promoted (v1.0 acceptance
criteria met), the renderer emits a placeholder block citing the v0.75
PREVIEW state. The README never claims a Re-Mistake-Rate without a
curated baseline behind it — that's the honesty contract.

Usage:
    python tools/render_eval_table.py
    python tools/render_eval_table.py --check     # exit 1 on drift, no write
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
BASELINE = ROOT / "tests" / "eval" / "results" / "baseline.jsonl"
START = "<!-- eval-table:start -->"
END = "<!-- eval-table:end -->"


def _placeholder() -> str:
    return (
        "_The baseline measurement is in development. The `v1.0` stable tag "
        "ships only after [`tests/eval/results/baseline.jsonl`](./tests/eval/results/) "
        "is populated under the methodology contract in "
        "[`tests/eval/README.md`](./tests/eval/README.md). Until then this section "
        "stays empty by design — see the [v0.75 PREVIEW](./ROADMAP.md) versioning rationale._"
    )


def _table_from_baseline(baseline_path: Path) -> str:
    """Aggregate JSONL records into a per-cell Re-Mistake-Rate table."""
    # bucket[(task_id, model_sku, temp, rule_state)] = [(criterion_pass,...)]
    bucket: dict[tuple[str, str, float, str], list[bool]] = defaultdict(list)
    with baseline_path.open(encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            rec = json.loads(line)
            key = (rec["task_id"], rec["model_sku"], rec["temperature"], rec["rule_state"])
            bucket[key].append(bool(rec["criterion_pass"]))

    # Per (task, model, temp) compute Re-Mistake-Rate = mistake_with / mistake_without.
    cells: dict[tuple[str, str, float], dict[str, float]] = {}
    for (task_id, sku, temp, state), passes in bucket.items():
        mistake_rate = 1.0 - (sum(passes) / max(1, len(passes)))
        cell = cells.setdefault((task_id, sku, temp), {})
        cell[state] = mistake_rate
        cell[f"{state}_n"] = len(passes)

    rows: list[str] = [
        "| Task | Model | Temp | n | Mistake-rate without rule | Mistake-rate with rule | Re-Mistake-Rate |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for (task_id, sku, temp), c in sorted(cells.items()):
        without = c.get("without_rule", float("nan"))
        with_r = c.get("with_rule", float("nan"))
        n_with = int(c.get("with_rule_n", 0))
        rmr = with_r / without if without else float("nan")
        rows.append(
            f"| `{task_id}` | `{sku}` | {temp:.1f} | {n_with} | "
            f"{without:.2%} | {with_r:.2%} | **{rmr:.2f}** |"
        )
    return "\n".join(rows)


def build_block() -> str:
    body = _placeholder() if not BASELINE.exists() else _table_from_baseline(BASELINE)
    return f"{START}\n\n{body}\n\n{END}"


def update(check: bool = False) -> int:
    if not README.exists():
        print(f"missing: {README}", file=sys.stderr)
        return 1
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        # Markers are optional — only present once an eval section is added.
        # Without markers there's nothing to render; exit 0 quietly.
        if check:
            return 0
        print("no eval-table markers in README; nothing to render.")
        return 0
    new_block = build_block()
    new_text = text.split(START)[0] + new_block + text.split(END, 1)[1]
    if check:
        if new_text != text:
            print(
                "render_eval_table.py: drift detected. Run `python tools/render_eval_table.py` and commit.",
                file=sys.stderr,
            )
            return 1
        return 0
    README.write_text(new_text, encoding="utf-8")
    print(f"wrote: {README}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument(
        "--check", action="store_true", help="fail with exit 1 if README would change (CI use)"
    )
    args = parser.parse_args()
    return update(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
