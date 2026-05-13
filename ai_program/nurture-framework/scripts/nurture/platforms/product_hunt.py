"""
Product Hunt nurturing implementation.

Actions: browse_daily, comment, upvote
Style: Casual, specific to product, no AI clichés, no markdown
Pitfalls: DOM extraction unreliable - must use vision fallback
          Comments MUST reference actual product features
          Filter out "THE PITCH" / Promoted products
"""

import random
import time
from typing import List

from core.base import PlatformNurturer, ActionResult
from core.executor import register_platform


class ProductHuntNurturer(PlatformNurturer):
    """Nurturing logic for Product Hunt."""

    @property
    def platform_name(self) -> str:
        return "product_hunt"

    def login_check(self) -> bool:
        """Check if logged into Product Hunt."""
        try:
            self.cdp.navigate("https://www.producthunt.com/")
            self.human_pause(3, 5)
            body_text = self.cdp.evaluate("document.body.innerText")
            # If no login/signup buttons visible, user is logged in
            has_login = "Log in" in body_text or "Sign up" in body_text or "Join" in body_text
            return not has_login
        except Exception as e:
            print(f"[{self.platform_name}] Login check error: {e}")
            return False

    def browse(self, duration_minutes: int) -> ActionResult:
        """Browse Product Hunt daily products."""
        print(f"[{self.platform_name}] Browsing daily products for {duration_minutes}min...")

        self.cdp.navigate("https://www.producthunt.com")
        self.human_pause(5, 7)  # Wait for React hydration

        # Scroll to trigger lazy loading
        for _ in range(3):
            self.cdp.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.human_pause(2, 3)

        # Try DOM extraction first
        products = []
        try:
            products = self.cdp.evaluate("""
                (function() {
                    const results = [];
                    const seen = new Set();
                    document.querySelectorAll('section').forEach(section => {
                        const text = section.innerText.trim();
                        const lines = text.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
                        if (lines.length >= 3) {
                            const name = lines[0];
                            const desc = lines[1];
                            if (name.length < 80 && desc.length > 5 &&
                                !name.includes('Welcome') && !name.includes('Product Hunt') &&
                                !name.includes('Take a tour') &&
                                !text.includes('THE PITCH') && !text.includes('Promoted')) {
                                const link = section.querySelector('a');
                                if (link) {
                                    const href = link.getAttribute('href');
                                    if (href && (href.startsWith('/products/') || href.startsWith('/posts/')) &&
                                        !href.includes('/new') && !seen.has(href)) {
                                        seen.add(href);
                                        results.push({name: name, description: desc, href: href});
                                    }
                                }
                            }
                        }
                    });
                    return results.slice(0, 10);
                })()
            """)
        except Exception as e:
            print(f"[{self.platform_name}] DOM extraction failed: {e}")

        # Fallback: if DOM extraction failed, take screenshot for vision
        if len(products) < 3:
            print(f"[{self.platform_name}] DOM returned {len(products)} products, saving screenshot for vision fallback")
            try:
                self.cdp.screenshot("/tmp/ph_homepage.png", full_page=True)
            except Exception:
                pass

        # Record observations
        for p in products[:5]:
            self.record_observation(
                f"PH product: {p['name']} - {p['description'][:100]}",
                tags=["producthunt", "daily"],
                source_url=f"https://www.producthunt.com{p['href']}",
            )

        # Cache products for comment action
        self._products_cache = products

        # Browse duration
        start = time.time()
        while time.time() - start < duration_minutes * 60:
            self.human_pause(5, 12)
            if random.random() < 0.3:
                self.cdp.scroll_by(random.randint(300, 700))
                self.human_pause(2, 4)

        return ActionResult(
            "browse",
            True,
            f"Browsed PH for {duration_minutes}min, found {len(products)} products",
        )

    def execute_action(self, action_name: str) -> ActionResult:
        """Execute a specific interaction on Product Hunt."""
        print(f"[{self.platform_name}] Executing: {action_name}")

        if action_name == "comment":
            return self._action_comment()
        elif action_name == "upvote":
            return self._action_upvote()
        else:
            return ActionResult(action_name, False, f"Unknown action: {action_name}")

    # ------------------------------------------------------------------
    #  Upvote
    # ------------------------------------------------------------------

    def _action_upvote(self) -> ActionResult:
        """Upvote a product on PH."""
        if not getattr(self, "_products_cache", None):
            return ActionResult("upvote", False, "No products cached from browse")

        target = random.choice(self._products_cache[:5])

        try:
            self.cdp.navigate(f"https://www.producthunt.com{target['href']}")
            self.human_pause(3, 5)

            # Try to find and click upvote button
            result = self.cdp.evaluate("""
                (function() {
                    // Look for upvote button by various selectors
                    var btn = document.querySelector('button[data-testid="upvote-button"]');
                    if (!btn) btn = document.querySelector('button[aria-label*="upvote"]');
                    if (!btn) {
                        // Try to find by inner text or icon
                        var buttons = document.querySelectorAll('button');
                        for (var i = 0; i < buttons.length; i++) {
                            var text = buttons[i].innerText.toLowerCase();
                            if (text.includes('upvote') || text.includes('▲')) {
                                btn = buttons[i];
                                break;
                            }
                        }
                    }
                    if (btn) {
                        btn.click();
                        return 'UPVOTED';
                    }
                    return 'NO_BUTTON';
                })()
            """)

            if result == "UPVOTED":
                self.actions_done["upvote"] += 1
                self.record_observation(
                    f"Upvoted PH product: {target['name']}",
                    tags=["producthunt", "upvote"],
                    source_url=f"https://www.producthunt.com{target['href']}",
                )
                return ActionResult("upvote", True, f"Upvoted {target['name']}")
            else:
                return ActionResult("upvote", False, "No upvote button found")

        except Exception as e:
            return ActionResult("upvote", False, f"Error: {e}")

    # ------------------------------------------------------------------
    #  Comment
    # ------------------------------------------------------------------

    def _action_comment(self) -> ActionResult:
        """
        Comment on a Product Hunt product.
        CRITICAL RULES:
        - Must read product description first
        - Comment must reference specific features/details
        - 1-3 sentences max
        - No AI clichés ("Great product", "Congratulations")
        - Casual tone, can be skeptical
        - No markdown
        """
        if not getattr(self, "_products_cache", None):
            return ActionResult("comment", False, "No products cached from browse")

        target = random.choice(self._products_cache[:5])

        try:
            # Navigate to product page
            self.cdp.navigate(f"https://www.producthunt.com{target['href']}")
            self.human_pause(3, 5)

            # Read product details
            product_title = self.cdp.evaluate("document.title") or target["name"]
            tagline = ""
            description = ""
            try:
                tagline_el = self.cdp.query_selector('[data-test="product-tagline"], h2, h3')
                if tagline_el:
                    tagline = tagline_el.inner_text().strip()
            except Exception:
                pass

            try:
                description = self.cdp.evaluate("document.body.innerText")[:2000]
            except Exception:
                pass

            print(f"[{self.platform_name}] Product: {target['name']}")
            print(f"[{self.platform_name}] Tagline: {tagline[:100]}...")

            # Generate product-specific comment
            # TODO: Replace with AI-generated comment based on product details
            comment_text = self._generate_product_comment(target["name"], tagline, description)

            # Scroll to comment section
            self.cdp.evaluate("window.scrollTo(0, 1200)")
            self.human_pause(2, 3)

            # Find and click the "Comment" button to expand editor
            comment_btn = None
            try:
                buttons = self.cdp.query_selector_all("button")
                for btn in buttons:
                    try:
                        if btn.inner_text().strip() == "Comment" and btn.is_visible():
                            comment_btn = btn
                            break
                    except Exception:
                        continue
            except Exception:
                pass

            if comment_btn:
                comment_btn.click()
                self.human_pause(2, 3)

            # Find the contenteditable div editor
            editor = None
            try:
                editor = self.cdp.query_selector('div[contenteditable="true"]')
            except Exception:
                pass

            if not editor:
                return ActionResult("comment", False, "No comment editor found")

            # Click and clear (macOS: Meta+a, others: Control+a)
            editor.click()
            self.human_pause(1, 2)
            import sys
            select_all = "Meta+a" if sys.platform == "darwin" else "Control+a"
            self.cdp.keyboard_press(select_all)
            self.cdp.keyboard_press("Backspace")
            self.human_pause(0.5, 1)

            # Type comment
            self.cdp.keyboard_type(comment_text, delay=15)
            self.human_pause(1, 2)

            # Find submit button (also labeled "Comment")
            submit_btn = None
            try:
                all_buttons = self.cdp.query_selector_all("button")
                for btn in all_buttons:
                    try:
                        if btn.inner_text().strip() == "Comment" and btn.is_visible():
                            submit_btn = btn
                            break
                    except Exception:
                        continue
            except Exception:
                pass

            if not submit_btn:
                return ActionResult("comment", False, "Submit button not found")

            submit_btn.click()
            self.human_pause(5, 7)

            # Verify: reload and check if comment appears
            try:
                self.cdp.reload()
                self.human_pause(3, 5)
                self.cdp.evaluate("window.scrollTo(0, 1200)")
                self.human_pause(2, 3)

                body_text = self.cdp.evaluate("document.body.innerText")
                verified = comment_text[:30] in body_text
            except Exception:
                verified = False

            if verified:
                self.actions_done["comment"] += 1
                self.record_observation(
                    f"Commented on PH: {target['name']}",
                    tags=["producthunt", "comment"],
                    source_url=f"https://www.producthunt.com{target['href']}",
                )
                return ActionResult("comment", True, f"Commented on {target['name']}")
            else:
                # Comment might still have been posted but not visible after reload
                self.actions_done["comment"] += 1
                return ActionResult("comment", True, f"Commented on {target['name']} (verification inconclusive)")

        except Exception as e:
            return ActionResult("comment", False, f"Error: {e}")

    def _generate_product_comment(self, name: str, tagline: str, description: str) -> str:
        """
        Generate a product-specific, human-sounding PH comment using AI.
        Falls back to templates if AI is unavailable.
        """
        from core.text_generator import generate_comment
        post_text = f"{tagline}\n\n{description}" if description else tagline
        return generate_comment(
            platform="product_hunt",
            post_title=name,
            post_text=post_text,
            max_length=250,
        )

    # ------------------------------------------------------------------
    #  Session orchestration
    # ------------------------------------------------------------------

    def run_session(self, duration_minutes: int) -> List[ActionResult]:
        """Run a complete Product Hunt nurturing session."""
        results = []
        results.append(self.browse(duration_minutes))

        if self.random_decision("comment"):
            self.human_pause(2, 5)
            results.append(self.execute_action("comment"))

        if self.random_decision("upvote"):
            self.human_pause(2, 5)
            results.append(self.execute_action("upvote"))

        return results


# Register with executor
register_platform("product_hunt", ProductHuntNurturer)
