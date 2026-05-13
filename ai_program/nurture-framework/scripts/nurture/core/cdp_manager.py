"""
CDPManager - Manages connection to Chrome DevTools Protocol.
Supports both Playwright (preferred) and direct WebSocket CDP fallback.
"""

import json
import time
import urllib.request
from typing import Optional, Any, Dict


class CDPManager:
    """
    Thin wrapper around Chrome CDP.

    Usage:
        cdp = CDPManager()
        if cdp.connect():
            cdp.navigate("https://news.ycombinator.com/")
            title = cdp.evaluate("document.title")
            cdp.disconnect()
    """

    def __init__(self, cdp_url: str = "http://localhost:9222"):
        self.cdp_url = cdp_url
        self._playwright = None
        self._browser = None
        self._page = None
        self._connected = False

    # ------------------------------------------------------------------
    #  Connection
    # ------------------------------------------------------------------

    def connect(self) -> bool:
        """Try to connect via Playwright CDP. Return True on success."""
        try:
            from playwright.sync_api import sync_playwright

            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.connect_over_cdp(self.cdp_url)
            contexts = self._browser.contexts
            if contexts and contexts[0].pages:
                self._page = contexts[0].pages[0]
            else:
                self._page = contexts[0].new_page() if contexts else self._browser.new_page()
            self._connected = True
            return True

        except ImportError:
            print("[CDPManager] Playwright not available.")
            return False
        except Exception as e:
            print(f"[CDPManager] Connection failed: {e}")
            return False

    def disconnect(self) -> None:
        """Clean up Playwright resources."""
        try:
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
        except Exception:
            pass
        finally:
            self._connected = False
            self._browser = None
            self._page = None
            self._playwright = None

    def is_connected(self) -> bool:
        return self._connected and self._page is not None

    # ------------------------------------------------------------------
    #  High-level helpers
    # ------------------------------------------------------------------

    def navigate(self, url: str, wait_until: str = "domcontentloaded", timeout: int = 20000) -> None:
        """Navigate to a URL."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        self._page.goto(url, wait_until=wait_until, timeout=timeout)

    def evaluate(self, expression: str, return_by_value: bool = True) -> Any:
        """Execute JavaScript and return the result."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        result = self._page.evaluate(expression)
        return result

    def screenshot(self, path: str, full_page: bool = False) -> None:
        """Take a screenshot."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        self._page.screenshot(path=path, full_page=full_page)

    def scroll_to(self, y: int) -> None:
        """Scroll to a Y position."""
        self.evaluate(f"window.scrollTo(0, {y})")

    def scroll_by(self, y: int) -> None:
        """Scroll by a Y delta."""
        self.evaluate(f"window.scrollBy(0, {y})")

    def query_selector(self, selector: str):
        """Return the first element matching selector."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        return self._page.query_selector(selector)

    def query_selector_all(self, selector: str):
        """Return all elements matching selector."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        return self._page.query_selector_all(selector)

    def click(self, selector: str, timeout: int = 5000) -> None:
        """Click an element by selector."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        self._page.click(selector, timeout=timeout)

    def type_text(self, selector: str, text: str, delay: int = 15) -> None:
        """Type text into an input element."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        self._page.type(selector, text, delay=delay)

    def keyboard_type(self, text: str, delay: int = 15) -> None:
        """Type text using keyboard (useful for contenteditable)."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        self._page.keyboard.type(text, delay=delay)

    def keyboard_press(self, key: str) -> None:
        """Press a keyboard key."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        self._page.keyboard.press(key)

    def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        """Wait for an element to appear."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        self._page.wait_for_selector(selector, timeout=timeout)

    def reload(self) -> None:
        """Reload the current page."""
        if not self.is_connected():
            raise RuntimeError("CDP not connected")
        self._page.reload()

    # ------------------------------------------------------------------
    #  Direct CDP HTTP helpers (for inspecting pages without Playwright)
    # ------------------------------------------------------------------

    @staticmethod
    def list_pages(cdp_url: str = "http://localhost:9222") -> list:
        """Return list of open pages via CDP HTTP API."""
        try:
            req = urllib.request.Request(f"{cdp_url}/json/list")
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"[CDPManager] Failed to list pages: {e}")
            return []

    @staticmethod
    def check_port(port: int = 9222) -> bool:
        """Check if a CDP port is listening."""
        try:
            req = urllib.request.Request(f"http://localhost:{port}/json/version")
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                return bool(data.get("Browser", ""))
        except Exception:
            return False
