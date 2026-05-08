"""Tests for tools/generate-dashboard.py parsing."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Load `generate-dashboard.py` (filename has a hyphen, so we use importlib)
_spec = importlib.util.spec_from_file_location(
    "generate_dashboard",
    ROOT / "tools" / "generate-dashboard.py",
)
assert _spec and _spec.loader
gd = importlib.util.module_from_spec(_spec)
sys.modules["generate_dashboard"] = gd
_spec.loader.exec_module(gd)


def test_parses_existing_repo_log():
    """The committed error-log.md must produce real entries (not empty)."""
    entries = gd.parse_error_log(ROOT / "references" / "errors" / "error-log.md")
    assert len(entries) >= 2, "expected at least two real entries"
    # Multi-line block scalars must come through populated, not empty.
    for e in entries:
        assert e.get("context"), f"empty context in {e.get('id')}"
        assert e.get("new_rule"), f"empty new_rule in {e.get('id')}"


def test_template_excluded():
    """Template placeholder entries (ERR-YYYY-NNN) must be filtered out."""
    entries = gd.parse_error_log(ROOT / "references" / "errors" / "error-log.md")
    for e in entries:
        assert "YYYY" not in str(e.get("id", "")), \
            f"template placeholder leaked through: {e.get('id')}"


def test_count_tokens_returns_positive():
    n = gd.count_tokens("hello world this is a test")
    assert n > 0


def test_safe_neutralises_script_breakout():
    out = gd._safe("</script><script>alert(1)</script>")
    assert "</script>" not in out
    assert r"<\/script>" in out
    assert "&lt;" in out  # also HTML-escaped


def test_sanitize_recursive():
    data = {"a": ["</script>", {"b": "</script>"}], "c": "ok"}
    out = gd.sanitize(data)
    assert "</script>" not in out["a"][0]
    assert "</script>" not in out["a"][1]["b"]
    assert "ok" in out["c"]
