#!/usr/bin/env python3
"""
eval_runner.py - Re-Mistake-Rate harness for tests/eval/tasks/*.yml.

Runs ONE (task, model, temperature, rule_state) cell end-to-end:
canonicalise prompts, hash inputs, call the provider (or synthesise in
dry-run), evaluate the pass-criterion, write JSONL records that satisfy
schemas/eval-result.json.

This is the harness layer. The methodology contract (sample sizes,
acceptance criteria, hash recipe) is in tests/eval/README.md. The
orchestrator that fans out the matrix (5 tasks x 5 models x 2 temps x
2 rule-states) is tools/run_eval.py. The JSONL validator is
tools/validate_eval_results.py.

Real-provider calls (Anthropic / OpenAI / Ollama) are stubbed in v0.75
PREVIEW. The harness runs end-to-end in --dry-run mode so the full
pipeline (hashing, criterion evaluation, JSONL emission, schema
validation) can be exercised in CI without API keys. Real providers
land in the v1.0 build-out.

Usage:
    python tools/eval_runner.py \\
        --task 01-ts-async-without-await \\
        --model anthropic/claude-sonnet-4-5-20251022 \\
        --temperature 0.0 --max-tokens 1024 --top-p 1.0 \\
        --rule-state with_rule --n 5 --dry-run \\
        --out /tmp/results.jsonl

Output: JSONL appended to --out, one record per sample. Schema:
schemas/eval-result.json.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import re
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, Protocol

import yaml

HARNESS_VERSION = "0.1.0"
SCHEMA_VERSION = "1.0.0"

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "tests" / "eval" / "tasks"
PRICEBOOK_PATH = ROOT / "tests" / "eval" / "pricebook.yml"

# Verb allow-list lifted from tools/validate_rules.py — used only to sanity
# check that `rule_under_test` in a task is a real action directive.
ALLOWED_VERBS = {
    "Always", "Never", "Before", "After",
    "Prefer", "Avoid", "Use", "Do", "Ensure",
}


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ModelSpec:
    """Pinned model identity. `model_sku` MUST be a dated SKU string."""
    provider: Literal["anthropic", "openai", "ollama", "dry_run"]
    model_sku: str
    temperature: float
    max_tokens: int
    top_p: float = 1.0
    seed: int | None = None


@dataclass
class Task:
    """In-memory representation of one tests/eval/tasks/*.yml fixture."""
    id: str
    title: str
    mistake_class: str
    rule_under_test: str
    prompt: str
    tier: int
    references: list[str]
    mistake_signature: dict
    pass_signature: dict
    judge_rubric: str | None = None
    judge_calibration: str | None = None
    notes: str | None = None
    # Computed at load time:
    yml_sha256: str = ""


@dataclass
class RawResponse:
    """Provider response after retries; what the harness records as wire output."""
    text: str
    tokens_in: int
    tokens_out: int
    system_fingerprint: str | None = None
    model_provider_revision: str | None = None
    model_call_received_at: str | None = None


@dataclass
class Result:
    """One JSONL record. Field set matches schemas/eval-result.json exactly."""
    schema_version: str
    run_id: str
    harness_version: str
    task_id: str
    task_yml_sha256: str
    rule_state: str
    model_sku: str
    temperature: float
    max_tokens: int
    top_p: float
    sample_index: int
    prompt_canon_hash: str
    prompt_bytes_sha256: str
    response_text: str
    tokens_in: int
    tokens_out: int
    cost_usd: float
    cost_pricebook_version: str
    latency_ms: int
    criterion_type: str
    criterion_pass: bool
    status: str
    timestamp_utc: str
    # Optional / null-permitted fields:
    model_provider_revision: str | None = None
    model_call_received_at: str | None = None
    seed: int | None = None
    criterion_rationale: str | None = None
    judge_model_sku: str | None = None
    judge_calibration_accuracy: float | None = None
    error: dict | None = None
    system_fingerprint: str | None = None
    notes: str | None = None


# ---------------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------------

class Provider(Protocol):
    def complete(self, system: str, user: str, spec: ModelSpec) -> RawResponse: ...


class DryRunProvider:
    """Synthesises deterministic responses without calling any API.

    Output is keyed on (prompt_canon_hash, sample_index). For pass-pattern
    tasks we deterministically return either a known-pass or known-mistake
    skeleton based on rule_state: with_rule -> 70% pass, without_rule -> 30%
    pass. That gives the rest of the pipeline (criterion evaluation,
    JSONL emission, schema validation) realistic data to chew on without
    spending a cent.
    """

    def complete(self, system: str, user: str, spec: ModelSpec) -> RawResponse:
        # Derive a deterministic pseudo-random verdict from inputs.
        salt = f"{system}\n\x1e\n{user}\n\x1e\n{spec.model_sku}\n{spec.seed}".encode()
        digest = hashlib.sha256(salt).hexdigest()
        # Treat the first hex char as a 0-15 scalar.
        roll = int(digest[0], 16)
        rule_in_system = "Always" in system or "Never" in system or "After" in system
        # with_rule: 70% pass (roll < 11); without_rule: 30% pass (roll < 5).
        threshold = 11 if rule_in_system else 5
        pass_outcome = roll < threshold
        text = (
            "// DRY-RUN synthetic response. No real provider was called.\n"
            f"// rule_state_hint={'with' if rule_in_system else 'without'} "
            f"pass_outcome={pass_outcome} digest_head={digest[:8]}\n"
            + (
                "const userName = await db.findById(id);\nreturn userName.name;\n"
                if pass_outcome
                else "return db.findById(id).name;\n"
            )
        )
        # Token counts are estimates: ~1 token / 3 chars.
        tin = max(1, (len(system) + len(user)) // 3)
        tout = max(1, len(text) // 3)
        return RawResponse(
            text=text,
            tokens_in=tin,
            tokens_out=tout,
            system_fingerprint="dry-run",
            model_provider_revision=spec.model_sku,
            model_call_received_at=_now_utc(),
        )


class _StubProvider:
    """Raises with a clear message pointing to the v1.0 build-out."""

    def __init__(self, provider_name: str):
        self.provider_name = provider_name

    def complete(self, system: str, user: str, spec: ModelSpec) -> RawResponse:
        raise NotImplementedError(
            f"Real {self.provider_name} provider is stubbed in v0.75 PREVIEW. "
            f"The harness runs end-to-end in --dry-run mode. Real provider "
            f"integration lands in the v1.0 build-out — see ROADMAP.md and "
            f"tests/eval/README.md."
        )


def make_provider(name: str) -> Provider:
    if name == "dry_run":
        return DryRunProvider()
    if name in {"anthropic", "openai", "ollama"}:
        return _StubProvider(name)
    raise ValueError(f"unknown provider: {name!r}")


# ---------------------------------------------------------------------------
# Hashing, prompt building, criterion evaluation
# ---------------------------------------------------------------------------

def canonical_prompt_hash(
    task: Task,
    rule_state: str,
    system_prompt: str,
    user_prompt: str,
    spec: ModelSpec,
) -> str:
    """SHA-256 over the 10-field hash recipe in tests/eval/README.md."""
    parts = [
        task.id,
        task.yml_sha256,
        rule_state,
        system_prompt,
        user_prompt,
        spec.model_sku,
        f"{spec.temperature:.3f}",
        str(spec.max_tokens),
        f"{spec.top_p:.3f}",
        HARNESS_VERSION,
    ]
    blob = "\n".join(parts).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def build_prompts(task: Task, rule_state: str) -> tuple[str, str]:
    """Materialise (system_prompt, user_prompt) for one cell.

    The rule_under_test goes in the system prompt (matches how Claude Code
    and OpenCode inject skill rules in production). User prompt is the
    task body verbatim, identical for with_rule and without_rule.
    """
    if rule_state == "with_rule":
        system = (
            "You are a careful senior engineer. Follow the rule below.\n\n"
            f"- {task.rule_under_test.strip()}\n\n"
            "Apply the rule. Produce code only; no commentary unless asked."
        )
    else:
        system = (
            "You are a careful senior engineer. "
            "Produce code only; no commentary unless asked."
        )
    return system, task.prompt


def evaluate_criterion(
    response_text: str,
    task: Task,
) -> tuple[str, bool, str | None]:
    """Apply the task's pass_signature to the response.

    Returns (criterion_type, criterion_pass, rationale). Tier-3 (judge)
    is stubbed: returns ("judge", False, "judge stub — v1.0") so the
    schema is satisfied but the run is not credit-bearing.
    """
    sig = task.pass_signature
    sig_type = sig.get("type")
    if sig_type == "regex":
        pattern = sig.get("pattern", "")
        match = re.search(pattern, response_text)
        return "regex", bool(match), None
    if sig_type == "regex_negative":
        # Pass = at least one of the patterns is present.
        pattern = sig.get("pattern", "")
        match = re.search(pattern, response_text)
        return "regex_negative", bool(match), None
    if sig_type == "ast":
        # AST tier-2 stub. v1.0 implements per-task AST checks.
        return "ast", False, "ast stub — v1.0 build-out"
    if sig_type == "judge":
        return "judge", False, "judge stub — v1.0 build-out"
    raise ValueError(f"unknown pass_signature.type: {sig_type!r}")


# ---------------------------------------------------------------------------
# Pricebook
# ---------------------------------------------------------------------------

def load_pricebook(path: Path = PRICEBOOK_PATH) -> tuple[dict, str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data["models"], str(data["version"])


def cost_for(spec: ModelSpec, tin: int, tout: int, book: dict) -> float:
    key = f"{spec.provider}/{spec.model_sku}" if "/" not in spec.model_sku else spec.model_sku
    # Allow callers to pass model_sku already containing the provider prefix.
    if key not in book:
        # Fall back to bare model_sku lookup.
        key = spec.model_sku
    rates = book.get(key)
    if rates is None:
        return 0.0
    return (tin * rates["input_per_mtok"] + tout * rates["output_per_mtok"]) / 1_000_000


# ---------------------------------------------------------------------------
# Task loading
# ---------------------------------------------------------------------------

def load_task(task_id: str) -> Task:
    """Load tests/eval/tasks/<task_id>.yml + compute yml_sha256."""
    path = TASKS_DIR / f"{task_id}.yml"
    raw_bytes = path.read_bytes()
    sha = hashlib.sha256(raw_bytes).hexdigest()
    data = yaml.safe_load(raw_bytes.decode("utf-8"))
    return Task(
        id=data["id"],
        title=data["title"],
        mistake_class=data["mistake_class"],
        rule_under_test=data["rule_under_test"],
        prompt=data["prompt"],
        tier=data.get("tier", 1),
        references=data.get("references", []),
        mistake_signature=data["mistake_signature"],
        pass_signature=data["pass_signature"],
        judge_rubric=data.get("judge_rubric"),
        judge_calibration=data.get("judge_calibration"),
        notes=data.get("notes"),
        yml_sha256=sha,
    )


# ---------------------------------------------------------------------------
# Core: run_task
# ---------------------------------------------------------------------------

def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_task(
    task: Task,
    spec: ModelSpec,
    n_samples: int,
    rule_state: str,
    run_id: str,
    dry_run: bool = False,
) -> list[Result]:
    """Run one (task, spec, rule_state) cell for n_samples.

    Returns one Result per sample. Caller is responsible for serialising
    to JSONL and aggregating across cells.
    """
    if rule_state not in {"with_rule", "without_rule"}:
        raise ValueError(f"rule_state must be with_rule or without_rule, got {rule_state!r}")
    provider = make_provider("dry_run") if dry_run else make_provider(spec.provider)

    book, book_version = load_pricebook()
    system, user = build_prompts(task, rule_state)
    canon_hash = canonical_prompt_hash(task, rule_state, system, user, spec)

    out: list[Result] = []
    for i in range(n_samples):
        # Per-sample seed: deterministic from (canon_hash, sample_index).
        sample_seed = int(
            hashlib.sha256(f"{canon_hash}:{i}".encode()).hexdigest()[:8],
            16,
        )
        spec_i = dataclasses.replace(spec, seed=sample_seed)
        t0 = time.monotonic()
        status: str = "ok"
        err_obj: dict | None = None
        try:
            raw = provider.complete(system, user, spec_i)
            text, tin, tout = raw.text, raw.tokens_in, raw.tokens_out
            sysfp = raw.system_fingerprint
            prov_rev = raw.model_provider_revision
            recv_at = raw.model_call_received_at
        except NotImplementedError as e:
            status = "provider_error"
            err_obj = {"code": "NotImplementedError", "message": str(e), "retry_count": 0}
            text, tin, tout, sysfp, prov_rev, recv_at = "", 0, 0, None, None, None
        except Exception as e:
            status = "provider_error"
            err_obj = {"code": type(e).__name__, "message": str(e), "retry_count": 0}
            text, tin, tout, sysfp, prov_rev, recv_at = "", 0, 0, None, None, None
        latency_ms = int((time.monotonic() - t0) * 1000)

        # Defensive: hash the bytes we actually had on hand (after any SDK
        # serialisation a real provider would have done). In dry-run / stub
        # mode this equals canon_hash; in real mode it may diverge.
        prompt_bytes_hash = hashlib.sha256(
            (system + "\n\x1e\n" + user).encode("utf-8")
        ).hexdigest()

        if status == "ok":
            crit_type, crit_pass, rationale = evaluate_criterion(text, task)
        else:
            crit_type, crit_pass, rationale = (
                task.pass_signature.get("type", "regex"),
                False,
                f"status={status}",
            )

        if dry_run:
            status = "dry_run"

        result = Result(
            schema_version=SCHEMA_VERSION,
            run_id=run_id,
            harness_version=HARNESS_VERSION,
            task_id=task.id,
            task_yml_sha256=task.yml_sha256,
            rule_state=rule_state,
            model_sku=spec.model_sku,
            temperature=spec.temperature,
            max_tokens=spec.max_tokens,
            top_p=spec.top_p,
            sample_index=i,
            prompt_canon_hash=canon_hash,
            prompt_bytes_sha256=prompt_bytes_hash,
            response_text=text,
            tokens_in=tin,
            tokens_out=tout,
            cost_usd=cost_for(spec, tin, tout, book) if status == "ok" else 0.0,
            cost_pricebook_version=book_version,
            latency_ms=latency_ms,
            criterion_type=crit_type,
            criterion_pass=crit_pass,
            status=status,
            timestamp_utc=_now_utc(),
            model_provider_revision=prov_rev,
            model_call_received_at=recv_at,
            seed=spec_i.seed if spec.provider != "anthropic" else None,
            criterion_rationale=rationale,
            error=err_obj,
            system_fingerprint=sysfp,
        )
        out.append(result)
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_model_arg(raw: str) -> tuple[str, str]:
    """Parse 'provider/model_sku' -> ('provider', 'model_sku').

    For dry-run, accept bare 'dry-run' or 'dry_run' as shorthand.
    """
    if raw in {"dry-run", "dry_run"}:
        return "dry_run", "dry-run-stub-1.0.0"
    if "/" not in raw:
        raise argparse.ArgumentTypeError(
            "--model must be 'provider/model_sku', e.g. anthropic/claude-sonnet-4-5-20251022"
        )
    prov, sku = raw.split("/", 1)
    if prov not in {"anthropic", "openai", "ollama"}:
        raise argparse.ArgumentTypeError(
            f"unknown provider {prov!r}; must be anthropic, openai, or ollama"
        )
    return prov, sku


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one eval cell end-to-end.")
    parser.add_argument("--task", required=True, help="Task id, e.g. 01-ts-async-without-await")
    parser.add_argument("--model", required=True, help="Model in 'provider/sku' form (or 'dry-run')")
    parser.add_argument("--temperature", type=float, required=True)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--rule-state", choices=["with_rule", "without_rule"], required=True)
    parser.add_argument("--n", type=int, default=1, help="Samples per cell")
    parser.add_argument("--run-id", default=None, help="Stable identifier for this run (default: uuid7)")
    parser.add_argument("--out", default="-", help="JSONL output path; '-' = stdout")
    parser.add_argument("--dry-run", action="store_true",
                        help="Skip real provider calls; synthesise responses for pipeline testing.")
    args = parser.parse_args(argv)

    provider_name, model_sku = _parse_model_arg(args.model)
    spec = ModelSpec(
        provider=provider_name,
        model_sku=model_sku,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        top_p=args.top_p,
    )
    task = load_task(args.task)
    run_id = args.run_id or uuid.uuid4().hex[:16]

    results = run_task(task, spec, args.n, args.rule_state, run_id, dry_run=args.dry_run)

    if args.out == "-":
        for r in results:
            sys.stdout.write(json.dumps(dataclasses.asdict(r), ensure_ascii=False) + "\n")
    else:
        with Path(args.out).open("a", encoding="utf-8") as sink:
            for r in results:
                sink.write(json.dumps(dataclasses.asdict(r), ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
