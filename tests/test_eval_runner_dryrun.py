"""Tests for tools/eval_runner.py in --dry-run mode.

Exercises the full pipeline end-to-end without API keys: load task,
build prompts, canonical hash, dry-run provider, criterion eval,
Result emission. The JSONL records produced must validate against
schemas/eval-result.json.
"""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import eval_runner  # noqa: E402

RESULT_SCHEMA = json.loads((ROOT / "schemas" / "eval-result.json").read_text(encoding="utf-8"))


def _spec(model_sku: str = "dry-run-stub-1.0.0", provider: str = "dry_run") -> eval_runner.ModelSpec:
    return eval_runner.ModelSpec(
        provider=provider,
        model_sku=model_sku,
        temperature=0.0,
        max_tokens=1024,
        top_p=1.0,
    )


def test_dry_run_produces_schema_valid_records():
    """Run task 01 in dry-run mode and validate every Result against the schema."""
    task = eval_runner.load_task("01-ts-async-without-await")
    spec = _spec()
    results = eval_runner.run_task(
        task, spec, n_samples=3, rule_state="with_rule", run_id="test-dry-1", dry_run=True
    )
    assert len(results) == 3
    validator = Draft202012Validator(RESULT_SCHEMA)
    for r in results:
        record = dataclasses.asdict(r)
        errs = list(validator.iter_errors(record))
        assert errs == [], f"schema error in dry-run result: {errs}\nrecord: {record}"
        assert record["status"] == "dry_run"
        assert record["schema_version"] == "1.0.0"
        assert record["harness_version"] == eval_runner.HARNESS_VERSION
        assert record["task_id"] == "01-ts-async-without-await"
        assert record["rule_state"] == "with_rule"


def test_canonical_hash_is_stable_across_calls():
    """Same inputs => same prompt_canon_hash. Different sample_index => same hash."""
    task = eval_runner.load_task("02-python-mutable-default")
    spec = _spec()
    r1 = eval_runner.run_task(
        task, spec, n_samples=2, rule_state="with_rule", run_id="test-hash-1", dry_run=True
    )
    r2 = eval_runner.run_task(
        task, spec, n_samples=2, rule_state="with_rule", run_id="test-hash-2", dry_run=True
    )
    # The hash binds task + rule_state + model + temp + max_tokens + top_p +
    # harness_version. Sample index is NOT in the hash. So r1[0] and r1[1]
    # and r2[0] and r2[1] all share the same prompt_canon_hash.
    hashes = {r.prompt_canon_hash for r in r1 + r2}
    assert len(hashes) == 1, f"expected one hash, got {hashes}"


def test_canonical_hash_changes_with_rule_state():
    """with_rule vs without_rule must produce different prompt_canon_hashes."""
    task = eval_runner.load_task("03-react-key-missing")
    spec = _spec()
    r_with = eval_runner.run_task(task, spec, 1, "with_rule", "test-rs-1", dry_run=True)
    r_without = eval_runner.run_task(task, spec, 1, "without_rule", "test-rs-2", dry_run=True)
    assert r_with[0].prompt_canon_hash != r_without[0].prompt_canon_hash, (
        "rule_state must affect prompt_canon_hash"
    )


def test_dry_run_provider_returns_no_cost():
    """Dry-run mode must not incur any cost (pricebook entry for dry-run-stub is zero)."""
    task = eval_runner.load_task("04-sql-select-star")
    spec = _spec()
    results = eval_runner.run_task(
        task, spec, n_samples=2, rule_state="with_rule", run_id="test-cost-1", dry_run=True
    )
    for r in results:
        # Dry-run uses the dry_run provider; pricebook has no entry, cost_for falls back to 0.
        assert r.cost_usd == 0.0, f"dry-run cost must be zero, got {r.cost_usd}"


def test_real_provider_without_sdk_or_keys_is_recorded_as_error():
    """When the eval[anthropic|openai|requests] optional deps are not
    installed or the API key is missing, the harness still produces a
    well-formed Result with status=provider_error — never crashes the run.
    Either path is acceptable; CI installs the deps so the error is
    likely 'authentication' rather than 'ImportError', but the contract
    is just 'no crash, status=provider_error, error.code set'."""
    task = eval_runner.load_task("01-ts-async-without-await")
    spec = eval_runner.ModelSpec(
        provider="anthropic",
        model_sku="claude-sonnet-4-5-20251022",
        temperature=0.0,
        max_tokens=1024,
        top_p=1.0,
    )
    # Force-clear the API key so the test is deterministic even on CI
    # where ANTHROPIC_API_KEY might be set.
    import os

    saved = os.environ.pop("ANTHROPIC_API_KEY", None)
    try:
        results = eval_runner.run_task(
            task,
            spec,
            n_samples=1,
            rule_state="with_rule",
            run_id="test-real-1",
            dry_run=False,
        )
    finally:
        if saved is not None:
            os.environ["ANTHROPIC_API_KEY"] = saved
    assert len(results) == 1
    r = results[0]
    assert r.status == "provider_error", f"expected provider_error, got {r.status}"
    assert r.error is not None
    assert r.error.get("code"), "error.code must be set"


def test_judge_calibration_jsonl_is_well_formed():
    """The Tier-3 judge calibration corpus for task 05 must parse cleanly
    and carry exactly the expected_verdict values."""
    cal_path = ROOT / "tests" / "eval" / "tasks" / "05-judge-calibration.jsonl"
    assert cal_path.exists(), "05-judge-calibration.jsonl must exist for tier-3 task 05"
    n_pass = 0
    n_fail = 0
    with cal_path.open(encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            entry = json.loads(line)  # JSONDecodeError surfaces directly
            assert "response_text" in entry, f"line {line_no}: missing response_text"
            assert "expected_verdict" in entry, f"line {line_no}: missing expected_verdict"
            assert entry["expected_verdict"] in {"pass", "fail"}, (
                f"line {line_no}: expected_verdict must be pass|fail"
            )
            assert len(entry["response_text"]) >= 30, f"line {line_no}: response_text suspiciously short"
            if entry["expected_verdict"] == "pass":
                n_pass += 1
            else:
                n_fail += 1
    # Methodology contract: 10 known-pass + 10 known-fail per Tier-3 task.
    assert n_pass == 10, f"expected 10 pass calibration entries, got {n_pass}"
    assert n_fail == 10, f"expected 10 fail calibration entries, got {n_fail}"


def test_evaluate_criterion_regex_pass_and_fail():
    """The regex criterion evaluator returns the expected pass/fail."""
    task = eval_runner.load_task("01-ts-async-without-await")
    # Task 01 pass-pattern: `const\s+\w+\s*=\s*await\s+db\.findById\(`
    pass_text = "const userName = await db.findById(id);\nreturn userName.name;"
    fail_text = "return db.findById(id).name;"
    crit_type, pass_result, _ = eval_runner.evaluate_criterion(pass_text, task)
    assert crit_type == "regex"
    assert pass_result is True
    _, fail_result, _ = eval_runner.evaluate_criterion(fail_text, task)
    assert fail_result is False
