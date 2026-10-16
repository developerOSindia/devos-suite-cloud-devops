"""
Unit tests for suite-cloud-devops business logic.
"""

import sys
import unittest
from pathlib import Path

# Ensure suite root is in sys.path
SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.cron import explain_cron_expression


class TestCronParser(unittest.TestCase):
    def test_standard_expression(self):
        res = explain_cron_expression("*/5 * * * *")
        self.assertTrue(res["is_valid"])
        self.assertIn("every 5 minutes", res["human_readable"])
        self.assertEqual(res["parts"]["minute"], "*/5")

    def test_invalid_part_count(self):
        res = explain_cron_expression("*/5 * *")
        self.assertFalse(res["is_valid"])
        self.assertIn("exactly 5 parts", res["error"])


if __name__ == "__main__":
    unittest.main()
