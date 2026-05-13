"""
PlatformNurturer - Base class for all social media nurturing platforms.
All platform implementations must inherit from this class.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from collections import defaultdict
import time
import random


@dataclass
class ActionResult:
    """Result of a single action execution."""
    action: str
    success: bool
    detail: str
    timestamp: float = field(default_factory=time.time)
    observation: Optional[str] = None


class PlatformNurturer(ABC):
    """
    Base class for platform-specific nurturing logic.
    
    Subclasses must implement:
      - platform_name (property)
      - login_check()
      - browse()
      - execute_action()
      - run_session()
    """

    def __init__(self, config: dict, cdp_manager, notifier=None, account: dict = None):
        self.config = config
        self.cdp = cdp_manager
        self.notifier = notifier
        self.account = account or {}
        self.observations: List[Dict] = []
        self.actions_done = defaultdict(int)
        self._session_start = time.time()
        self._posts_cache: List[Dict] = []  # Cached from browse for actions to use

    # ------------------------------------------------------------------
    #  Framework-level helpers (shared across all platforms)
    # ------------------------------------------------------------------

    def human_pause(self, min_sec: float = 3.0, max_sec: float = 7.0) -> None:
        """Pause for a random duration to simulate human behavior."""
        time.sleep(random.uniform(min_sec, max_sec))

    def random_decision(self, action_name: str) -> bool:
        """
        Decide whether to perform an action based on:
          1. Per-session max limit
          2. Daily max limit (if configured)
          3. Random weight
        """
        actions_cfg = self.config.get("actions", {})
        if action_name not in actions_cfg:
            return False

        action_cfg = actions_cfg[action_name]
        max_per_session = action_cfg.get("max_per_session", 999)

        # 1. Session limit
        if self.actions_done[action_name] >= max_per_session:
            return False

        # 2. Daily limit (if defined in daily_limits)
        daily_limits = self.config.get("daily_limits", {})
        if action_name in daily_limits:
            if self.actions_done[f"_daily_{action_name}"] >= daily_limits[action_name]:
                return False

        # 3. Random weight
        weight = action_cfg.get("weight", 0.0)
        return random.random() < weight

    def record_observation(
        self,
        text: str,
        tags: List[str] = None,
        source_url: str = "",
        platform: str = None,
    ) -> None:
        """Record an observation for later feedback analysis."""
        self.observations.append({
            "timestamp": time.time(),
            "platform": platform or self.platform_name,
            "text": text,
            "tags": tags or [],
            "source_url": source_url,
        })

    def notify(self, message: str) -> None:
        """Send a notification if notifier is available."""
        if self.notifier:
            try:
                self.notifier.send(f"[{self.platform_name}] {message}")
            except Exception:
                pass  # Notifications are best-effort

    # ------------------------------------------------------------------
    #  Abstract interface (must be implemented by subclasses)
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Unique platform identifier, e.g. 'hackernews', 'reddit'."""
        pass

    @abstractmethod
    def login_check(self) -> bool:
        """Return True if the user is logged in on this platform."""
        pass

    @abstractmethod
    def browse(self, duration_minutes: int) -> ActionResult:
        """
        Browse the platform for the given duration.
        Should scroll, observe, and record observations.
        """
        pass

    @abstractmethod
    def execute_action(self, action_name: str) -> ActionResult:
        """Execute a specific action (like, comment, upvote, etc.)."""
        pass

    @abstractmethod
    def run_session(self, duration_minutes: int) -> List[ActionResult]:
        """
        Run a complete nurturing session:
          1. Check login
          2. Browse
          3. Decide and execute optional actions
          4. Return all results
        """
        pass

    # ------------------------------------------------------------------
    #  Optional hooks
    # ------------------------------------------------------------------

    def preflight_check(self) -> bool:
        """
        Optional pre-flight validation (e.g. HN new-account limits).
        Return False to skip the entire session.
        """
        return True

    def post_session(self) -> None:
        """Cleanup after session ends. Override if needed."""
        pass
