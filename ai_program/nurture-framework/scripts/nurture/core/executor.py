"""
Executor - Runs nurturing sessions for selected platforms sequentially.
Handles CDP lifecycle, logging, and observation persistence.
"""

import time
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

from .cdp_manager import CDPManager
from .randomizer import Randomizer
from .base import PlatformNurturer, ActionResult

# Platform registry - populated by importing platform modules
PLATFORM_REGISTRY: Dict[str, type] = {}


def register_platform(name: str, cls: type):
    """Register a platform implementation."""
    PLATFORM_REGISTRY[name] = cls


class Executor:
    """
    Orchestrates the execution of platform nurturing tasks.
    """

    def __init__(
        self,
        cdp_manager: CDPManager,
        platforms_config: dict,
        notifier=None,
        log_dir: str = "logs",
        feedback_dir: str = "feedback/observations",
        accounts: dict = None,
    ):
        self.cdp = cdp_manager
        self.config = platforms_config
        self.notifier = notifier
        self.accounts = accounts or {}
        self.log_dir = log_dir
        self.feedback_dir = feedback_dir
        os.makedirs(log_dir, exist_ok=True)
        os.makedirs(feedback_dir, exist_ok=True)

    def run_platform(self, platform_name: str, duration_minutes: int) -> List[ActionResult]:
        """
        Execute a single platform session.
        Returns list of ActionResults.
        """
        if platform_name not in PLATFORM_REGISTRY:
            raise ValueError(f"Platform '{platform_name}' not registered. "
                           f"Available: {list(PLATFORM_REGISTRY.keys())}")

        platform_cfg = self.config["platforms"][platform_name]
        cls = PLATFORM_REGISTRY[platform_name]

        print(f"\n{'='*50}")
        print(f"[Executor] Starting: {platform_name} ({duration_minutes}min)")
        print(f"{'='*50}")

        # Instantiate platform nurturer
        account = self.accounts.get(platform_name, {})
        nurturer = cls(config=platform_cfg, cdp_manager=self.cdp, notifier=self.notifier, account=account)

        # Pre-flight check
        if not nurturer.preflight_check():
            msg = f"Pre-flight check failed for {platform_name}, skipping."
            print(f"[Executor] {msg}")
            nurturer.notify(msg)
            return [ActionResult("preflight", False, msg)]

        # Check login
        try:
            if not nurturer.login_check():
                msg = f"Not logged in on {platform_name}, skipping."
                print(f"[Executor] {msg}")
                nurturer.notify(msg)
                return [ActionResult("login_check", False, msg)]
        except Exception as e:
            msg = f"Login check error on {platform_name}: {e}"
            print(f"[Executor] {msg}")
            return [ActionResult("login_check", False, msg)]

        # Run session
        results = []
        try:
            results = nurturer.run_session(duration_minutes)
        except Exception as e:
            msg = f"Session error on {platform_name}: {e}"
            print(f"[Executor] {msg}")
            results = [ActionResult("session", False, msg)]

        # Persist observations
        if nurturer.observations:
            self._save_observations(platform_name, nurturer.observations)

        # Persist logs
        self._save_log(platform_name, results, nurturer.observations)

        # Notify
        success_count = sum(1 for r in results if r.success)
        total_count = len(results)
        nurturer.notify(f"Session complete: {success_count}/{total_count} actions succeeded.")

        print(f"[Executor] {platform_name} finished: {success_count}/{total_count} actions OK")

        # Post-session cleanup
        try:
            nurturer.post_session()
        except Exception:
            pass

        return results

    def run_tasks(self, tasks: List[Dict]) -> Dict[str, List[ActionResult]]:
        """
        Run multiple platform tasks sequentially with gaps between them.
        Returns a dict mapping platform_name -> list of results.
        """
        all_results = {}

        for i, task in enumerate(tasks):
            platform = task["platform"]
            duration = task["duration_minutes"]

            results = self.run_platform(platform, duration)
            all_results[platform] = results

            # Gap between platforms (except after the last one)
            if i < len(tasks) - 1:
                gap = Randomizer.gap_between_platforms(
                    self.config.get("global", {}).get("min_gap_between_platforms", 180),
                    300
                )
                print(f"[Executor] Waiting {gap}s before next platform...")
                time.sleep(gap)

        return all_results

    def _save_observations(self, platform_name: str, observations: List[Dict]) -> None:
        """Append observations to daily JSONL file."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(self.feedback_dir, f"{date_str}.jsonl")

        with open(filepath, "a", encoding="utf-8") as f:
            for obs in observations:
                f.write(json.dumps(obs, ensure_ascii=False) + "\n")

        print(f"[Executor] Saved {len(observations)} observations to {filepath}")

    def _save_log(self, platform_name: str, results: List[ActionResult], observations: List[Dict]) -> None:
        """Save detailed log for the session."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        daily_dir = os.path.join(self.log_dir, date_str)
        os.makedirs(daily_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%H%M%S")
        filepath = os.path.join(daily_dir, f"{platform_name}_{timestamp}.json")

        log_data = {
            "platform": platform_name,
            "timestamp": datetime.now().isoformat(),
            "results": [
                {
                    "action": r.action,
                    "success": r.success,
                    "detail": r.detail,
                    "timestamp": r.timestamp,
                }
                for r in results
            ],
            "observations_count": len(observations),
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
