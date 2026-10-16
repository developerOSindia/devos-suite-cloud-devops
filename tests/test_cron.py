"""
Unit tests for suite-cloud-devops cron parser business logic.
"""

import sys
import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.cron import explain_cron_expression


class TestCron(unittest.TestCase):
    def test_standard_every_minute(self):
        res = explain_cron_expression("* * * * *")
        self.assertTrue(res["is_valid"])
        self.assertIn("Runs every minute, every hour", res["human_readable"])
        self.assertEqual(res["parts"]["minute"], "*")

    def test_daily_midnight(self):
        res = explain_cron_expression("0 0 * * *")
        self.assertTrue(res["is_valid"])
        self.assertIn("at minute 0", res["human_readable"])
        self.assertIn("at hour 0", res["human_readable"])

    def test_step_schedule(self):
        res = explain_cron_expression("*/15 * * * *")
        self.assertTrue(res["is_valid"])
        self.assertIn("every 15 minutes", res["human_readable"])

    def test_weekday_range(self):
        res = explain_cron_expression("0 9 * * 1-5")
        self.assertTrue(res["is_valid"])
        self.assertIn("1 through 5", res["human_readable"])

    def test_invalid_parts_count(self):
        res = explain_cron_expression("* * *")
        self.assertFalse(res["is_valid"])
        self.assertIn("must contain exactly 5 parts", res["error"])

    def test_out_of_bounds_minute(self):
        res = explain_cron_expression("65 * * * *")
        self.assertFalse(res["is_valid"])
        self.assertIn("out of bounds for minute", res["error"])

    def test_empty_input(self):
        res = explain_cron_expression("")
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["error"], "Cron expression cannot be empty.")

    def test_none_input(self):
        res = explain_cron_expression(None)
        self.assertFalse(res["is_valid"])


if __name__ == "__main__":
    unittest.main()
