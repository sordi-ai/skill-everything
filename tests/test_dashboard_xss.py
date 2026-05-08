"""XSS regression tests for the dashboard pipeline."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "generate_dashboard",
    ROOT / "tools" / "generate-dashboard.py",
)
assert _spec and _spec.loader
gd = importlib.util.module_from_spec(_spec)
sys.modules["generate_dashboard"] = gd
_spec.loader.exec_module(gd)


def test_payload_in_what_happened_does_not_break_script_block(tmp_path):
    """
    Build a fake data dict containing the classic </script>-breakout payload
    and confirm that the resulting JSON cannot end the <script> wrapper.
    """
    payload = "</script><script>alert('xss')</script>"
    data = {
        "summary": {"total_errors": 1},
        "recent": [{"id": "ERR-T-001", "date": "2026-05-08",
                    "severity": "high", "description": payload}],
    }
    sanitised = gd.sanitize(data)
    import json
    serialised = json.dumps(sanitised, ensure_ascii=False)
    # Exact </script> must not survive
    assert "</script>" not in serialised
    # Either escaped or HTML-entity form must be present
    assert (r"<\/script>" in serialised) or ("&lt;" in serialised)
    # The injected attacker payload `alert('xss')` is allowed inside escaped JSON;
    # the safety contract is only about not breaking the script wrapper.


def test_dashboard_html_round_trip_keeps_safety(tmp_path):
    """
    Inject sanitised data into a minimal dashboard.html template and assert
    that the </script> sequence inside an attacker string did not survive.
    """
    template = tmp_path / "dash.html"
    template.write_text(
        '<html><body>'
        '<script id="data" type="application/json">\n'
        '{"placeholder": true}\n'
        '</script>'
        '</body></html>',
        encoding="utf-8",
    )
    data = {
        "recent": [{"id": "ERR-T-002", "date": "2026-05-08",
                    "severity": "low",
                    "description": "</script><script>alert(1)</script>"}],
    }
    gd.inject_data(template, data)
    out = template.read_text(encoding="utf-8")
    # Find the position of the closing </script> that ends the data block.
    # If the attacker payload had survived intact, there would be an EXTRA
    # </script> earlier in the document. Count: must be exactly 1 closing tag.
    assert out.count("</script>") == 1, (
        "Attacker-controlled </script> survived sanitisation - "
        "XSS regression!"
    )
