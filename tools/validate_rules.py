#!/usr/bin/env python3
"""
validate_rules.py - Schema + lint validator for references/errors/error-log.md
                    and sub-skill manifest frontmatter.

Usage:
    python tools/validate_rules.py [--soft]

Exit code 0 on clean, 1 on validation errors. --soft prints but doesn't fail.

Validation layers (all run independently):
    1. JSON-Schema validation against schemas/error-entry.json for every error entry.
    2. Verb allow-list check on `new_rule` field (must start with one of:
       Always, Never, Before, After, Prefer, Avoid, Use, Do, Ensure).
    3. Forbidden-pattern check on `new_rule` (URLs, shell binaries, credential
       paths, base64-shaped strings, <script> tags, fs-mutation commands).
    4. JSON-Schema validation against schemas/skill-manifest.json for every
       sub-skill frontmatter block.

Honest limitations (also documented in SECURITY.md):
    * The verb allow-list and forbidden patterns are best-effort, not airtight.
    * Homoglyph attacks (e.g. Cyrillic look-alikes that visually match
      Latin letters) bypass pattern matching.
    * Indirection ("run the {tool} command") bypasses literal patterns.
    * Human PR review remains the primary trust boundary.
    See tests/test_validate_rules_adversarial.py for the documented bypass set.

Bypass mechanism:
    Add an entry to references/errors/exceptions.yml with a rationale and
    require CODEOWNERS approval to merge it. The validator soft-fails for
    listed IDs (forbidden-pattern violations only; schema errors stay hard).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
ERROR_LOG = ROOT / "references" / "errors" / "error-log.md"
ERROR_SCHEMA = ROOT / "schemas" / "error-entry.json"
SKILL_SCHEMA = ROOT / "schemas" / "skill-manifest.json"
EXCEPTIONS = ROOT / "references" / "errors" / "exceptions.yml"

ALLOWED_VERBS = {
    "Always", "Never", "Before", "After",
    "Prefer", "Avoid", "Use", "Do", "Ensure",
}

FORBIDDEN_PATTERNS = [
    (re.compile(r"\b(curl|wget|fetch|exec|eval|os\.system|subprocess|spawn|popen)\b", re.I),
     "shell-exec"),
    (re.compile(r"https?://"),
     "url-in-rule"),
    (re.compile(r"\b(cat|less|head|tail)\s+/", re.I),
     "fs-read"),
    (re.compile(r"\b(rm|chmod|chown|sudo)\b", re.I),
     "fs-mutate"),
    (re.compile(r"~/\.(ssh|aws|gcp|kube|gnupg|config)", re.I),
     "credentials-path"),
    (re.compile(r"[A-Za-z0-9+/]{40,}={0,2}"),
     "base64-blob"),
    (re.compile(r"<\s*script", re.I),
     "html-tag"),
]

SUB_SKILL_DIRS = ["development", "git", "process", "domain", "errors"]


def load_yaml_file(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None


def _stringify_dates(obj):
    """yaml.safe_load returns datetime.date for ISO date scalars; the JSON-Schema
    expects strings with format=date. Convert them in place before validation."""
    import datetime
    if isinstance(obj, dict):
        return {k: _stringify_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_stringify_dates(x) for x in obj]
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()[:10] if isinstance(obj, datetime.date) else obj.isoformat()
    return obj


def load_exceptions() -> set[str]:
    if not EXCEPTIONS.exists():
        return set()
    data = yaml.safe_load(EXCEPTIONS.read_text(encoding="utf-8")) or {}
    ids = data.get("allow_forbidden_pattern_for", [])
    return set(ids) if isinstance(ids, list) else set()


def lint_rule_text(rule: str, eid: str, allow_forbidden: bool) -> list[str]:
    """Verb allow-list + forbidden-pattern checks. Returns list of error strings."""
    errs: list[str] = []
    head = (rule.strip().split() or [""])[0]
    if head not in ALLOWED_VERBS:
        errs.append(
            f"{eid}: new_rule must start with one of "
            f"{sorted(ALLOWED_VERBS)} (got {head!r})"
        )
    if not allow_forbidden:
        for pattern, tag in FORBIDDEN_PATTERNS:
            if pattern.search(rule):
                errs.append(f"{eid}: forbidden pattern [{tag}]")
    return errs


def validate_error_log() -> list[str]:
    """Run schema + lint over every error entry in error-log.md."""
    if not ERROR_LOG.exists():
        return [f"file not found: {ERROR_LOG}"]
    if not ERROR_SCHEMA.exists():
        return [f"schema not found: {ERROR_SCHEMA}"]

    schema = load_yaml_file(ERROR_SCHEMA)  # JSON is valid YAML
    validator = Draft202012Validator(schema)
    exceptions = load_exceptions()

    text = ERROR_LOG.read_text(encoding="utf-8")
    errors: list[str] = []

    for block in re.findall(r"```yaml\s*\n(.*?)```", text, re.DOTALL):
        try:
            doc = yaml.safe_load(block)
        except yaml.YAMLError as e:
            errors.append(f"yaml-parse: {e}")
            continue
        if doc is None:
            continue
        if isinstance(doc, dict) and "errors" in doc:
            items = doc["errors"]
        elif isinstance(doc, list):
            items = doc
        else:
            items = [doc]
        for entry in items or []:
            if not isinstance(entry, dict):
                continue
            eid = str(entry.get("id", "?"))
            # Skip template placeholders (ERR-YYYY-NNN) so the schema doesn't
            # complain about the documentation example.
            if "YYYY" in eid:
                continue
            entry_for_schema = _stringify_dates(entry)
            for v in validator.iter_errors(entry_for_schema):
                errors.append(f"{eid}: schema: {v.message}")
            allow_forbidden = eid in exceptions
            errors.extend(
                lint_rule_text(
                    str(entry.get("new_rule", "")),
                    eid,
                    allow_forbidden,
                )
            )
    return errors


def parse_frontmatter(path: Path) -> dict | None:
    """Extract YAML frontmatter block from a Markdown file. None if absent."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def validate_sub_skills() -> list[str]:
    """Run skill-manifest.json schema over every sub-skill's frontmatter."""
    if not SKILL_SCHEMA.exists():
        return [f"schema not found: {SKILL_SCHEMA}"]
    schema = load_yaml_file(SKILL_SCHEMA)
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    references = ROOT / "references"
    for sub_dir in SUB_SKILL_DIRS:
        for path in (references / sub_dir).glob("*.md"):
            # Skip templates and READMEs
            if path.name.startswith("_") or path.name.lower() == "readme.md":
                continue
            fm = parse_frontmatter(path)
            if fm is None:
                errors.append(f"{path.relative_to(ROOT)}: missing frontmatter")
                continue
            fm_for_schema = _stringify_dates(fm)
            for v in validator.iter_errors(fm_for_schema):
                errors.append(f"{path.relative_to(ROOT)}: schema: {v.message}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument(
        "--soft", action="store_true",
        help="print errors but exit 0 (useful in pre-merge advisory mode)",
    )
    args = parser.parse_args()

    failures = validate_error_log() + validate_sub_skills()

    if not failures:
        print("validate_rules.py: clean")
        return 0

    for line in failures:
        print(line, file=sys.stderr)
    print(f"\n{len(failures)} validation error(s)", file=sys.stderr)
    return 0 if args.soft else 1


if __name__ == "__main__":
    raise SystemExit(main())
