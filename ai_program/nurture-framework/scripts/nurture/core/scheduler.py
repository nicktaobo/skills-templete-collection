"""
Scheduler - Decides which platforms to run in which time windows.
Reads configuration and generates a task list for the current time.
"""

from datetime import datetime, time as dt_time
from typing import List, Dict, Optional, Tuple
import random

from .randomizer import Randomizer


class TimeWindow:
    """Represents a scheduled time window."""
    def __init__(self, name: str, config: dict):
        self.name = name
        self.start = self._parse_time(config["start"])
        self.end = self._parse_time(config["end"])
        self.hit_probability = config.get("hit_probability", 1.0)
        self.max_platforms = config.get("max_platforms_per_window", 2)
        self.preferred = config.get("preferred_platforms", [])

    @staticmethod
    def _parse_time(t: str) -> dt_time:
        """Parse 'HH:MM' string to time object."""
        h, m = map(int, t.split(":"))
        return dt_time(h, m)

    def contains(self, now: datetime) -> bool:
        """Check if given datetime falls within this window."""
        current = now.time()
        if self.start <= self.end:
            return self.start <= current <= self.end
        else:
            # Window crosses midnight (not used in current config)
            return current >= self.start or current <= self.end


class Scheduler:
    """
    Generates daily nurturing tasks based on schedule and platform configs.
    """

    def __init__(self, schedule_config: dict, platforms_config: dict):
        self.schedule = schedule_config
        self.platforms = platforms_config
        self.windows: List[TimeWindow] = []
        self._parse_windows()

    def _parse_windows(self) -> None:
        """Parse time windows from config."""
        for name, cfg in self.schedule.get("windows", {}).items():
            self.windows.append(TimeWindow(name, cfg))

    def get_current_window(self, now: Optional[datetime] = None) -> Optional[TimeWindow]:
        """Return the current active time window, or None."""
        now = now or datetime.now()
        for window in self.windows:
            if window.contains(now):
                return window
        return None

    def generate_tasks(self, window: TimeWindow) -> List[Dict]:
        """
        Generate a list of tasks for the given window.
        Each task: {"platform": str, "duration_minutes": int}
        """
        enabled_platforms = []
        weights = []

        for name, cfg in self.platforms.get("platforms", {}).items():
            if not cfg.get("enabled", True):
                continue

            # Respect preferred_platforms if specified
            if window.preferred and name not in window.preferred:
                continue

            weight = cfg.get("weight", 1.0)
            enabled_platforms.append(name)
            weights.append(weight)

        if not enabled_platforms:
            return []

        # Decide how many platforms to run (1 to max_platforms)
        max_p = min(window.max_platforms, len(enabled_platforms))
        count = random.randint(1, max_p)

        # Choose platforms
        chosen = Randomizer.choose_platforms(enabled_platforms, weights, count)

        # Build tasks with random durations
        tasks = []
        for platform_name in chosen:
            cfg = self.platforms["platforms"][platform_name]
            dur_range = cfg.get("session_duration", [5, 10])
            duration = Randomizer.session_duration(dur_range[0], dur_range[1])
            tasks.append({
                "platform": platform_name,
                "duration_minutes": duration,
                "window": window.name,
            })

        return tasks

    def should_run_now(self, now: Optional[datetime] = None) -> Tuple[bool, Optional[TimeWindow]]:
        """
        Convenience method: check if we should run now.
        Returns (should_run, window_or_none).
        """
        window = self.get_current_window(now)
        if not window:
            return False, None

        if not Randomizer.should_execute_window(window.hit_probability):
            return False, window

        return True, window
