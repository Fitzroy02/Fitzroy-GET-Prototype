# tests/test_civic_meta.py

import builtins
from datetime import datetime
import pytest
import streamlit as st

try:
    from zoneinfo import ZoneInfo
except Exception:
    from backports.zoneinfo import ZoneInfo

from civic_meta import render_scaffold_stamp

class Capture:
    def __init__(self):
        self.value = None
    def __call__(self, s):
        self.value = s


@pytest.fixture(autouse=True)
def capture_caption(monkeypatch):
    cap = Capture()
    monkeypatch.setattr(st, "caption", cap)
    return cap


def test_naive_default_utc(capture_caption):
    # naive datetime assumed UTC, choose a date in November -> GMT
    dt = datetime(2025, 11, 19, 12, 0)
    render_scaffold_stamp(dt)
    assert "Scaffolded on" in capture_caption.value
    assert "GMT" in capture_caption.value or "BST" in capture_caption.value


def test_naive_explicit_source_tz(capture_caption):
    # naive datetime that should be treated as Europe/Berlin (CET/CEST)
    dt = datetime(2025, 7, 1, 12, 0)
    render_scaffold_stamp(dt, source_tz="Europe/Berlin")
    assert "Scaffolded on" in capture_caption.value
    assert "BST" in capture_caption.value or "GMT" in capture_caption.value


def test_aware_non_london_zone(capture_caption):
    # create an aware datetime in America/New_York and ensure it converts
    dt = datetime(2025, 7, 1, 8, 0, tzinfo=ZoneInfo("America/New_York"))
    render_scaffold_stamp(dt)
    assert "Scaffolded on" in capture_caption.value
    # London in July should be BST
    assert "BST" in capture_caption.value


def test_invalid_source_tz_raises():
    dt = datetime(2025, 7, 1, 12, 0)
    with pytest.raises(ValueError):
        render_scaffold_stamp(dt, source_tz="NoSuchZone")
