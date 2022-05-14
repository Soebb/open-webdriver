"""
    Tests the open_webdriver package.
"""

import os
import unittest

from open_webdriver import open_webdriver

FULL_TESTS = os.environ.get("FULL_TESTS", "0") == "0"

if FULL_TESTS:
    all_drivers = ["chrome", "firefox", "brave"]
else:
    all_drivers = ["chrome"]


def do_google_test(driver_name: str, headless: bool) -> bool:
    """Runs the tests for a given driver."""
    with open_webdriver(driver_name=driver_name, headless=headless, verbose=True) as driver:
        driver.get("https://www.google.com")
        return driver.title == "Google"


class OpenWebDriverTests(unittest.TestCase):
    """Tester for open_webdriver.py"""

    def test_google(self) -> None:
        """Tests that google test works."""
        for driver in all_drivers:
            ok = do_google_test(driver, headless=False)  # pylint: disable=invalid-name
            self.assertTrue(ok)

    def test_google_headless(self) -> None:
        """Tests that google headless works."""
        for driver in all_drivers:
            ok = do_google_test(driver, headless=True)  # pylint: disable=invalid-name
            self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
