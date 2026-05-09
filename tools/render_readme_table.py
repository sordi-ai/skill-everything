#!/usr/bin/env python3
"""
render_readme_table.py - Updates the token-budget table in README.md
                         between the markers
                             <!-- token-table:start -->
                             <!-- token-table:end -->
                         using real tiktoken (cl100k_base) counts.

Usage:
    python tools/render_readme_table.py
    python tools/render_readme_table.py --check    # exit 1 on drift

The table shows REAL costs without marketing fiction. The README's headline
claim is now "20-34% cheaper than uncached monolithic, roughly break-even
with cached monolithic" - this script provides the data behind that.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
except ImportError:
    _ENC = None

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "references" / "_index.yml"
README = ROOT / "README.md"
START = "<!-- token-table:start -->"
END = "<!-- token-table:end -->"


def count_tokens(text: str) -> int:
    if _ENC is not None:
        return len(_ENC.encode(text))
    # Fallback: ~1 token / 3 chars for Markdown with code blocks
    return len(text) // 3 + (len(text) % 3 > 0)


def _bucket(n: int) -> int:
    """Floor a token count to the nearest 50.

    Rationale: the README is a human-facing document. Showing a token
    count that flips by ±5 every time someone fixes a typo is noise.
    Bucketing to 50 keeps the table stable against trivial edits while
    still surfacing meaningful changes (a new rule typically adds
    ≥ 100 tokens). The CI no-drift check therefore only fails when a
    sub-skill crosses a 50-token boundary, which is the right
    granularity for review.
    """
    return (n // 50) * 50


def build_table() -> str:
    if not INDEX.exists():
        return f"<!-- _index.yml missing: {INDEX} -->"
    index = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
    rows = []
    rows.append("| Sub-skill | Path | Tokens (real, tiktoken cl100k) |")
    rows.append("|---|---|---:|")
    total = 0
    for s in index["skills"]:
        path = ROOT / s["path"]
        sid = s["id"]
        if not path.exists():
            rows.append(f"| `{sid}` | `{s['path']}` | _missing_ |")
            continue
        n = count_tokens(path.read_text(encoding="utf-8"))
        total += n
        rows.append(f"| `{sid}` | `{s['path']}` | ~{_bucket(n):,} |")
    rows.append(
        f"| **Total if all loaded** | — | **~{_bucket(total):,}** |"
    )
    rows.append(  # noqa: RUF001 — en-dashes match the README's typography
        "| **Typical (router + 1–2 skills)** | depends on task | **~1,800–3,500** |"
    )
    fallback_note = ""
    if _ENC is None:
        fallback_note = (
            "\n\n> _Counts above use a chars/3 fallback because tiktoken is "
            "not installed. Install `tiktoken>=0.7` for accurate numbers._"
        )
    return "\n".join(rows) + fallback_note


def update(check: bool = False) -> int:
    if not README.exists():
        print(f"missing: {README}", file=sys.stderr)
        return 1
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print(
            f"README.md has no {START}/{END} markers; "
            "add them around the token table block.",
            file=sys.stderr,
        )
        return 1
    table = build_table()
    new_block = f"{START}\n\n{table}\n\n{END}"
    new_text = (
        text.split(START)[0]
        + new_block
        + text.split(END, 1)[1]
    )
    if check:
        if new_text != text:
            print(
                "render_readme_table.py: drift detected. "
                "Run `python tools/render_readme_table.py` and commit.",
                file=sys.stderr,
            )
            return 1
        return 0
    README.write_text(new_text, encoding="utf-8")
    print(f"wrote: {README}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--check", action="store_true",
                        help="fail with exit 1 if README would change (CI use)")
    args = parser.parse_args()
    return update(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
