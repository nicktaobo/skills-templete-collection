"""
Randomizer - Generates human-like random behaviors for nurturing sessions.
"""

import random
from datetime import datetime, timedelta
from typing import List, Tuple


class Randomizer:
    """
    Centralized random behavior generation.
    All random decisions go through here for reproducibility and tuning.
    """

    @staticmethod
    def should_execute_window(hit_probability: float) -> bool:
        """Decide if a time window should trigger execution."""
        return random.random() < hit_probability

    @staticmethod
    def choose_platforms(platforms: List[str], weights: List[float], max_count: int) -> List[str]:
        """
        Choose up to max_count platforms based on weights.
        Uses weighted random sampling without replacement.
        """
        if not platforms or not weights:
            return []

        # Normalize weights
        total = sum(weights)
        if total == 0:
            return []
        normalized = [w / total for w in weights]

        # Sample without replacement
        chosen = []
        available = list(zip(platforms, normalized))
        while len(chosen) < max_count and available:
            names, probs = zip(*available)
            pick = random.choices(names, weights=probs, k=1)[0]
            chosen.append(pick)
            available = [(n, p) for n, p in available if n != pick]

        return chosen

    @staticmethod
    def session_duration(min_minutes: int, max_minutes: int) -> int:
        """Generate a random session duration in minutes."""
        return random.randint(min_minutes, max_minutes)

    @staticmethod
    def human_pause(min_sec: float = 3.0, max_sec: float = 7.0) -> float:
        """Generate a random pause duration in seconds."""
        return random.uniform(min_sec, max_sec)

    @staticmethod
    def scroll_amount(min_px: int = 200, max_px: int = 800) -> int:
        """Generate a random scroll amount in pixels."""
        return random.randint(min_px, max_px)

    @staticmethod
    def gap_between_platforms(min_sec: int = 180, max_sec: int = 300) -> int:
        """Generate a random gap between platform sessions in seconds."""
        return random.randint(min_sec, max_sec)

    @staticmethod
    def jitter_time(base_time: datetime, jitter_minutes: int = 10) -> datetime:
        """Add random jitter to a scheduled time."""
        jitter = random.randint(-jitter_minutes, jitter_minutes)
        return base_time + timedelta(minutes=jitter)

    @staticmethod
    def coin_flip(probability: float = 0.5) -> bool:
        """Simple coin flip with given probability."""
        return random.random() < probability
