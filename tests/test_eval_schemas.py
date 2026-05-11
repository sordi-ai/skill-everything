"""Tests for schemas/eval-task.json + schemas/eval-result.json contracts.

Validates that every fixture in tests/eval/tasks/*.yml matches the task
schema, and that a synthetic eval-runner output matches the result schema.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "tests" / "eval" / "tasks"
TASK_SCHEMA = ROOT / "schemas" / "eval-task.json"
RESULT_SCHEMA = ROOT / "schemas" / "eval-result.json"


def _load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_every_task_yml_validates_against_task_schema():
    schema = _load_schema(TASK_SCHEMA)
    validator = Draft202012Validator(schema)
    failures = []
    for yml in sorted(TASKS_DIR.glob("0[1-9]-*.yml")):
        data = yaml.safe_load(yml.read_text(encoding="utf-8"))
        errs = list(validator.iter_errors(data))
        for e in errs:
            failures.append(f"{yml.name}: {e.message}")
    assert failures == [], "\n  " + "\n  ".join(failures)


def test_tier_3_tasks_carry_judge_rubric():
    schema = _load_schema(TASK_SCHEMA)
    validator = Draft202012Validator(schema)
    for yml in sorted(TASKS_DIR.glob("0[1-9]-*.yml")):
        data = yaml.safe_load(yml.read_text(encoding="utf-8"))
        if data.get("tier") == 3:
            assert data.get("judge_rubric"), (
                f"{yml.name}: tier=3 task must carry judge_rubric"
            )
            # Schema's allOf conditional enforces this too — double-check:
            errs = list(validator.iter_errors(data))
            assert errs == [], f"{yml.name}: schema errors: {errs}"


def test_result_schema_accepts_minimal_record():
    schema = _load_schema(RESULT_SCHEMA)
    validator = Draft202012Validator(schema)
    record = {
        "schema_version": "1.0.0",
        "run_id": "abc-test-1234",
        "harness_version": "0.1.0",
        "task_id": "01-ts-async-without-await",
        "task_yml_sha256": "0" * 64,
        "rule_state": "with_rule",
        "model_sku": "claude-sonnet-4-5-20251022",
        "temperature": 0.0,
        "max_tokens": 1024,
        "top_p": 1.0,
        "sample_index": 0,
        "prompt_canon_hash": "a" * 64,
        "prompt_bytes_sha256": "b" * 64,
        "response_text": "synthetic",
        "tokens_in": 100,
        "tokens_out": 50,
        "cost_usd": 0.0005,
        "cost_pricebook_version": "2026-05-11",
        "latency_ms": 250,
        "criterion_type": "regex",
        "criterion_pass": True,
        "status": "ok",
        "timestamp_utc": "2026-05-11T10:00:00Z",
    }
    errs = list(validator.iter_errors(record))
    assert errs == [], f"unexpected schema errors: {errs}"


def test_result_schema_rejects_missing_required_field():
    schema = _load_schema(RESULT_SCHEMA)
    validator = Draft202012Validator(schema)
    record = {"schema_version": "1.0.0"}  # missing everything else
    errs = list(validator.iter_errors(record))
    assert errs, "expected validation errors for under-specified record"


def test_result_schema_rejects_bare_model_sku():
    """A model_sku without a dated revision is methodologically forbidden,
    but the schema only enforces minLength + string — the dated-revision
    convention is documented in tests/eval/README.md and enforced at the
    harness level. This test confirms a too-short model_sku is rejected."""
    schema = _load_schema(RESULT_SCHEMA)
    validator = Draft202012Validator(schema)
    record = {
        "schema_version": "1.0.0",
        "run_id": "abc-1",
        "harness_version": "0.1.0",
        "task_id": "01-ts-async-without-await",
        "task_yml_sha256": "0" * 64,
        "rule_state": "with_rule",
        "model_sku": "ab",  # too short
        "temperature": 0.0,
        "max_tokens": 1024,
        "top_p": 1.0,
        "sample_index": 0,
        "prompt_canon_hash": "a" * 64,
        "prompt_bytes_sha256": "b" * 64,
        "response_text": "",
        "tokens_in": 0,
        "tokens_out": 0,
        "cost_usd": 0.0,
        "cost_pricebook_version": "v",
        "latency_ms": 0,
        "criterion_type": "regex",
        "criterion_pass": False,
        "status": "ok",
        "timestamp_utc": "2026-05-11T10:00:00Z",
    }
    errs = list(validator.iter_errors(record))
    assert errs, "expected minLength error for too-short model_sku"
