#!/usr/bin/env python3
"""
Test suite for the nurture framework.
Tests config loading, scheduling, randomization, platform registration,
and executor flow WITHOUT requiring a real CDP connection.
"""

import os
import sys
import yaml
import json
import unittest
from datetime import datetime, time as dt_time
from unittest.mock import MagicMock, patch

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.cdp_manager import CDPManager
from core.scheduler import Scheduler, TimeWindow
from core.randomizer import Randomizer
from core.executor import Executor, PLATFORM_REGISTRY
from core.base import PlatformNurturer, ActionResult
from core.notifier import Notifier


# ------------------------------------------------------------------
#  Mock CDP Manager for testing
# ------------------------------------------------------------------
class MockCDPManager:
    """Mock CDP manager that doesn't need real Chrome."""

    def __init__(self):
        self.navigated_urls = []
        self.evaluated_expressions = []
        self.screenshots = []

    def navigate(self, url, **kwargs):
        self.navigated_urls.append(url)

    def evaluate(self, expression, return_by_value=True):
        self.evaluated_expressions.append(expression)
        # Return sensible defaults for common checks
        if "logout" in expression.lower():
            return True  # Pretend logged in
        if "settings" in expression.lower() or "account" in expression.lower():
            return True
        return {}

    def screenshot(self, path, full_page=False):
        self.screenshots.append(path)

    def scroll_to(self, y):
        pass

    def scroll_by(self, y):
        pass

    def query_selector(self, selector):
        return MagicMock()

    def query_selector_all(self, selector):
        return []

    def click(self, selector, timeout=5000):
        pass

    def type_text(self, selector, text, delay=15):
        pass

    def keyboard_type(self, text, delay=15):
        pass

    def keyboard_press(self, key):
        pass

    def wait_for_selector(self, selector, timeout=5000):
        pass

    def reload(self):
        pass

    def is_connected(self):
        return True


# ------------------------------------------------------------------
#  Test Cases
# ------------------------------------------------------------------

class TestConfigLoading(unittest.TestCase):
    """Test configuration file loading."""

    def setUp(self):
        self.config_dir = os.path.join(os.path.dirname(__file__), "config")

    def test_platforms_yaml_exists_and_valid(self):
        path = os.path.join(self.config_dir, "platforms.yaml")
        self.assertTrue(os.path.exists(path))
        with open(path) as f:
            data = yaml.safe_load(f)
        self.assertIn("platforms", data)
        platforms = data["platforms"]
        self.assertIn("x_twitter", platforms)
        self.assertIn("reddit", platforms)
        self.assertIn("hackernews", platforms)
        self.assertIn("product_hunt", platforms)

        # Check each platform has required fields
        for name, cfg in platforms.items():
            self.assertIn("weight", cfg, f"{name} missing weight")
            self.assertIn("session_duration", cfg, f"{name} missing session_duration")
            self.assertIn("actions", cfg, f"{name} missing actions")

    def test_schedule_yaml_exists_and_valid(self):
        path = os.path.join(self.config_dir, "schedule.yaml")
        self.assertTrue(os.path.exists(path))
        with open(path) as f:
            data = yaml.safe_load(f)
        self.assertIn("windows", data)
        self.assertIn("global", data)
        windows = data["windows"]
        self.assertIn("morning", windows)
        self.assertIn("noon", windows)
        self.assertIn("evening", windows)

    def test_account_profiles_yaml_exists(self):
        path = os.path.join(self.config_dir, "account_profiles.yaml")
        self.assertTrue(os.path.exists(path))


class TestTimeWindow(unittest.TestCase):
    """Test TimeWindow logic."""

    def test_contains_within_window(self):
        window = TimeWindow("test", {"start": "09:00", "end": "10:00", "hit_probability": 1.0})
        now = datetime(2024, 1, 1, 9, 30)
        self.assertTrue(window.contains(now))

    def test_contains_outside_window(self):
        window = TimeWindow("test", {"start": "09:00", "end": "10:00", "hit_probability": 1.0})
        now = datetime(2024, 1, 1, 11, 0)
        self.assertFalse(window.contains(now))

    def test_contains_at_boundary(self):
        window = TimeWindow("test", {"start": "09:00", "end": "10:00", "hit_probability": 1.0})
        self.assertTrue(window.contains(datetime(2024, 1, 1, 9, 0)))
        self.assertTrue(window.contains(datetime(2024, 1, 1, 10, 0)))


