#!/usr/bin/env python3
"""
generate-dashboard.py — Parses error-log.md + git history → updates dashboard.html

Usage:
    python3 tools/generate-dashboard.py

Reads:  references/errors/error-log.md, git log
Writes: docs/dashboard.html (updates the JSON data block)
"""

import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERROR_LOG = ROOT / "references" / "errors" / "error-log.md"
DASHBOARD = ROOT / "docs" / "dashboard.html"


def parse_error_log(path):
    """Extract YAML error entries from error-log.md."""
    text = path.read_text(encoding="utf-8")
    yaml_blocks = re.findall(r"```yaml\s*\n(.*?)```", text, re.DOTALL)

    entries = []
    for block in yaml_blocks:
        chunks = re.split(r"\n\s*- id:", block)
        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            if not chunk.startswith("id:") and not chunk.startswith("ERR-"):
                if "id:" not in chunk:
                    continue
                chunk = chunk[chunk.index("id:"):]
            if not chunk.startswith("id:"):
                chunk = "id: " + chunk

            entry = {}
            for line in chunk.split("\n"):
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("["):
                    continue
                m = re.match(r"^(\w[\w_]*):\s*(.+)$", line)
                if m:
                    key, val = m.group(1), m.group(2).strip().strip('"').strip("'")
                    val = re.sub(r"\s*#.*$", "", val).strip()
                    if val and val != "|":
                        entry[key] = val

            if "id" in entry and "YYYY" not in entry["id"]:
                entries.append(entry)

    return entries


def get_learn_commits():
    """Get all learn() commits from git history."""
    try:
        result = subprocess.run(
            ["git", "log", "--all", "--oneline", "--format=%H|%aI|%s"],
            capture_output=True, text=True, cwd=ROOT,
        )
        commits = []
        for line in result.stdout.strip().split("\n"):
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
    except FileNotFoundError:
        return []


def count_rules_in_file(path):
    """Count numbered rules (lines starting with digits followed by a dot)."""
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    return len(re.findall(r"^\d+\.\s", text, re.MULTILINE))


def get_skill_stats():
    """Get token count and rule count per sub-skill."""
    dev = ROOT / "references" / "development"
    skills = []
    files = [
        ("Code Quality", dev / "code-quality.md"),
        ("Python", dev / "python.md"),
        ("TypeScript", dev / "typescript.md"),
        ("React", dev / "react.md"),
        ("Git Conventions", ROOT / "references" / "git" / "conventions.md"),
        ("Review & Deployment", ROOT / "references" / "process" / "review-deployment.md"),
    ]
    for name, path in files:
        if path.exists():
            chars = len(path.read_text(encoding="utf-8"))
            tokens = chars // 4
            rules = count_rules_in_file(path)
            skills.append({"name": name, "rules": rules, "tokens": tokens})
    return skills


def build_data(entries, commits):
    """Build the JSON data structure for the dashboard."""
    dates = []
    categories = Counter()
    severity = Counter()
    monthly = defaultdict(int)
    total_count = 0

    for e in entries:
        d = e.get("date", "")
        if d:
            dates.append(d)
        cat = e.get("category", "unknown")
        categories[cat] += 1
        sev = e.get("severity", "medium")
        severity[sev] += 1
        count = int(e.get("count", 1))
        total_count += count
        if d and len(d) >= 7:
            monthly[d[:7]] += 1

    for c in commits:
        if c["date"] and len(c["date"]) >= 7:
            m = c["date"][:7]
            if m not in monthly:
                monthly[m] += 1

    if dates:
        date_from = min(dates)
        date_to = max(dates)
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        date_from = date_to = today

    total_errors = len(entries)
    errors_prevented = max(0, total_count - total_errors)

    skills = get_skill_stats()
    total_rules = sum(s["rules"] for s in skills)

    recent = []
    for e in sorted(entries, key=lambda x: x.get("date", ""), reverse=True)[:5]:
        desc = e.get("what_happened", e.get("description", e.get("new_rule", "")))
        if len(desc) > 80:
            desc = desc[:77] + "..."
        recent.append({
            "id": e.get("id", "?"),
            "date": e.get("date", "?"),
            "severity": e.get("severity", "medium"),
            "description": desc,
        })

    sorted_monthly = sorted(monthly.items())

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date_range": {"from": date_from, "to": date_to},
        "summary": {
            "total_errors": total_errors,
            "total_rules": total_rules,
            "errors_prevented": errors_prevented,
            "categories": dict(categories),
            "severity": dict(severity),
            "monthly": [{"month": m, "count": c} for m, c in sorted_monthly],
        },
        "recent": recent,
        "skills": skills,
    }


def inject_data(html_path, data):
    """Replace the JSON data block in dashboard.html."""
    html = html_path.read_text(encoding="utf-8")
    pattern = r'(<script id="data" type="application/json">)\s*\n.*?\n(</script>)'
    replacement = r'\1\n' + json.dumps(data, indent=2) + r'\n\2'
    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    html_path.write_text(new_html, encoding="utf-8")


def main():
    if not ERROR_LOG.exists():
        print(f"Error log not found: {ERROR_LOG}", file=sys.stderr)
        sys.exit(1)
    if not DASHBOARD.exists():
        print(f"Dashboard not found: {DASHBOARD}", file=sys.stderr)
        sys.exit(1)

    entries = parse_error_log(ERROR_LOG)
    commits = get_learn_commits()
    data = build_data(entries, commits)

    inject_data(DASHBOARD, data)

    print(f"Dashboard updated: {DASHBOARD}")
    print(f"  Errors:    {data['summary']['total_errors']}")
    print(f"  Rules:     {data['summary']['total_rules']}")
    print(f"  Prevented: {data['summary']['errors_prevented']}")
    print(f"  Skills:    {len(data['skills'])}")


if __name__ == "__main__":
    main()
