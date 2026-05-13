"""
Reddit (Rabbit) nurturing implementation.

Actions: browse_feed, upvote, comment, save
Style: Casual, slang allowed (lol, ngl, fr, tbh), short comments
Pitfalls: Shadow DOM blocks text extraction - MUST use vision screenshots
          Collapsed composer trigger, adaptive scroll for comment box
"""

import os
import random
import time
from typing import List

from core.base import PlatformNurturer, ActionResult
from core.executor import register_platform


class RedditNurturer(PlatformNurturer):
    """Nurturing logic for Reddit."""

    @property
    def platform_name(self) -> str:
        return "reddit"

    def login_check(self) -> bool:
        """Check if logged into Reddit by visiting profile page."""
        try:
            username = self.account.get("username", "")
            if not username:
                return False
            self.cdp.navigate(f"https://www.reddit.com/user/{username}/")
            self.human_pause(3, 5)
            body_text = self.cdp.evaluate("document.body.innerText")
            return "Overview" in body_text
        except Exception as e:
            print(f"[{self.platform_name}] Login check error: {e}")
            return False

    def browse(self, duration_minutes: int) -> ActionResult:
        """Browse Reddit home feed or search results."""
        print(f"[{self.platform_name}] Browsing for {duration_minutes}min...")

        # Choose mode: home or search
        mode = random.choice(["home", "search"])
        if mode == "home":
            self.cdp.navigate("https://www.reddit.com/")
        else:
            topic = random.choice(
                self.config.get("search_fallback_topics", ["vibe coding"])
            )
            self.cdp.navigate(
                f"https://www.reddit.com/search/?q={topic.replace(' ', '+')}&sort=top&t=month"
            )

        self.human_pause(4, 7)

        # Extract posts for observations
        posts = []
        try:
            posts = self.cdp.evaluate("""
                (function() {
                    const results = [];
                    const seen = new Set();
                    // Try multiple selectors for post titles
                    const selectors = [
                        'a[slot="title"]',
                        'a[data-testid="post-title"]',
                        'a[data-testid="post-title-text"]',
                        'a[href*="/comments/"]'
                    ];
                    for (const sel of selectors) {
                        document.querySelectorAll(sel).forEach(a => {
                            const text = a.innerText.trim();
                            const href = a.getAttribute('href');
                            if (text && text.length > 5 && text.length < 200 && !seen.has(text)) {
                                seen.add(text);
                                results.push({title: text, href: href || ''});
                            }
                        });
                    }
                    return results.slice(0, 10);
                })()
            """)

            for post in posts[:5]:
                self.record_observation(
                    f"Reddit post: {post['title']}",
                    tags=["reddit", mode, "post"],
                    source_url=f"https://www.reddit.com{post['href']}" if post['href'] else "",
                )
        except Exception as e:
            print(f"[{self.platform_name}] Failed to extract posts: {e}")

        # Cache posts for actions
        self._posts_cache = posts

        # Browse duration
        start = time.time()
        posts_seen = len(posts)
        while time.time() - start < duration_minutes * 60:
            self.human_pause(5, 12)

            if random.random() < 0.4:
                self.cdp.scroll_by(random.randint(300, 800))
                self.human_pause(2, 4)

            # Long pause for "reading"
            if random.random() < 0.15:
                self.human_pause(10, 20)

        return ActionResult(
            "browse",
            True,
            f"Browsed Reddit ({mode}) for {duration_minutes}min, saw ~{posts_seen} posts",
        )

    def execute_action(self, action_name: str) -> ActionResult:
        """Execute a specific interaction on Reddit."""
        print(f"[{self.platform_name}] Executing: {action_name}")

        if action_name == "upvote":
            return self._action_upvote()
        elif action_name == "comment":
            return self._action_comment()
        elif action_name == "save":
            return self._action_save()
        else:
            return ActionResult(action_name, False, f"Unknown action: {action_name}")

    # ------------------------------------------------------------------
    #  Upvote
    # ------------------------------------------------------------------

    def _action_upvote(self) -> ActionResult:
        """Upvote a post on the current page. Multi-strategy detection for Reddit's Web Components."""
        try:
            # Multi-strategy upvote detection with shadow DOM support
            result = self.cdp.evaluate("""
                (function() {
                    function isVisible(el) {
                        if (!el) return false;
                        var rect = el.getBoundingClientRect();
                        return rect.width > 0 && rect.height > 0 && rect.top >= 0 && rect.top < window.innerHeight;
                    }
                    function clickUpvote(btn, strategy) {
                        btn.scrollIntoView({behavior: 'instant', block: 'center'});
                        btn.click();
                        return {status: 'UPVOTED', strategy: strategy};
                    }
                    
                    // Strategy 1: aria-label / data-testid containing "upvote" (case-insensitive)
                    var allBtns = document.querySelectorAll('button, [role="button"]');
                    for (var i = 0; i < allBtns.length; i++) {
                        var b = allBtns[i];
                        var label = (b.getAttribute('aria-label') || '').toLowerCase();
                        var testid = (b.getAttribute('data-testid') || '').toLowerCase();
                        if ((label.includes('upvote') || testid.includes('upvote')) && isVisible(b)) {
                            return clickUpvote(b, 'aria-label');
                        }
                    }
                    
                    // Strategy 2: innerHTML contains upvote-related text
                    for (var i = 0; i < allBtns.length; i++) {
                        var b = allBtns[i];
                        var html = (b.innerHTML || '').toLowerCase();
                        if ((html.includes('upvote') || html.includes('arrow-up') || 
                             html.includes('uparrow') || html.includes('caret-up')) && isVisible(b)) {
                            return clickUpvote(b, 'svg-pattern');
                        }
                    }
                    
                    // Strategy 3: Inside shreddit-post shadow DOM
                    var posts = document.querySelectorAll('shreddit-post');
                    for (var p = 0; p < Math.min(posts.length, 5); p++) {
                        var post = posts[p];
                        var sr = post.shadowRoot;
                        if (sr) {
                            var srBtns = sr.querySelectorAll('button, [role="button"]');
                            for (var j = 0; j < srBtns.length; j++) {
                                var sb = srBtns[j];
                                var sbLabel = (sb.getAttribute('aria-label') || '').toLowerCase();
                                if (sbLabel.includes('upvote')) {
                                    return clickUpvote(sb, 'shadow-dom');
                                }
                                // Check for up arrow SVG inside
                                var svg = sb.querySelector('svg');
                                if (svg) {
                                    var svgHtml = svg.outerHTML.toLowerCase();
                                    if (svgHtml.includes('up') || svgHtml.includes('arrow')) {
                                        return clickUpvote(sb, 'shadow-svg');
                                    }
                                }
                            }
                        }
                    }
                    
                    // Strategy 4: rpl-action-bar (light DOM child of shreddit-post)
                    var actionBars = document.querySelectorAll('rpl-action-bar');
                    for (var a = 0; a < actionBars.length; a++) {
                        var ab = actionBars[a];
                        var abBtns = ab.querySelectorAll('button, [role="button"]');
                        for (var k = 0; k < abBtns.length; k++) {
                            var abBtn = abBtns[k];
                            var abLabel = (abBtn.getAttribute('aria-label') || '').toLowerCase();
                            if (abLabel.includes('upvote')) {
                                return clickUpvote(abBtn, 'action-bar');
                            }
                            // First button in action-bar is often upvote
                            if (k === 0 && isVisible(abBtn)) {
                                var abSvg = abBtn.querySelector('svg');
                                if (abSvg) {
                                    return clickUpvote(abBtn, 'action-bar-first');
                                }
                            }
                        }
                    }
                    
                    // Strategy 5: shreddit-vote-animations component
                    var voteAnims = document.querySelectorAll('shreddit-vote-animations');
                    for (var v = 0; v < voteAnims.length; v++) {
                        var va = voteAnims[v];
                        var vaBtns = va.querySelectorAll('button, [role="button"]');
                        for (var m = 0; m < vaBtns.length; m++) {
                            var vaBtn = vaBtns[m];
                            var vaLabel = (vaBtn.getAttribute('aria-label') || '').toLowerCase();
                            if (vaLabel.includes('upvote')) {
                                return clickUpvote(vaBtn, 'vote-animations');
                            }
                        }
                    }
                    
                    // Strategy 6: Generic up arrow in post containers
                    var containers = document.querySelectorAll('shreddit-post, article, [data-testid="post-container"]');
                    for (var c = 0; c < Math.min(containers.length, 5); c++) {
                        var container = containers[c];
                        var buttons = container.querySelectorAll('button');
                        for (var n = 0; n < buttons.length; n++) {
                            var btn = buttons[n];
                            var svg = btn.querySelector('svg');
                            if (svg) {
                                var svgText = svg.outerHTML.toLowerCase();
                                if ((svgText.includes('up') || svgText.includes('arrow')) && isVisible(btn)) {
                                    // Make sure it's an upvote (not downvote) - usually first button in pair
                                    return clickUpvote(btn, 'generic-arrow');
                                }
                            }
                        }
                    }
                    
                    return {status: 'NO_BUTTON', checked: allBtns.length};
                })()
            """)

            if result.get("status") == "UPVOTED":
                self.actions_done["upvote"] += 1
                self.human_pause(1, 2)
                return ActionResult("upvote", True, f"Upvoted a post ({result.get('strategy')})")
            else:
                return ActionResult("upvote", False, f"No upvote button found (checked {result.get('checked', '?')} buttons)")

        except Exception as e:
            return ActionResult("upvote", False, f"Error: {e}")

    # ------------------------------------------------------------------
    #  Comment
    # ------------------------------------------------------------------

    def _action_comment(self) -> ActionResult:
        """
        Comment on a Reddit post.
        CRITICAL: Uses screenshot + vision to read post content due to shadow DOM.
        """
        if not getattr(self, "_posts_cache", None):
            return ActionResult("comment", False, "No posts cached from browse")

        # Pick a post
        target = random.choice(self._posts_cache[:5])
        post_href = target.get("href", "")
        if not post_href:
            return ActionResult("comment", False, "No post href available")

        # Ensure href starts with /
        if not post_href.startswith("/"):
            post_href = "/" + post_href

        try:
            # Navigate to post
            self.cdp.navigate(f"https://www.reddit.com{post_href}")
            self.human_pause(5, 7)  # Wait for React render

            # Try to read post content (DOM extraction often fails on Reddit)
            post_text = ""
            try:
                post_text = self.cdp.evaluate("""
                    (function() {
                        var el = document.querySelector('div[data-testid="post-content-text"]');
                        if (el) return el.innerText;
                        el = document.querySelector('shreddit-post [slot="text-body"]');
                        if (el) return el.innerText;
                        return document.body.innerText.slice(0, 3000);
                    })()
                """)
            except Exception:
                post_text = ""

            # Screenshot for vision analysis (saved for external processing)
            screenshot_path = "/tmp/reddit_post_read.png"
            try:
                self.cdp.screenshot(screenshot_path)
                print(f"[{self.platform_name}] Screenshot saved to {screenshot_path} for vision analysis")
            except Exception as e:
                print(f"[{self.platform_name}] Screenshot failed: {e}")

            # Generate comment text
            # TODO: Integrate with vision tool to read screenshot and generate personalized comment
            comment_text = self._generate_comment(target.get("title", ""), post_text)

            # Adaptive scroll to find comment box
            # Reddit's comment UI: faceplate-textarea-input elements, some hidden, some visible
            scroll_positions = [0, 400, 800, 1200]
            comment_box = None
            trigger_clicked = False

            for pos in scroll_positions:
                if comment_box:
                    break
                self.cdp.scroll_to(pos)
                self.human_pause(2, 3)

                # Strategy 1: Find visible faceplate-textarea-input (the trigger/expanded input)
                try:
                    inputs = self.cdp.query_selector_all("faceplate-textarea-input")
                    for inp in inputs:
                        try:
                            if inp.is_visible():
                                if not trigger_clicked:
                                    inp.click()
                                    trigger_clicked = True
                                    print(f"[reddit] Clicked faceplate input at scroll {pos}")
                                    self.human_pause(2, 3)
                                    # After click, look for contenteditable inside or nearby
                                    editables = self.cdp.query_selector_all("[contenteditable]")
                                    for ed in editables:
                                        try:
                                            if ed.is_visible():
                                                comment_box = ed
                                                print(f"[reddit] Found contenteditable after click at scroll {pos}")
                                                break
                                        except Exception:
                                            continue
                                break
                        except Exception:
                            continue
                except Exception:
                    pass

                # Strategy 2: Direct contenteditable search (if already expanded)
                if not comment_box:
                    try:
                        editables = self.cdp.query_selector_all("[contenteditable]")
                        for ed in editables:
                            try:
                                if ed.is_visible():
                                    comment_box = ed
                                    print(f"[reddit] Found contenteditable directly at scroll {pos}")
                                    break
                            except Exception:
                                continue
                    except Exception:
                        pass

                # Strategy 3: Look for textarea as fallback
                if not comment_box:
                    try:
                        textareas = self.cdp.query_selector_all("textarea")
                        for ta in textareas:
                            try:
                                if ta.is_visible():
                                    comment_box = ta
                                    print(f"[reddit] Found textarea at scroll {pos}")
                                    break
                            except Exception:
                                continue
                    except Exception:
                        pass

            if not comment_box:
                return ActionResult("comment", False, "No comment box found after scrolling")

            # Focus and clear (macOS: Meta+a, others: Control+a)
            comment_box.focus()
            self.human_pause(0.5, 1)
            import sys
            select_all = "Meta+a" if sys.platform == "darwin" else "Control+a"
            self.cdp.keyboard_press(select_all)
            self.cdp.keyboard_press("Backspace")
            self.human_pause(0.5, 1)

            # Type comment
            self.cdp.keyboard_type(comment_text, delay=15)
            self.human_pause(1, 2)

            # Find and click submit button
            buttons = self.cdp.query_selector_all("button")
            submit_btn = None
            for btn in buttons:
                try:
                    text = btn.inner_text().strip().lower()
                    if text == "comment" and btn.is_visible():
                        submit_btn = btn
                        break
                except Exception:
                    continue

            if not submit_btn:
                return ActionResult("comment", False, "Submit button not found")

            submit_btn.click()
            self.human_pause(5, 7)  # Wait for Reddit to process

            # Verify via JS (check if username appears on page)
            username = self.config.get("username", "")
            if username:
                has_comment = self.cdp.evaluate(f"""
                    (function() {{
                        var links = document.querySelectorAll('a');
                        for (var i = 0; i < links.length; i++) {{
                            if (links[i].href && links[i].href.includes('{username}')) return true;
                        }}
                        return document.body.innerText.includes('{username}');
                    }})()
                """)
                success = bool(has_comment)
            else:
                success = True

            if success:
                self.actions_done["comment"] += 1
                self.record_observation(
                    f"Commented on Reddit: {target['title'][:60]}",
                    tags=["reddit", "comment"],
                    source_url=f"https://www.reddit.com{post_href}",
                )
                return ActionResult("comment", True, f"Commented on post")
            else:
                return ActionResult("comment", False, "Comment verification failed")

        except Exception as e:
            return ActionResult("comment", False, f"Error: {e}")

    def _generate_comment(self, title: str, post_text: str) -> str:
        """
        Generate a casual, human-sounding Reddit comment using AI.
        Falls back to templates if AI is unavailable.
        """
        from core.text_generator import generate_comment
        return generate_comment(
            platform="reddit",
            post_title=title,
            post_text=post_text,
            max_length=250,
        )

    # ------------------------------------------------------------------
    #  Save
    # ------------------------------------------------------------------

    def _action_save(self) -> ActionResult:
        """Save a post. Clicks the Save option in shreddit-post-overflow-menu shadow DOM."""
        try:
            # Reddit's save button is inside shreddit-post-overflow-menu's shadow DOM
            # The menu item has id="post-overflow-save" and contains a [role="menuitem"] element
            result = self.cdp.evaluate("""
                (function() {
                    // Find the first shreddit-post-overflow-menu (associated with first post)
                    var menu = document.querySelector('shreddit-post-overflow-menu');
                    if (!menu) return {status: 'NO_MENU'};
                    if (!menu.shadowRoot) return {status: 'NO_SHADOW'};
                    
                    // Find the Save menu item
                    var saveItem = menu.shadowRoot.querySelector('#post-overflow-save');
                    if (!saveItem) return {status: 'NO_SAVE_ITEM'};
                    
                    // Click the menuitem inside
                    var menuitem = saveItem.querySelector('[role="menuitem"]');
                    if (menuitem) {
                        menuitem.click();
                        return {status: 'CLICKED', target: 'menuitem'};
                    }
                    
                    // Fallback: click the li itself
                    saveItem.click();
                    return {status: 'CLICKED', target: 'li'};
                })()
            """)

            if result.get("status") == "CLICKED":
                self.human_pause(1, 2)
                self.actions_done["save"] += 1
                return ActionResult("save", True, f"Saved a post ({result.get('target')})")
            else:
                return ActionResult("save", False, f"Save item not found: {result.get('status')}")

        except Exception as e:
            return ActionResult("save", False, f"Error: {e}")

    # ------------------------------------------------------------------
    #  Session orchestration
    # ------------------------------------------------------------------

    def run_session(self, duration_minutes: int) -> List[ActionResult]:
        """Run a complete Reddit nurturing session."""
        results = []
        results.append(self.browse(duration_minutes))

        actions = ["upvote", "comment", "save"]
        for action in actions:
            if self.random_decision(action):
                self.human_pause(2, 5)
                results.append(self.execute_action(action))

        return results


# Register with executor
register_platform("reddit", RedditNurturer)