class TestScheduler(unittest.TestCase):
    """Test Scheduler task generation."""

    def setUp(self):
        self.schedule_cfg = {
            "windows": {
                "morning": {
                    "start": "08:30",
                    "end": "10:30",
                    "hit_probability": 1.0,
                    "max_platforms_per_window": 2,
                    "preferred_platforms": ["x_twitter", "reddit"],
                }
            },
            "global": {"min_gap_between_platforms": 180},
        }
        self.platforms_cfg = {
            "platforms": {
                "x_twitter": {
                    "enabled": True,
                    "weight": 0.5,
                    "session_duration": [5, 10],
                    "actions": {"browse_feed": {"weight": 1.0}},
                },
                "reddit": {
                    "enabled": True,
                    "weight": 0.5,
                    "session_duration": [5, 10],
                    "actions": {"browse_feed": {"weight": 1.0}},
                },
                "hackernews": {
                    "enabled": True,
                    "weight": 0.5,
                    "session_duration": [5, 10],
                    "actions": {"browse_frontpage": {"weight": 1.0}},
                },
            }
        }
        self.scheduler = Scheduler(self.schedule_cfg, self.platforms_cfg)

    def test_get_current_window_inside(self):
        now = datetime(2024, 1, 1, 9, 0)  # 9:00 AM
        window = self.scheduler.get_current_window(now)
        self.assertIsNotNone(window)
        self.assertEqual(window.name, "morning")

    def test_get_current_window_outside(self):
        now = datetime(2024, 1, 1, 15, 0)  # 3:00 PM
        window = self.scheduler.get_current_window(now)
        self.assertIsNone(window)

    def test_generate_tasks_respects_max_platforms(self):
        window = self.scheduler.get_current_window(datetime(2024, 1, 1, 9, 0))
        tasks = self.scheduler.generate_tasks(window)
        self.assertGreater(len(tasks), 0)
        self.assertLessEqual(len(tasks), 2)  # max_platforms_per_window

    def test_generate_tasks_respects_weights(self):
        window = self.scheduler.get_current_window(datetime(2024, 1, 1, 9, 0))
        # Run multiple times to verify weight-based selection
        selected_platforms = set()
        for _ in range(20):
            tasks = self.scheduler.generate_tasks(window)
            for t in tasks:
                selected_platforms.add(t["platform"])
        # Should only select from preferred_platforms
        self.assertTrue(all(p in ["x_twitter", "reddit"] for p in selected_platforms))

    def test_should_run_now(self):
        should_run, window = self.scheduler.should_run_now(datetime(2024, 1, 1, 9, 0))
        self.assertTrue(should_run)
        self.assertIsNotNone(window)


class TestRandomizer(unittest.TestCase):
    """Test Randomizer behavior."""

    def test_session_duration_range(self):
        for _ in range(50):
            d = Randomizer.session_duration(5, 10)
            self.assertGreaterEqual(d, 5)
            self.assertLessEqual(d, 10)

    def test_human_pause_range(self):
        for _ in range(50):
            p = Randomizer.human_pause(3, 7)
            self.assertGreaterEqual(p, 3)
            self.assertLessEqual(p, 7)

    def test_choose_platforms(self):
        platforms = ["a", "b", "c"]
        weights = [1.0, 1.0, 1.0]
        chosen = Randomizer.choose_platforms(platforms, weights, 2)
        self.assertLessEqual(len(chosen), 2)
        self.assertGreater(len(chosen), 0)
        # No duplicates
        self.assertEqual(len(chosen), len(set(chosen)))

    def test_should_execute_window_always(self):
        # With probability 1.0, should always execute
        for _ in range(20):
            self.assertTrue(Randomizer.should_execute_window(1.0))

    def test_should_execute_window_never(self):
        # With probability 0.0, should never execute
        for _ in range(20):
            self.assertFalse(Randomizer.should_execute_window(0.0))


class TestPlatformRegistry(unittest.TestCase):
    """Test that all platforms are registered."""

    def test_all_platforms_registered(self):
        expected = {"x_twitter", "reddit", "hackernews", "product_hunt"}
        actual = set(PLATFORM_REGISTRY.keys())
        self.assertEqual(expected, actual)

    def test_platforms_are_nurturer_subclasses(self):
        for name, cls in PLATFORM_REGISTRY.items():
            self.assertTrue(
                issubclass(cls, PlatformNurturer),
                f"{name} is not a PlatformNurturer subclass",
            )


