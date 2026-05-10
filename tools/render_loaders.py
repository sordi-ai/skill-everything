#!/usr/bin/env python3
"""
render_loaders.py - Regenerates SKILL.md, CLAUDE.md, GEMINI.md, .cursorrules,
                    AGENTS.md, and .cursor/rules/<name>.mdc files from
                    skills/_index.yml. CI fails if outputs drift.

Usage:
    python tools/render_loaders.py
    python tools/render_loaders.py --check     # exit 1 on drift, no write

Templates live under tools/templates/*.j2.

This is the single source of truth machinery: editing CLAUDE.md, GEMINI.md,
.cursorrules, AGENTS.md, or .cursor/rules/* directly will be overwritten on
the next pre-commit / CI run. Edit skills/_index.yml (or the source SKILL.md
files for per-skill .mdc body content) instead.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import jinja2
import yaml

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "skills" / "_index.yml"
TEMPLATES = ROOT / "tools" / "templates"

# Static targets — one template renders one output at a fixed path.
# Output filenames are written to the repo root. The Cursor loaders
# (.cursorrules + .cursor/rules/) must live at the repo root because
# Cursor only auto-discovers them when adjacent to the project root.
STATIC_TARGETS = [
    ("SKILL.md",     "skill.md.j2"),
    ("CLAUDE.md",    "claude.md.j2"),
    ("GEMINI.md",    "gemini.md.j2"),
    (".cursorrules", "cursorrules.j2"),
    ("AGENTS.md",    "agents.md.j2"),
]

# Per-skill targets — one template renders one output per skill in
# skills/_index.yml. The output_pattern is a Path-style template with
# `{id}` substituted from each skill entry.
PER_SKILL_TARGETS = [
    (".cursor/rules/{id}.mdc", "cursor-rule.mdc.j2"),
]

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)", re.DOTALL)


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """Split a Markdown file with YAML frontmatter into (frontmatter dict, body str).
    Returns ({}, text) when no frontmatter is present."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    fm = yaml.safe_load(match.group(1)) or {}
    if not isinstance(fm, dict):
        fm = {}
    return fm, match.group(2)


def render(check: bool = False) -> int:
    if not INDEX.exists():
        print(f"missing: {INDEX}", file=sys.stderr)
        return 1
    if not TEMPLATES.is_dir():
        print(f"missing: {TEMPLATES}", file=sys.stderr)
        return 1

    data = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    drift = False

    # Static targets
    for output_name, template_name in STATIC_TARGETS:
        template = env.get_template(template_name)
        rendered = template.render(**data)
        out_path = ROOT / output_name
        if check:
            existing = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
            if existing != rendered:
                drift = True
                print(f"DRIFT: {output_name}", file=sys.stderr)
        else:
            out_path.write_text(rendered, encoding="utf-8")
            print(f"wrote: {output_name}")

    # Per-skill targets
    for output_pattern, template_name in PER_SKILL_TARGETS:
        template = env.get_template(template_name)
        for skill in data["skills"]:
            skill_path = ROOT / skill["path"]
            if not skill_path.exists():
                print(
                    f"warn: skill source missing for {skill['id']}: {skill_path}",
                    file=sys.stderr,
                )
                continue
            skill_text = skill_path.read_text(encoding="utf-8")
            skill_fm, body = _split_frontmatter(skill_text)
            rendered = template.render(
                meta=data["meta"],
                skill=skill,
                skill_fm=skill_fm,
                body=body,
            )
            out_name = output_pattern.format(id=skill["id"])
            out_path = ROOT / out_name
            if check:
                existing = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
                if existing != rendered:
                    drift = True
                    print(f"DRIFT: {out_name}", file=sys.stderr)
            else:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(rendered, encoding="utf-8")
                print(f"wrote: {out_name}")

    if check and drift:
        print(
            "\nrender_loaders.py: drift detected. Run "
            "`python tools/render_loaders.py` and commit the regenerated files.",
            file=sys.stderr,
        )
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--check", action="store_true",
                        help="fail with exit 1 if outputs would change (CI use)")
    args = parser.parse_args()
    return render(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
