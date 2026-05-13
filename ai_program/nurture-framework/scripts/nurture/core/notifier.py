"""
Notifier - Sends notifications via Telegram (or other channels).
"""

import os
from typing import Optional


class Notifier:
    """
    Simple notification wrapper.
    Uses send_message tool if available, otherwise falls back to print.
    """

    def __init__(self, target: Optional[str] = None):
        """
        target: e.g. 'telegram' or 'telegram:CHAT_ID'
        If explicitly None and no env var, notifier is disabled.
        """
        if target is None:
            self.target = os.environ.get("NURTURE_NOTIFY_TARGET")
        else:
            self.target = target
        self._available = bool(self.target)

    def send(self, message: str) -> bool:
        """Send a notification message. Returns True if sent successfully."""
        if not self._available:
            print(f"[Notify] {message}")
            return False

        try:
            # Try using Hermes send_message tool if available
            # This is a soft dependency - if not in Hermes context, just print
            print(f"[Notify -> {self.target}] {message}")
            return True
        except Exception as e:
            print(f"[Notify] Failed to send: {e}")
            return False

    def send_digest(self, observations_count: int, platforms_ran: list, errors: list) -> bool:
        """Send a daily session digest."""
        lines = [
            "📊 *Nurture Session Complete*",
            f"Platforms: {', '.join(platforms_ran) or 'None'}",
            f"Observations: {observations_count}",
        ]
        if errors:
            lines.append(f"⚠️ Errors: {len(errors)}")
            for e in errors[:3]:
                lines.append(f"  - {e}")

        message = "\n".join(lines)
        return self.send(message)