class TestPlatformInstantiation(unittest.TestCase):
    """Test platform instantiation with mock CDP."""

    def setUp(self):
        self.mock_cdp = MockCDPManager()
        self.config = {
            "enabled": True,
            "weight": 1.0,
            "session_duration": [5, 10],
            "actions": {"browse_feed": {"weight": 1.0, "max_per_session": 1}},
            "topics": ["test"],
            "special_rules": [],
        }

    def test_x_twitter_instantiation(self):
        from platforms.x_twitter import XTwitterNurturer

        nurturer = XTwitterNurturer(self.config, self.mock_cdp)
        self.assertEqual(nurturer.platform_name, "x_twitter")

    def test_reddit_instantiation(self):
        from platforms.reddit import RedditNurturer

        nurturer = RedditNurturer(self.config, self.mock_cdp)
        self.assertEqual(nurturer.platform_name, "reddit")

    def test_hackernews_instantiation(self):
        from platforms.hackernews import HackerNewsNurturer

        nurturer = HackerNewsNurturer(self.config, self.mock_cdp)
        self.assertEqual(nurturer.platform_name, "hackernews")

    def test_product_hunt_instantiation(self):
        from platforms.product_hunt import ProductHuntNurturer

        nurturer = ProductHuntNurturer(self.config, self.mock_cdp)
        self.assertEqual(nurturer.platform_name, "product_hunt")


class TestPlatformLogic(unittest.TestCase):
    """Test platform business logic with mock CDP."""

    def setUp(self):
        self.mock_cdp = MockCDPManager()
        self.config = {
            "enabled": True,
            "weight": 1.0,
            "session_duration": [1, 2],
            "actions": {
                "browse_feed": {"weight": 1.0},
                "like": {"weight": 1.0, "max_per_session": 2},
            },
            "topics": ["AI"],
            "special_rules": [],
        }

    def test_login_check(self):
        from platforms.hackernews import HackerNewsNurturer

        nurturer = HackerNewsNurturer(self.config, self.mock_cdp)
        self.assertTrue(nurturer.login_check())
        self.assertIn("logout", str(self.mock_cdp.evaluated_expressions[-1]))

    def test_preflight_default(self):
        """Default preflight should pass."""
        from platforms.x_twitter import XTwitterNurturer

        nurturer = XTwitterNurturer(self.config, self.mock_cdp)
        self.assertTrue(nurturer.preflight_check())

    def test_random_decision_respects_max(self):
        from platforms.x_twitter import XTwitterNurturer

        nurturer = XTwitterNurturer(self.config, self.mock_cdp)
        # Force action count to max
        nurturer.actions_done["like"] = 2
        self.assertFalse(nurturer.random_decision("like"))

    def test_random_decision_weight_zero(self):
        """Action with weight 0 should never be chosen."""
        from platforms.x_twitter import XTwitterNurturer

        config = self.config.copy()
        config["actions"] = {"browse_feed": {"weight": 0.0}}
        nurturer = XTwitterNurturer(config, self.mock_cdp)
        self.assertFalse(nurturer.random_decision("browse_feed"))

    def test_record_observation(self):
        from platforms.x_twitter import XTwitterNurturer

        nurturer = XTwitterNurturer(self.config, self.mock_cdp)
        nurturer.record_observation("Test observation", tags=["test"])
        self.assertEqual(len(nurturer.observations), 1)
        self.assertEqual(nurturer.observations[0]["text"], "Test observation")
        self.assertEqual(nurturer.observations[0]["platform"], "x_twitter")


