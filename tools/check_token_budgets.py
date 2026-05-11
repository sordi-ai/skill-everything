#!/usr/bin/env python3
"""
check_token_budgets.py - Verify each skills/<name>/SKILL.md actual tiktoken
                         (cl100k_base) count is within its frontmatter
                         tokens_target. Backs the README's "per-skill 3K
                         token cap, CI-enforced" claim with a real check.

Usage:
    python tools/check_token_budgets.py
    python tools/check_token_budgets.py --tolerance 50

Exit code 0 on clean, 1 on any over-budget skill. The tolerance flag lets
small overshoots through (default 0); useful when render_readme_table.py
buckets to the nearest 50 and the README rounding is the source of small
drift. Real skill content + frontmatter are both counted (matches the
README token-table calculation).

If a skill is over budget, the message tells the author the two options:
trim the body, or bump tokens_target in the frontmatter (within the
schema's hard cap of 3000).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

try:
    import tiktoken

    _ENC = tiktoken.get_encoding("cl100k_base")
except ImportError:
    _ENC = None

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def count_tokens(text: str) -> int:
    if _ENC is not None:
        return len(_ENC.encode(text))
    # Fallback: ~1 token / 3 chars for Markdown with code blocks.
    # Matches render_readme_table.py's fallback so the two scripts agree.
    return len(text) // 3 + (len(text) % 3 > 0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument(
        "--tolerance",
        type=int,
        default=0,
        help="Allow actual count to exceed tokens_target by N tokens (default 0).",
    )
    args = parser.parse_args()

    if not SKILLS_DIR.is_dir():
        print(f"missing: {SKILLS_DIR}", file=sys.stderr)
        return 1

    failures: list[str] = []
    rows: list[tuple[str, int, int]] = []

    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        # Skip placeholder templates (e.g. skills/_template/SKILL.md).
        if skill_md.parent.name.startswith("_"):
            continue
        text = skill_md.read_text(encoding="utf-8")
        rel = skill_md.relative_to(ROOT).as_posix()
        match = _FRONTMATTER_RE.match(text)
        if not match:
            failures.append(f"{rel}: missing frontmatter")
            continue
        try:
            fm = yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            failures.append(f"{rel}: yaml parse error: {e}")
            continue
        if not isinstance(fm, dict):
            failures.append(f"{rel}: frontmatter is not a YAML mapping")
            continue
        target = fm.get("tokens_target")
        if not isinstance(target, int):
            failures.append(f"{rel}: tokens_target missing or not an integer")
            continue
        actual = count_tokens(text)
        rows.append((rel, actual, target))
        if actual > target + args.tolerance:
            over_by = actual - target
            failures.append(
                f"{rel}: actual {actual} tokens > target {target} (over by {over_by}). "
                f"Trim the body, or bump tokens_target in the frontmatter "
                f"(schema cap 3000)."
            )

    # Summary table on stdout (always shown, success or failure).
    if rows:
        col1 = max(len(r[0]) for r in rows)
        print(f"{'skill':<{col1}}  actual  target")
        print(f"{'-' * col1}  ------  ------")
        for rel, actual, target in rows:
            mark = " " if actual <= target + args.tolerance else " *"
            print(f"{rel:<{col1}}  {actual:>6}  {target:>6}{mark}")
        if _ENC is None:
            print(
                "\n  Note: tiktoken not installed; using chars/3 fallback. "
                "Install `tiktoken>=0.7` for accurate numbers."
            )

    if failures:
        print("", file=sys.stderr)
        for f in failures:
            print(f, file=sys.stderr)
        print(
            f"\n{len(failures)} skill(s) over budget (tolerance {args.tolerance})",
            file=sys.stderr,
        )
        return 1

    print("\ncheck_token_budgets.py: clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
