# ruff: noqa: I001
"""Tests for tools/render_loaders.py.

The strict drift-check (`render --check`) is exercised in CI under the
`loaders-and-table-no-drift` job — it requires jinja2 + an exact rendering
match. Locally we only assert that the source-of-truth file is valid and
that all referenced paths exist, so the test suite stays green even when
jinja2 isn't installed.

I001 is disabled because the render_loaders import depends on a
sys.path.insert that has to run between the top-level imports and
the test-target import.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import render_loaders as rl  # noqa: E402


def test_index_yml_exists():
    assert rl.INDEX.exists(), "references/_index.yml is the source of truth"


def test_index_yml_is_valid():
    data = yaml.safe_load(rl.INDEX.read_text(encoding="utf-8"))
    assert "meta" in data
    assert data["meta"].get("name")
    assert "skills" in data
    assert len(data["skills"]) > 0


def test_all_skills_have_paths():
    data = yaml.safe_load(rl.INDEX.read_text(encoding="utf-8"))
    for s in data["skills"]:
        path = ROOT / s["path"]
        assert path.exists(), f"skill {s['id']} points at missing path {s['path']}"


def test_loaders_section_present_for_each_skill():
    data = yaml.safe_load(rl.INDEX.read_text(encoding="utf-8"))
    for s in data["skills"]:
        assert "claude" in s["loaders"]
        assert "gemini" in s["loaders"]
        assert "skill_resource" in s["loaders"]