class TestExecutorFlow(unittest.TestCase):
    """Test executor task flow."""

    def setUp(self):
        # Ensure platforms are registered before creating executor
        import platforms

        # Patch sleep to avoid delays in tests
        import time as _time
        self._orig_sleep = _time.sleep
        _time.sleep = lambda x: None

        self.mock_cdp = MockCDPManager()
        self.platforms_cfg = {
            "platforms": {
                "x_twitter": {
                    "enabled": True,
                    "weight": 1.0,
                    "session_duration": [1, 1],
                    "actions": {"browse_feed": {"weight": 1.0}},
                    "topics": ["test"],
                    "special_rules": [],
                },
            },
            "global": {"min_gap_between_platforms": 0},  # No gap for tests
        }
        self.executor = Executor(
            self.mock_cdp, self.platforms_cfg, log_dir="/tmp/nurture_test_logs"
        )

    def test_run_platform(self):
        results = self.executor.run_platform("x_twitter", 0)  # 0min to avoid waiting
        self.assertGreater(len(results), 0)
        # First action should be browse
        self.assertEqual(results[0].action, "browse")
        self.assertTrue(results[0].success)

    def test_run_tasks(self):
        tasks = [
            {"platform": "x_twitter", "duration_minutes": 0},
        ]
        all_results = self.executor.run_tasks(tasks)
        self.assertIn("x_twitter", all_results)
        self.assertGreater(len(all_results["x_twitter"]), 0)

    def test_unknown_platform_raises(self):
        with self.assertRaises(ValueError):
            self.executor.run_platform("unknown_platform", 1)


    def tearDown(self):
        import time as _time
        _time.sleep = self._orig_sleep

class TestNotifier(unittest.TestCase):
    """Test notifier."""

    def test_notifier_prints(self):
        notifier = Notifier(target=None)
        result = notifier.send("Test message")
        # Without target, notifier falls back to print and returns False
        self.assertFalse(result)

    def test_notifier_digest(self):
        notifier = Notifier(target=None)
        result = notifier.send_digest(
            observations_count=5,
            platforms_ran=["x_twitter", "reddit"],
            errors=["test error"],
        )
        self.assertFalse(result)


class TestCDPManagerStatic(unittest.TestCase):
    """Test CDPManager static methods."""

    def test_check_port_no_server(self):
        """Port check should return False when no server running."""
        result = CDPManager.check_port(port=99999)
        self.assertFalse(result)

    def test_list_pages_no_server(self):
        """List pages should return empty list when no server."""
        result = CDPManager.list_pages(cdp_url="http://localhost:99999")
        self.assertEqual(result, [])


# ------------------------------------------------------------------
#  Integration-style test: full flow simulation
# ------------------------------------------------------------------

class TestFullFlow(unittest.TestCase):
    """Simulate a complete nurturing session end-to-end."""

    def setUp(self):
        import time as _time
        self._orig_sleep = _time.sleep
        _time.sleep = lambda x: None

    def tearDown(self):
        import time as _time
        _time.sleep = self._orig_sleep

    def test_simulated_evening_session(self):
        """Simulate an evening session with the scheduler and executor."""
        # Ensure platforms are registered
        import platforms

        schedule_cfg = {
            "windows": {
                "evening": {
                    "start": "20:00",
                    "end": "22:00",
                    "hit_probability": 1.0,
                    "max_platforms_per_window": 2,
                }
            }
        }
        platforms_cfg = {
            "platforms": {
                "hackernews": {
                    "enabled": True,
                    "weight": 1.0,
                    "session_duration": [0, 0],  # Fast for tests
                    "actions": {
                        "browse_frontpage": {"weight": 1.0},
                        "upvote": {"weight": 0.0},  # Disabled for test
                    },
                    "topics": ["AI"],
                    "special_rules": [],
                    "username": "testuser",
                },
            },
            "global": {"min_gap_between_platforms": 0},
        }

        scheduler = Scheduler(schedule_cfg, platforms_cfg)
        now = datetime(2024, 1, 1, 21, 0)  # 9 PM

        should_run, window = scheduler.should_run_now(now)
        self.assertTrue(should_run)

        tasks = scheduler.generate_tasks(window)
        self.assertGreater(len(tasks), 0)

        # Execute with mock CDP
        mock_cdp = MockCDPManager()
        executor = Executor(mock_cdp, platforms_cfg, log_dir="/tmp/nurture_test_logs")
        all_results = executor.run_tasks(tasks)

        for platform, results in all_results.items():
            for r in results:
                self.assertTrue(r.success, f"{platform}/{r.action} failed: {r.detail}")


# ------------------------------------------------------------------
#  Run tests
# ------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Nurture Framework Test Suite")
    print("=" * 60)

    # Run with verbosity
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors")
    print("=" * 60)

    sys.exit(0 if result.wasSuccessful() else 1)
