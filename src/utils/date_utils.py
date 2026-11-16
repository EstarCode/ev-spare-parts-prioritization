# Date Parsing and UTC ISO 8601 Timestamp Utility Module.
from datetime import datetime, timezone

# Return current UTC timestamp in ISO 8601 format.
def get_utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

# Return current date string YYYY-MM-DD.
def get_current_date_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Attempt to parse various date formats into ISO 8601 YYYY-MM-DD, or return original string.
def parse_flexible_date(date_str: str) -> str:
    if not date_str:
        return ""
    clean_str = date_str.strip()
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%b %d, %Y",
        "%B %d, %Y",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(clean_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return clean_str
