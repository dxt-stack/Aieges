"""
AEGIS Utility Helpers
"""

from datetime import datetime, timezone


def utc_now_iso() -> str:
    """Returns current UTC timestamp in ISO-8601 string format."""
    return datetime.now(timezone.utc).isoformat()
