#!/usr/bin/env python3
"""
render_loaders.py - Regenerates SKILL.md, CLAUDE.md, GEMINI.md, .cursorrules
                    from skills/_index.yml. CI fails if outputs drift.

Usage:
    python tools/render_loaders.py
    python tools/render_loaders.py --check     # exit 1 on drift, no write

Templates live under tools/templates/*.j2.

This is the single source of truth machinery: editing CLAUDE.md, GEMINI.md or
.cursorrules directly will be overwritten on the next pre-commit / CI run.
Edit skills/_index.yml instead.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import jinja2
import yaml

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "skills" / "_index.yml"
TEMPLATES = ROOT / "tools" / "templates"

# Each tuple: (output filename, template filename).
# Output filenames are written to the repo root (ROOT). The Cursor loader
# must live at the repo root as `.cursorrules` — Cursor only auto-discovers
# the file when it sits next to the project root.
TARGETS = [
    ("SKILL.md",     "skill.md.j2"),
    ("CLAUDE.md",    "claude.md.j2"),
    ("GEMINI.md",    "gemini.md.j2"),
    (".cursorrules", "cursorrules.j2"),
]


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
    for output_name, template_name in TARGETS:
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
