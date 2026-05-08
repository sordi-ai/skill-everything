#!/usr/bin/env python3
"""
generate-dashboard.py - Parses references/errors/error-log.md + git history
                       -> updates docs/dashboard.html

Usage:
    python tools/generate-dashboard.py

Reads:
    references/errors/error-log.md  (YAML fenced blocks)
    git log --all                   (commit subjects)
    references/**/*.md              (token counts via tiktoken)

Writes:
    docs/dashboard.html             (replaces JSON data block in-place)

Notes:
    * Uses pyyaml.safe_load for the error log (not regex). Multi-line block
      scalars (|) are preserved.
    * Uses tiktoken cl100k_base for accurate token counts (no chars//4).
    * All user-controlled strings are HTML-escaped before JSON embedding,
      and </ is replaced by <\\/ to prevent script-tag breakout.
"""

from __future__ import annotations

import html as _html
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
except ImportError:
    _ENC = None  # graceful fallback in environments without tiktoken

ROOT = Path(__file__).resolve().parent.parent
ERROR_LOG = ROOT / "references" / "errors" / "error-log.md"
DASHBOARD = ROOT / "docs" / "dashboard.html"


# ---------- safety helpers ----------

def _safe(v: Any) -> Any:
    """HTML-escape a string and neutralise </ to prevent script-tag breakout."""
    if isinstance(v, str):
        return _html.escape(v, quote=True).replace("</", r"<\/")
    return v


def sanitize(d: Any) -> Any:
    """Recursively sanitize all strings in a nested structure."""
    if isinstance(d, dict):
        return {k: sanitize(v) for k, v in d.items()}
    if isinstance(d, list):
        return [sanitize(x) for x in d]
    return _safe(d)


# ---------- parsing ----------

