# civic_meta.py

from datetime import datetime
from typing import Optional
import streamlit as st

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:
    from backports.zoneinfo import ZoneInfo
    # backports.zoneinfo doesn't expose ZoneInfoNotFoundError on older versions; define a local alias
    class ZoneInfoNotFoundError(Exception):
        pass

def render_scaffold_stamp(timestamp: datetime, source_tz: Optional[str] = "UTC") -> None:
    """
    🕊️ Civic Timestamp Renderer

    Marks the moment of scaffolding in London time (BST/GMT), honoring ethical presence.

    Parameters:
    - timestamp: datetime object (aware or naive).
    - source_tz: IANA timezone name for naive input (default: "UTC"). If None and timestamp is naive, ValueError is raised.

    Raises:
    - ValueError if timestamp is naive and no source_tz is provided, or if source_tz is invalid.
    """
    if timestamp.tzinfo is None:
        if source_tz is None:
            raise ValueError("Naive datetime provided; set source_tz or provide an aware datetime.")
        try:
            timestamp = timestamp.replace(tzinfo=ZoneInfo(source_tz))
        except ZoneInfoNotFoundError:
            raise ValueError(f"Unknown source timezone: {source_tz}")

    try:
        london = timestamp.astimezone(ZoneInfo("Europe/London"))
    except ZoneInfoNotFoundError:
        raise ValueError("Local timezone 'Europe/London' not found on this system")

    formatted_time = london.strftime("%d %b %Y, %H:%M %Z")
    st.caption(f"Scaffolded on {formatted_time}")
