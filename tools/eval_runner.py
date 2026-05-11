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

Real-provider calls (Anthropic / OpenAI / Ollama) are implemented via
thin SDK wrappers with exponential-backoff retry on transient errors
(429, 5xx, connection / timeout). Each provider lazy-imports its SDK;
when the optional eval dependency group is not installed or the API
key env-var is missing, the harness records the failure as a per-sample
provider_error in the JSONL — it never crashes the orchestrator.

The --dry-run mode is preserved for CI smoke tests + pipeline verification
without API costs. CI always invokes --dry-run; --no-dry-run runs against
real providers gated by API-key secrets and a fail-fast --max-usd cap.

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
import functools
import hashlib
import json
import os
import random
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
    "Always",
    "Never",
    "Before",
    "After",
    "Prefer",
    "Avoid",
    "Use",
    "Do",
    "Ensure",
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


def _retry_on_transient(fn):
    """Decorator: retry up to 5 times on transient provider errors with
    exponential backoff + jitter. Retries on rate-limits (429), 5xx, and
    transport-level connection / timeout errors. Hard failures (4xx other
    than 429, content-policy, invalid-api-key) fail fast."""

    @functools.wraps(fn)
    def wrapper(self, system: str, user: str, spec: ModelSpec):
        last_err: Exception | None = None
        for attempt in range(5):
            try:
                return fn(self, system, user, spec)
            except Exception as e:
                last_err = e
                # Detect retriable status codes across SDKs.
                status = getattr(e, "status_code", None)
                if status is None:
                    response = getattr(e, "response", None)
                    if response is not None:
                        status = getattr(response, "status_code", None)
                name = type(e).__name__
                is_retriable = status in {429, 500, 502, 503, 504} or name in {
                    "ConnectionError",
                    "Timeout",
                    "ReadTimeout",
                    "APIConnectionError",
                    "APITimeoutError",
                    "RateLimitError",
                    "InternalServerError",
                    "ServiceUnavailableError",
                }
                if not is_retriable or attempt == 4:
                    raise
                delay = min(60.0, (2**attempt) * (1.0 + random.random()))
                time.sleep(delay)
        # Should be unreachable, but keep type-checker happy.
        if last_err is not None:
            raise last_err
        raise RuntimeError("retry loop exhausted with no last error")

    return wrapper