def parse_error_log(path: Path) -> list[dict]:
    """Extract error entries from YAML fenced blocks in error-log.md."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    entries: list[dict] = []
    for block in re.findall(r"```yaml\s*\n(.*?)```", text, re.DOTALL):
        try:
            doc = yaml.safe_load(block)
        except yaml.YAMLError as e:
            print(f"WARN: invalid YAML block: {e}", file=sys.stderr)
            continue
        if doc is None:
            continue
        # Schema allows either {errors: [...]} or a bare list, or single dict
        if isinstance(doc, dict) and "errors" in doc:
            items = doc["errors"]
        elif isinstance(doc, list):
            items = doc
        else:
            items = [doc]
        for entry in items or []:
            if not isinstance(entry, dict):
                continue
            # Skip template placeholder entries
            if "YYYY" in str(entry.get("id", "")):
                continue
            entries.append(entry)
    return entries


def get_learn_commits() -> list[dict]:
    """Get all learn(...) commits from git history."""
    try:
        result = subprocess.run(
            ["git", "log", "--all", "--format=%H|%aI|%s"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", cwd=ROOT, check=False,
        )
    except FileNotFoundError:
        return []
    if result.returncode != 0:
        return []
    commits = []
    for line in (result.stdout or "").strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) == 3 and "learn(" in parts[2]:
            commits.append({
                "hash": parts[0][:7],
                "date": parts[1][:10],
                "message": parts[2],
            })
    return commits


# ---------- token math ----------

def count_tokens(text: str) -> int:
    """Real tiktoken count if available, else conservative chars/3.25 estimate."""
    if _ENC is not None:
        return len(_ENC.encode(text))
    # Fallback: Markdown with code/backticks/YAML averages ~1 token / 3.25 chars
    return len(text) // 3 + (len(text) % 3 > 0)


def count_rules_in_file(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    return len(re.findall(r"^\d+\.\s", text, re.MULTILINE))


def get_skill_stats() -> list[dict]:
    """Token count + rule count per sub-skill."""
    files = [
        ("Code Quality", ROOT / "references" / "development" / "code-quality.md"),
        ("Python", ROOT / "references" / "development" / "python.md"),
        ("TypeScript", ROOT / "references" / "development" / "typescript.md"),
        ("React", ROOT / "references" / "development" / "react.md"),
        ("Git Conventions", ROOT / "references" / "git" / "conventions.md"),
        ("Review & Deployment", ROOT / "references" / "process" / "review-deployment.md"),
    ]
    skills = []
    for name, path in files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        skills.append({
            "name": name,
            "rules": count_rules_in_file(path),
            "tokens": count_tokens(text),
        })
    return skills


# ---------- dashboard data build ----------

def build_data(entries: list[dict], commits: list[dict]) -> dict:
    dates: list[str] = []
    categories: Counter = Counter()
    severity: Counter = Counter()
    monthly: dict[str, int] = defaultdict(int)
    total_count = 0

    for e in entries:
        d = str(e.get("date", "") or "")
        if d:
            dates.append(d)
        categories[str(e.get("category", "unknown"))] += 1
        severity[str(e.get("severity", "medium"))] += 1
        try:
            count = int(e.get("count", 1))
        except (TypeError, ValueError):
            count = 1
        total_count += count
        if d and len(d) >= 7:
            monthly[d[:7]] += 1

    for c in commits:
        if c["date"] and len(c["date"]) >= 7:
            m = c["date"][:7]
            monthly.setdefault(m, 0)
            monthly[m] += 0  # commit presence is informational; see entries[].count for "prevented"

    today = datetime.now().strftime("%Y-%m-%d")
    date_from = min(dates) if dates else today
    date_to = max(dates) if dates else today

    total_errors = len(entries)
    errors_prevented = max(0, total_count - total_errors)

    skills = get_skill_stats()
    total_rules = sum(s["rules"] for s in skills)

    recent = []
    for e in sorted(entries, key=lambda x: str(x.get("date", "")), reverse=True)[:5]:
        desc = (
            e.get("what_happened")
            or e.get("description")
            or e.get("new_rule")
            or ""
        )
        desc = str(desc)
        if len(desc) > 80:
            desc = desc[:77] + "..."
        recent.append({
            "id": str(e.get("id", "?")),
            "date": str(e.get("date", "?")),
            "severity": str(e.get("severity", "medium")),
            "description": desc,
        })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "date_range": {"from": date_from, "to": date_to},
        "summary": {
            "total_errors": total_errors,
            "total_rules": total_rules,
            "errors_prevented": errors_prevented,
            "categories": dict(categories),
            "severity": dict(severity),
            "monthly": [{"month": m, "count": c} for m, c in sorted(monthly.items())],
        },
        "recent": recent,
        "skills": skills,
    }


def inject_data(html_path: Path, data: dict) -> None:
    """Replace the JSON data block in dashboard.html. All strings are sanitised."""
    if not html_path.exists():
        raise SystemExit(f"Dashboard not found: {html_path}")
    html_text = html_path.read_text(encoding="utf-8")
    payload = json.dumps(sanitize(data), indent=2, ensure_ascii=False)
    pattern = r'(<script id="data" type="application/json">)\s*\n.*?\n(</script>)'
    new_html = re.sub(
        pattern,
        lambda m: m.group(1) + "\n" + payload + "\n" + m.group(2),
        html_text,
        flags=re.DOTALL,
    )
    html_path.write_text(new_html, encoding="utf-8")


def main() -> int:
    if not ERROR_LOG.exists():
        print(f"Error log not found: {ERROR_LOG}", file=sys.stderr)
        return 1
    if not DASHBOARD.exists():
        print(f"Dashboard not found: {DASHBOARD}", file=sys.stderr)
        return 1

    entries = parse_error_log(ERROR_LOG)
    commits = get_learn_commits()
    data = build_data(entries, commits)
    inject_data(DASHBOARD, data)

    print(f"Dashboard updated: {DASHBOARD}")
    print(f"  Errors logged:    {data['summary']['total_errors']}")
    print(f"  Rules across subs: {data['summary']['total_rules']}")
    print(f"  Errors prevented: {data['summary']['errors_prevented']}")
    print(f"  Sub-skills:       {len(data['skills'])}")
    if _ENC is None:
        print("  NOTE: tiktoken not installed; token counts use chars/3 fallback.",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
