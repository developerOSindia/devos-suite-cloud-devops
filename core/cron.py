"""
Pure business logic for cron expression parsing and explanation.
Zero Streamlit or UI dependencies.
"""

from typing import Dict, Any


def explain_cron_expression(expression: str) -> Dict[str, Any]:
    """Parses a standard 5-part cron expression and provides human-readable explanations."""
    parts = expression.strip().split()
    if len(parts) != 5:
        return {
            "is_valid": False,
            "error": f"Cron expression must contain exactly 5 parts (received {len(parts)}). Format: 'minute hour day-of-month month day-of-week'",
            "human_readable": "",
            "parts": {}
        }

    minute, hour, dom, month, dow = parts

    def humanize_part(val: str, unit: str) -> str:
        if val == "*":
            return f"every {unit}"
        elif val.startswith("*/"):
            return f"every {val[2:]} {unit}s"
        elif "," in val:
            return f"at {unit}s {val}"
        return f"at {unit} {val}"

    explanation = (
        f"Runs {humanize_part(minute, 'minute')}, "
        f"{humanize_part(hour, 'hour')}, "
        f"{humanize_part(dom, 'day of month')}, "
        f"{humanize_part(month, 'month')}, "
        f"{humanize_part(dow, 'day of week')}."
    )

    return {
        "is_valid": True,
        "error": None,
        "human_readable": explanation,
        "parts": {
            "minute": minute,
            "hour": hour,
            "day_of_month": dom,
            "month": month,
            "day_of_week": dow,
        }
    }