class AnthropicProvider:
    """Real Anthropic Messages API client. Lazy-imports the `anthropic`
    SDK so the harness still runs in dry-run mode without the optional
    eval dependencies installed. Requires `ANTHROPIC_API_KEY` env var."""

    def __init__(self) -> None:
        try:
            import anthropic  # noqa: F401
        except ImportError as e:
            raise RuntimeError(
                "anthropic SDK not installed. Install the eval dependency group: "
                "`pip install -e '.[eval]'` or `pip install anthropic`."
            ) from e
        from anthropic import Anthropic

        self._client = Anthropic()  # Anthropic() reads ANTHROPIC_API_KEY automatically

    @_retry_on_transient
    def complete(self, system: str, user: str, spec: ModelSpec) -> RawResponse:
        resp = self._client.messages.create(
            model=spec.model_sku,
            max_tokens=spec.max_tokens,
            temperature=spec.temperature,
            top_p=spec.top_p,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(getattr(block, "text", "") for block in resp.content)
        return RawResponse(
            text=text,
            tokens_in=resp.usage.input_tokens,
            tokens_out=resp.usage.output_tokens,
            system_fingerprint=None,
            model_provider_revision=resp.model,
            model_call_received_at=_now_utc(),
        )


class OpenAIProvider:
    """Real OpenAI Chat Completions client. Lazy-imports the `openai`
    SDK. Requires `OPENAI_API_KEY` env var."""

    def __init__(self) -> None:
        try:
            import openai  # noqa: F401
        except ImportError as e:
            raise RuntimeError(
                "openai SDK not installed. Install the eval dependency group: "
                "`pip install -e '.[eval]'` or `pip install openai`."
            ) from e
        from openai import OpenAI

        self._client = OpenAI()  # OpenAI() reads OPENAI_API_KEY automatically

    @_retry_on_transient
    def complete(self, system: str, user: str, spec: ModelSpec) -> RawResponse:
        kwargs = {
            "model": spec.model_sku,
            "max_tokens": spec.max_tokens,
            "temperature": spec.temperature,
            "top_p": spec.top_p,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        if spec.seed is not None:
            kwargs["seed"] = spec.seed
        resp = self._client.chat.completions.create(**kwargs)
        choice = resp.choices[0]
        return RawResponse(
            text=choice.message.content or "",
            tokens_in=resp.usage.prompt_tokens,
            tokens_out=resp.usage.completion_tokens,
            system_fingerprint=getattr(resp, "system_fingerprint", None),
            model_provider_revision=resp.model,
            model_call_received_at=_now_utc(),
        )


class OllamaProvider:
    """Ollama local inference via HTTP. Lazy-imports `requests`. Honours
    `OLLAMA_HOST` env var (default `http://localhost:11434`)."""

    def __init__(self) -> None:
        try:
            import requests  # noqa: F401
        except ImportError as e:
            raise RuntimeError(
                "requests not installed. Install the eval dependency group: "
                "`pip install -e '.[eval]'` or `pip install requests`."
            ) from e
        self._host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

    @_retry_on_transient
    def complete(self, system: str, user: str, spec: ModelSpec) -> RawResponse:
        import requests

        # Strip an `@<digest>` suffix from the model_sku for the wire call;
        # the digest is for hash-pinning, not the Ollama API.
        bare_model = spec.model_sku.split("@", 1)[0]
        resp = requests.post(
            f"{self._host}/api/chat",
            json={
                "model": bare_model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "stream": False,
                "options": {
                    "temperature": spec.temperature,
                    "top_p": spec.top_p,
                    "seed": spec.seed if spec.seed is not None else 0,
                    "num_predict": spec.max_tokens,
                },
            },
            timeout=300,
        )
        resp.raise_for_status()
        data = resp.json()
        return RawResponse(
            text=data["message"]["content"],
            tokens_in=int(data.get("prompt_eval_count", 0)),
            tokens_out=int(data.get("eval_count", 0)),
            system_fingerprint=None,
            model_provider_revision=data.get("model", spec.model_sku),
            model_call_received_at=_now_utc(),
        )


def make_provider(name: str) -> Provider:
    """Construct a Provider instance for the named backend.

    Real providers raise RuntimeError at instantiation time when the
    optional SDK is missing or the auth env-var is absent. Calling code
    catches these and records them as provider_error in the Result.
    """
    if name == "dry_run":
        return DryRunProvider()
    if name == "anthropic":
        return AnthropicProvider()
    if name == "openai":
        return OpenAIProvider()
    if name == "ollama":
        return OllamaProvider()
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
        system = "You are a careful senior engineer. Produce code only; no commentary unless asked."
    return system, task.prompt


def _judge_verdict(
    response_text: str,
    task: Task,
    judge_provider: Provider,
    judge_spec: ModelSpec,
) -> tuple[bool, str]:
    """Call the judge model with the rubric + response. Returns
    (pass: bool, rationale: str). Parse failures default to (False,
    error-string) so callers can record the issue without crashing."""
    rubric = task.judge_rubric or (
        "Did the response demonstrate the expected behavior described in "
        'rule_under_test? Return JSON: {"pass": bool, "rationale": str}.'
    )
    judge_system = (
        "You are a strict evaluator. Output ONLY a single JSON object "
        'with two fields: "pass" (boolean) and "rationale" (one short '
        "sentence). No prose outside the JSON."
    )
    judge_user = f"# Rubric\n\n{rubric}\n\n# Response to evaluate\n\n{response_text}"
    raw = judge_provider.complete(judge_system, judge_user, judge_spec)
    # Be tolerant of judge models that wrap JSON in markdown fences.
    text = raw.text.strip()
    if text.startswith("```"):
        # Strip ```json ... ``` or ``` ... ```
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    try:
        verdict = json.loads(text)
    except json.JSONDecodeError as e:
        return False, f"judge JSON parse error: {e}; first 80 chars: {text[:80]!r}"
    pass_value = verdict.get("pass")
    if not isinstance(pass_value, bool):
        return False, f"judge returned non-boolean pass field: {pass_value!r}"
    rationale = str(verdict.get("rationale", ""))[:500]
    return pass_value, rationale


def evaluate_criterion(
    response_text: str,
    task: Task,
    judge_provider: Provider | None = None,
    judge_spec: ModelSpec | None = None,
) -> tuple[str, bool, str | None]:
    """Apply the task's pass_signature to the response.

    Returns (criterion_type, criterion_pass, rationale). For tier-3
    (judge) tasks, requires judge_provider + judge_spec; raises if they
    are missing. AST tier-2 remains stubbed; v1.0 build-out implements
    per-task AST checks as those tasks are added.
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
        # AST tier-2 stub. v1.0 implements per-task AST checks as needed.
        return "ast", False, "ast stub — per-task AST checks land with the task"
    if sig_type == "judge":
        if judge_provider is None or judge_spec is None:
            return "judge", False, "judge stub — judge_provider not configured"
        try:
            pass_value, rationale = _judge_verdict(response_text, task, judge_provider, judge_spec)
            return "judge", pass_value, rationale
        except Exception as e:
            return "judge", False, f"judge call failed: {type(e).__name__}: {e}"
    raise ValueError(f"unknown pass_signature.type: {sig_type!r}")


def measure_judge_calibration(
    task: Task,
    judge_provider: Provider,
    judge_spec: ModelSpec,
) -> float | None:
    """Score the judge against the task's 20-row calibration corpus.

    Returns accuracy in [0, 1] or None if the corpus is missing. Per the
    methodology contract, runs with judge_calibration_accuracy < 0.90 are
    invalid; the caller records the accuracy into every Result for the
    task and downstream stats handles the gating.
    """
    if task.judge_calibration is None:
        return None
    cal_path = ROOT / task.judge_calibration
    if not cal_path.exists():
        return None
    correct = 0
    total = 0
    with cal_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            response_text = entry.get("response_text", "")
            expected = entry.get("expected_verdict", "")  # "pass" or "fail"
            if expected not in {"pass", "fail"}:
                continue
            try:
                pass_value, _ = _judge_verdict(response_text, task, judge_provider, judge_spec)
            except Exception:
                # Judge call failed — count as wrong against the expected verdict.
                pass_value = expected != "pass"
            judge_verdict = "pass" if pass_value else "fail"
            if judge_verdict == expected:
                correct += 1
            total += 1
    if total == 0:
        return None
    return correct / total


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
    judge_provider: Provider | None = None,
    judge_spec: ModelSpec | None = None,
) -> list[Result]:
    """Run one (task, spec, rule_state) cell for n_samples.

    Returns one Result per sample. Caller is responsible for serialising
    to JSONL and aggregating across cells. For tier-3 tasks, the caller
    SHOULD provide judge_provider + judge_spec so the judge verdict can
    populate criterion_pass; without them tier-3 results carry
    criterion_pass=False with a "judge_provider not configured" rationale
    and the calibration accuracy is reported as None.
    """
    if rule_state not in {"with_rule", "without_rule"}:
        raise ValueError(f"rule_state must be with_rule or without_rule, got {rule_state!r}")
    # Provider construction can fail when the optional SDK isn't installed
    # or the API key env-var is missing. Record this as a per-sample
    # provider_error rather than crashing the whole pass — a single misconfigured
    # provider should produce error records, not abort the orchestrator.
    provider: Provider | None
    provider_init_err: Exception | None = None
    try:
        provider = make_provider("dry_run") if dry_run else make_provider(spec.provider)
    except Exception as e:
        provider = None
        provider_init_err = e

    book, book_version = load_pricebook()
    system, user = build_prompts(task, rule_state)
    canon_hash = canonical_prompt_hash(task, rule_state, system, user, spec)

    # Tier-3: measure judge calibration once per cell (not per sample) so
    # we don't pay the calibration cost 50-100 times. Same number is
    # stamped on every Result row from this cell.
    judge_cal_acc: float | None = None
    if task.tier == 3 and not dry_run and judge_provider is not None and judge_spec is not None:
        try:
            judge_cal_acc = measure_judge_calibration(task, judge_provider, judge_spec)
        except Exception:
            judge_cal_acc = None

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
        if provider_init_err is not None:
            status = "provider_error"
            err_obj = {
                "code": type(provider_init_err).__name__,
                "message": str(provider_init_err),
                "retry_count": 0,
            }
            text, tin, tout, sysfp, prov_rev, recv_at = "", 0, 0, None, None, None
        else:
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
        prompt_bytes_hash = hashlib.sha256((system + "\n\x1e\n" + user).encode("utf-8")).hexdigest()

        if status == "ok":
            # For dry-run, do not consult the judge — it would defeat
            # the "no API calls" property of --dry-run.
            jp = None if dry_run else judge_provider
            js = None if dry_run else judge_spec
            crit_type, crit_pass, rationale = evaluate_criterion(text, task, jp, js)
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
            judge_model_sku=(
                judge_spec.model_sku if crit_type == "judge" and judge_spec is not None else None
            ),
            judge_calibration_accuracy=(judge_cal_acc if crit_type == "judge" else None),
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
        raise argparse.ArgumentTypeError(f"unknown provider {prov!r}; must be anthropic, openai, or ollama")
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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip real provider calls; synthesise responses for pipeline testing.",
    )
    parser.add_argument(
        "--judge-model",
        default=None,
        help="Provider/SKU for the tier-3 judge model, e.g. "
        "anthropic/claude-opus-4-7-20260301. Required only for "
        "tier-3 tasks; ignored otherwise.",
    )
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

    # Build a judge provider/spec when --judge-model is set. The judge runs
    # at temperature=0 for determinism (per methodology contract).
    judge_provider: Provider | None = None
    judge_spec: ModelSpec | None = None
    if args.judge_model is not None and not args.dry_run:
        jp_name, jp_sku = _parse_model_arg(args.judge_model)
        judge_provider = make_provider(jp_name)
        judge_spec = ModelSpec(
            provider=jp_name,
            model_sku=jp_sku,
            temperature=0.0,
            max_tokens=512,
            top_p=1.0,
        )

    results = run_task(
        task,
        spec,
        args.n,
        args.rule_state,
        run_id,
        dry_run=args.dry_run,
        judge_provider=judge_provider,
        judge_spec=judge_spec,
    )

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
