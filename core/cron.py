"""
Pure business logic for cron expression parsing and explanation.
Zero Streamlit or UI dependencies.
"""

from typing import Dict, Any


def explain_cron_expression(expression: str) -> Dict[str, Any]:
    """Parses a standard 5-part cron expression and provides human-readable explanations."""
    if not expression or not expression.strip():
        return {
            "is_valid": False,
            "error": "Cron expression cannot be empty.",
            "human_readable": "",
            "parts": {}
        }

    parts = expression.strip().split()
    if len(parts) != 5:
        return {
            "is_valid": False,
            "error": f"Cron expression must contain exactly 5 parts (received {len(parts)}). Format: 'minute hour day-of-month month day-of-week'",
            "human_readable": "",
            "parts": {}
        }

    minute, hour, dom, month, dow = parts

    # Validate part ranges
    limits = [
        (minute, 0, 59, "minute"),
        (hour, 0, 23, "hour"),
        (dom, 1, 31, "day-of-month"),
        (month, 1, 12, "month"),
        (dow, 0, 7, "day-of-week"),
    ]

    for val, min_val, max_val, name in limits:
        if val == "*":
            continue
        # Check simple integer or step
        sub_vals = val.split(",")
        for sv in sub_vals:
            if sv.startswith("*/"):
                step_str = sv[2:]
                if not step_str.isdigit() or int(step_str) < 1 or int(step_str) > max_val:
                    return {
                        "is_valid": False,
                        "error": f"Invalid step '{sv}' for {name} (valid step: 1-{max_val}).",
                        "human_readable": "",
                        "parts": {}
                    }
            elif "-" in sv:
                r_parts = sv.split("-")
                if len(r_parts) == 2 and r_parts[0].isdigit() and r_parts[1].isdigit():
                    start, end = int(r_parts[0]), int(r_parts[1])
                    if start < min_val or end > max_val or start > end:
                        return {
                            "is_valid": False,
                            "error": f"Invalid range '{sv}' for {name} (valid range: {min_val}-{max_val}).",
                            "human_readable": "",
                            "parts": {}
                        }
            elif sv.isdigit():
                num = int(sv)
                if num < min_val or num > max_val:
                    return {
                        "is_valid": False,
                        "error": f"Value '{num}' out of bounds for {name} (valid: {min_val}-{max_val}).",
                        "human_readable": "",
                        "parts": {}
                    }

    def humanize_part(val: str, unit: str) -> str:
        if val == "*":
            return f"every {unit}"
        elif val.startswith("*/"):
            return f"every {val[2:]} {unit}s"
        elif "-" in val:
            return f"from {unit} {val.replace('-', ' through ')}"
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
