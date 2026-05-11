#!/usr/bin/env python3
"""
validate_eval_results.py - JSON-Schema validator for tests/eval/results/*.jsonl.

Reads a JSONL file, parses every line, validates each record against
schemas/eval-result.json. Exits 0 on clean, 1 on any error.

Additional cross-line checks (caught by the same exit code):
    - All records share the same run_id (catches accidentally-concatenated files).
    - All records for one (task_id, rule_state) pair share the same
      prompt_canon_hash (catches mid-run prompt drift).
    - schema_version is consistent across the file.

Usage:
    python tools/validate_eval_results.py tests/eval/results/run-abc.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "eval-result.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("path", help="JSONL file to validate")
    args = parser.parse_args(argv)

    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    p = Path(args.path)
    if not p.exists():
        print(f"missing: {p}", file=sys.stderr)
        return 1

    errors: list[str] = []
    run_ids: set[str] = set()
    schema_versions: set[str] = set()
    canon_hashes: dict[tuple[str, str], set[str]] = defaultdict(set)
    n_records = 0

    with p.open(encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"line {lineno}: JSON decode: {e}")
                continue
            for v in validator.iter_errors(rec):
                errors.append(f"line {lineno}: schema: {v.message}")
            n_records += 1
            if isinstance(rec, dict):
                if "run_id" in rec:
                    run_ids.add(rec["run_id"])
                if "schema_version" in rec:
                    schema_versions.add(rec["schema_version"])
                if "task_id" in rec and "rule_state" in rec and "prompt_canon_hash" in rec:
                    canon_hashes[(rec["task_id"], rec["rule_state"])].add(rec["prompt_canon_hash"])

    # Cross-line invariants
    if len(run_ids) > 1:
        errors.append(
            f"cross-line: {len(run_ids)} distinct run_ids in one file "
            f"(expected exactly 1). Files were probably concatenated."
        )
    if len(schema_versions) > 1:
        errors.append(
            f"cross-line: {len(schema_versions)} distinct schema_versions: {sorted(schema_versions)}"
        )
    for (task_id, rule_state), hashes in canon_hashes.items():
        if len(hashes) > 1:
            errors.append(
                f"cross-line: ({task_id}, {rule_state}) has {len(hashes)} distinct "
                f"prompt_canon_hash values — prompt drifted mid-run"
            )

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print(
            f"\n{len(errors)} validation error(s) across {n_records} record(s)",
            file=sys.stderr,
        )
        return 1

    print(f"validate_eval_results.py: clean ({n_records} record(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
