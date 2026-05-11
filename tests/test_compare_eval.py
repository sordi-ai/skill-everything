"""Tests for tools/compare_eval.py.

Exercises the baseline-vs-rerun Re-Mistake-Rate comparison: synthesise
two minimal JSONL files, run compare_eval.main(), assert exit code +
divergence accounting.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import compare_eval  # noqa: E402


def _make_record(
    task_id: str,
    model_sku: str,
    temperature: float,
    rule_state: str,
    sample_index: int,
    criterion_pass: bool,
) -> dict:
    """Minimal record that satisfies _aggregate's keying requirements."""
    return {
        "schema_version": "1.0.0",
        "run_id": "test-run-01",
        "harness_version": "0.1.0",
        "task_id": task_id,
        "task_yml_sha256": "0" * 64,
        "rule_state": rule_state,
        "model_sku": model_sku,
        "temperature": temperature,
        "max_tokens": 1024,
        "top_p": 1.0,
        "sample_index": sample_index,
        "prompt_canon_hash": "a" * 64,
        "prompt_bytes_sha256": "b" * 64,
        "response_text": "x",
        "tokens_in": 1,
        "tokens_out": 1,
        "cost_usd": 0.0,
        "cost_pricebook_version": "v",
        "latency_ms": 1,
        "criterion_type": "regex",
        "criterion_pass": criterion_pass,
        "status": "ok",
        "timestamp_utc": "2026-05-11T00:00:00Z",
    }


def _write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")


def _make_cell(
    task: str, sku: str, temp: float, with_pass: int, with_fail: int, without_pass: int, without_fail: int
) -> list[dict]:
    """Helper: build a (task, sku, temp) cell with explicit pass/fail counts."""
    out: list[dict] = []
    for i in range(with_pass):
        out.append(_make_record(task, sku, temp, "with_rule", i, True))
    for i in range(with_pass, with_pass + with_fail):
        out.append(_make_record(task, sku, temp, "with_rule", i, False))
    for j in range(without_pass):
        out.append(_make_record(task, sku, temp, "without_rule", j, True))
    for j in range(without_pass, without_pass + without_fail):
        out.append(_make_record(task, sku, temp, "without_rule", j, False))
    return out


def test_clean_reproduction_exits_zero(tmp_path: Path) -> None:
    """Baseline RMR == rerun RMR, so all cells match the tolerance trivially."""
    # Cell: with_rule 70% pass (mistake 30%) / without_rule 30% pass (mistake 70%)
    # RMR = 0.30 / 0.70 = 0.428...
    base_records = _make_cell(
        "01-task", "model-a-1", 0.0, with_pass=70, with_fail=30, without_pass=30, without_fail=70
    )
    rerun_records = list(base_records)  # identical
    base = tmp_path / "base.jsonl"
    rerun = tmp_path / "rerun.jsonl"
    _write_jsonl(base, base_records)
    _write_jsonl(rerun, rerun_records)
    rc = compare_eval.main([str(base), str(rerun), "--tolerance", "0.10", "--min-n", "30"])
    assert rc == 0


def test_diverging_reproduction_exits_one(tmp_path: Path) -> None:
    """Rerun RMR drifts beyond tolerance — exit code 1."""
    # Baseline: RMR ≈ 0.30/0.70 = 0.428
    base_records = _make_cell(
        "01-task", "model-a-1", 0.0, with_pass=70, with_fail=30, without_pass=30, without_fail=70
    )
    # Rerun: with_rule mistake jumps to 60%, without_rule unchanged
    # RMR ≈ 0.60/0.70 = 0.857  -> Δ = 0.43 > 0.10
    rerun_records = _make_cell(
        "01-task", "model-a-1", 0.0, with_pass=40, with_fail=60, without_pass=30, without_fail=70
    )
    base = tmp_path / "base.jsonl"
    rerun = tmp_path / "rerun.jsonl"
    _write_jsonl(base, base_records)
    _write_jsonl(rerun, rerun_records)
    rc = compare_eval.main([str(base), str(rerun), "--tolerance", "0.10", "--min-n", "30"])
    assert rc == 1


def test_low_n_cells_are_skipped(tmp_path: Path) -> None:
    """Cells below --min-n are skipped, not failed."""
    base_records = _make_cell(
        "01-task", "model-a-1", 0.0, with_pass=5, with_fail=5, without_pass=5, without_fail=5
    )  # n=10 < 30
    rerun_records = list(base_records)
    base = tmp_path / "base.jsonl"
    rerun = tmp_path / "rerun.jsonl"
    _write_jsonl(base, base_records)
    _write_jsonl(rerun, rerun_records)
    rc = compare_eval.main([str(base), str(rerun), "--tolerance", "0.10", "--min-n", "30"])
    # All cells skipped => no comparable cells => exit 1 ("cannot certify")
    assert rc == 1


def test_missing_file_exits_two(tmp_path: Path) -> None:
    rc = compare_eval.main([str(tmp_path / "missing-base.jsonl"), str(tmp_path / "missing-rerun.jsonl")])
    assert rc == 2


def test_aggregate_skips_non_ok_status(tmp_path: Path) -> None:
    """Records with status != 'ok' must not contribute to the rate."""
    rec_ok = _make_record("01-task", "model-a-1", 0.0, "with_rule", 0, True)
    rec_err = _make_record("01-task", "model-a-1", 0.0, "with_rule", 1, False)
    rec_err["status"] = "provider_error"
    base = tmp_path / "base.jsonl"
    _write_jsonl(base, [rec_ok, rec_err])
    cells = compare_eval._aggregate(base)
    key = ("01-task", "model-a-1", 0.0, "with_rule")
    assert key in cells
    # Only the one ok record counted, mistake_rate = 0.0 (1 pass / 1)
    assert cells[key]["n"] == 1
    assert cells[key]["mistake_rate"] == 0.0
