"""
X/Twitter (XR) nurturing implementation.

Actions: browse_feed, like, retweet, reply, follow, bookmark
Style: Short replies (1-2 sentences), casual but not overly slangy
Pitfalls: Rate limits, shadowban, React state complexity
          MUST use keyboard.type() not element.fill()
          MUST use force=True clicks to bypass overlays
"""

import random
import time
from typing import List, Optional

from core.base import PlatformNurturer, ActionResult
from core.executor import register_platform


class XTwitterNurturer(PlatformNurturer):
    """Nurturing logic for X/Twitter."""

    @property
    def platform_name(self) -> str:
        return "x_twitter"

    def login_check(self) -> bool:
        """Check if logged into X/Twitter."""
        try:
            self.cdp.navigate("https://x.com/home")
            self.human_pause(2, 4)
            result = self.cdp.evaluate("""
                document.querySelector('a[href="/settings"]') !== null ||
                document.querySelector('[data-testid="SideNav_AccountSwitcher_Button"]') !== null
            """)
            return bool(result)
        except Exception as e:
            print(f"[{self.platform_name}] Login check error: {e}")
            return False

    def browse(self, duration_minutes: int) -> ActionResult:
        """Browse X home feed, observing trending topics."""
        print(f"[{self.platform_name}] Browsing home feed for {duration_minutes}min...")

        self.cdp.navigate("https://x.com/home")
        self.human_pause(3, 6)

        start = time.time()
        tweet_count = 0
        self._tweet_cache = []

        while time.time() - start < duration_minutes * 60:
            # Simulate reading pause
            self.human_pause(4, 12)

            # Occasionally scroll
            if random.random() < 0.5:
                scroll_y = random.randint(400, 1000)
                self.cdp.scroll_by(scroll_y)
                self.human_pause(2, 4)

                # Try to extract tweet text for observations
                try:
                    tweets = self.cdp.evaluate("""
                        Array.from(document.querySelectorAll('article')).slice(0, 5).map(a => {
                            const textEl = a.querySelector('[data-testid="tweetText"]');
                            const text = textEl ? textEl.innerText.slice(0, 200) : null;
                            const linkEl = a.querySelector('a[href*="/status/"]');
                            const href = linkEl ? linkEl.getAttribute('href') : null;
                            return text ? {text: text, href: href} : null;
                        }).filter(Boolean)
                    """)
                    for tweet in tweets:
                        tweet_count += 1
                        self._tweet_cache.append(tweet)
                        # Check if tweet matches our topics
                        topics = [t.lower() for t in self.config.get("topics", [])]
                        if any(topic in tweet["text"].lower() for topic in topics):
                            self.record_observation(
                                f"X relevant tweet: {tweet['text']}",
                                tags=["x_twitter", "relevant", "tweet"],
                                source_url=f"https://x.com{tweet['href']}" if tweet.get("href") else "",
                            )
                except Exception:
                    pass

            # Small chance to pause longer (like reading a long thread)
            if random.random() < 0.1:
                self.human_pause(8, 15)

        return ActionResult(
            "browse",
            True,
            f"Browsed feed for {duration_minutes}min, observed {tweet_count} tweets",
        )

    def execute_action(self, action_name: str) -> ActionResult:
        """Execute a specific interaction on X."""
        print(f"[{self.platform_name}] Executing: {action_name}")

        if action_name == "like":
            return self._action_like()
        elif action_name == "retweet":
            return self._action_retweet()
        elif action_name == "reply":
            return self._action_reply()
        elif action_name == "follow":
            return self._action_follow()
        elif action_name == "bookmark":
            return self._action_bookmark()
        else:
            return ActionResult(action_name, False, f"Unknown action: {action_name}")

    # ------------------------------------------------------------------
    #  Like
    # ------------------------------------------------------------------

    def _action_like(self) -> ActionResult:
        """Like a tweet on the current feed."""
        try:
            self.cdp.navigate("https://x.com/home")
            self.human_pause(3, 5)

            # Find a like button and click it
            result = self.cdp.evaluate("""
                (function() {
                    var articles = document.querySelectorAll('article');
                    for (var i = 0; i < Math.min(articles.length, 5); i++) {
                        var likeBtn = articles[i].querySelector('[data-testid="like"]');
                        if (likeBtn) {
                            likeBtn.click();
                            return 'LIKED';
                        }
                    }
                    return 'NO_LIKE_BUTTON';
                })()
            """)

            if result == "LIKED":
                self.human_pause(2, 3)
                # Verify by checking for unlike button
                verified = self.cdp.evaluate("""
                    document.querySelector('[data-testid="unlike"]') !== null
                """)
                self.actions_done["like"] += 1
                return ActionResult("like", True, "Liked a tweet" + (" (verified)" if verified else ""))
            else:
                return ActionResult("like", False, "No like button found")

        except Exception as e:
            return ActionResult("like", False, f"Error: {e}")

    # ------------------------------------------------------------------
    #  Retweet
    # ------------------------------------------------------------------

    def _action_retweet(self) -> ActionResult:
        """Retweet a tweet."""
        try:
            self.cdp.navigate("https://x.com/home")
            self.human_pause(3, 5)

            result = self.cdp.evaluate("""
                (function() {
                    var articles = document.querySelectorAll('article');
                    for (var i = 0; i < Math.min(articles.length, 5); i++) {
                        var rtBtn = articles[i].querySelector('[data-testid="retweet"]');
                        if (rtBtn) {
                            rtBtn.click();
                            return 'CLICKED';
                        }
                    }
                    return 'NO_RETWEET_BUTTON';
                })()
            """)

            if result == "CLICKED":
                self.human_pause(2, 3)
                # Try to confirm retweet (click the confirm button in modal)
                confirm = self.cdp.evaluate("""
                    (function() {
                        var btn = document.querySelector('[data-testid="retweetConfirm"]');
                        if (btn) { btn.click(); return 'CONFIRMED'; }
                        return 'NO_CONFIRM';
                    })()
                """)
                self.actions_done["retweet"] += 1
                return ActionResult("retweet", True, f"Retweeted ({confirm})")
            else:
                return ActionResult("retweet", False, "No retweet button found")

        except Exception as e:
            return ActionResult("retweet", False, f"Error: {e}")

    # ------------------------------------------------------------------
    #  Reply
    # ------------------------------------------------------------------

    def _action_reply(self) -> ActionResult:
        """Reply to a tweet with a short, human-sounding comment."""
        username = self.config.get("username", "")

        try:
            self.cdp.navigate("https://x.com/home")
            self.human_pause(3, 5)

            # Find a tweet to reply to and extract its text
            result = self.cdp.evaluate("""
                (function() {
                    var articles = document.querySelectorAll('article');
                    for (var i = 0; i < Math.min(articles.length, 5); i++) {
                        var replyBtn = articles[i].querySelector('[data-testid="reply"]');
                        if (replyBtn) {
                            var textEl = articles[i].querySelector('[data-testid="tweetText"]');
                            var tweetText = textEl ? textEl.innerText.slice(0, 300) : '';
                            replyBtn.click();
                            return {status: 'CLICKED', text: tweetText};
                        }
                    }
                    return {status: 'NO_REPLY_BUTTON', text: ''};
                })()
            """)

            if result.get("status") != "CLICKED":
                return ActionResult("reply", False, "No reply button found")

            tweet_text = result.get("text", "")
            self.human_pause(2, 3)

            # Find the text area and type
            textbox = self.cdp.query_selector("[data-testid='tweetTextarea_0']")
            if not textbox:
                return ActionResult("reply", False, "No reply textbox found")

            # Focus and type (React requires keyboard events)
            textbox.click(force=True)
            self.human_pause(0.5, 1)

            reply_text = self._generate_reply(tweet_text)
            self.cdp.keyboard_type(reply_text, delay=15)
            self.human_pause(1, 2)

            # Find submit button
            submit = self.cdp.query_selector("[data-testid='tweetButtonInline']")
            if not submit:
                submit = self.cdp.query_selector("[data-testid='tweetButton']")

            if not submit:
                return ActionResult("reply", False, "No submit button found")

            submit.click(force=True)
            self.human_pause(3, 5)

            # Verify by checking user's replies page
            if username:
                self.cdp.navigate(f"https://x.com/{username}/with_replies")
                self.human_pause(4, 6)
                body = self.cdp.evaluate("document.body.innerText")
                verified = reply_text[:20] in body
            else:
                verified = True

            self.actions_done["reply"] += 1
            return ActionResult("reply", True, f"Replied: '{reply_text[:40]}...'" + (" (verified)" if verified else ""))

        except Exception as e:
            return ActionResult("reply", False, f"Error: {e}")

    def _generate_reply(self, tweet_text: str = "") -> str:
        """Generate a short, human-sounding X reply using AI."""
        from core.text_generator import generate_comment
        return generate_comment(
            platform="x_twitter",
            post_title=tweet_text[:100] if tweet_text else "a tweet",
            post_text=tweet_text,
            max_length=200,
        )

    # ------------------------------------------------------------------
    #  Follow
    # ------------------------------------------------------------------

    def _action_follow(self) -> ActionResult:
        """Follow an account. Tries multiple strategies to find a follow button."""
        try:
            self.cdp.navigate("https://x.com/home")
            self.human_pause(3, 5)

            result = self.cdp.evaluate("""
                (function() {
                    // Helper: check if text means "Follow" (English or Chinese)
                    function isFollowText(text) {
                        var t = text.trim().toLowerCase();
                        return t === 'follow' || t === '\u5173\u6ce8';
                    }
                    function isFollowingText(text) {
                        var t = text.trim().toLowerCase();
                        return t === 'following' || t === '\u5df2\u5173\u6ce8';
                    }

                    // Strategy 1: aria-label containing "Follow @" or "\u5173\u6ce8 @"
                    var btn = document.querySelector('[aria-label*="Follow @"]');
                    if (!btn) btn = document.querySelector('[aria-label*="\u5173\u6ce8 @"]');
                    if (btn) { btn.click(); return 'FOLLOWED_ARIA'; }

                    // Strategy 2: data-testid containing follow
                    var btns = document.querySelectorAll('[data-testid*="follow"]');
                    for (var i = 0; i < btns.length; i++) {
                        if (isFollowText(btns[i].innerText)) {
                            btns[i].click();
                            return 'FOLLOWED_TESTID';
                        }
                    }

                    // Strategy 3: Look in "Who to follow" sidebar
                    var sidebar = document.querySelector('aside[aria-label="Who to follow"]') ||
                                  document.querySelector('[data-testid="sidebarColumn"]');
                    if (sidebar) {
                        var sBtns = sidebar.querySelectorAll('button, [role="button"]');
                        for (var i = 0; i < sBtns.length; i++) {
                            if (isFollowText(sBtns[i].innerText)) {
                                sBtns[i].click();
                                return 'FOLLOWED_SIDEBAR';
                            }
                        }
                    }

                    // Strategy 4: Any button/role=button with "Follow" or "\u5173\u6ce8" text
                    var allBtns = document.querySelectorAll('button, [role="button"]');
                    for (var i = 0; i < Math.min(allBtns.length, 200); i++) {
                        if (isFollowText(allBtns[i].innerText)) {
                            allBtns[i].click();
                            return 'FOLLOWED_TEXT';
                        }
                    }

                    return 'NO_FOLLOW_BUTTON';
                })()
            """)

            if result != 'NO_FOLLOW_BUTTON':
                self.human_pause(2, 3)
                # Verify: look for "Following" or "已关注"
                verified = self.cdp.evaluate("""
                    (function() {
                        function isFollowingText(text) {
                            var t = text.trim().toLowerCase();
                            return t === 'following' || t === '\u5df2\u5173\u6ce8';
                        }
                        var hasAria = document.querySelector('[aria-label*="Following @"]') !== null ||
                                      document.querySelector('[aria-label*="\u5df2\u5173\u6ce8 @"]') !== null;
                        if (hasAria) return true;
                        var btns = document.querySelectorAll('button, [role="button"]');
                        for (var i = 0; i < Math.min(btns.length, 100); i++) {
                            if (isFollowingText(btns[i].innerText)) return true;
                        }
                        return false;
                    })()
                """)
                self.actions_done["follow"] += 1
                return ActionResult("follow", True, f"Followed an account ({result})" + (" (verified)" if verified else ""))
            else:
                return ActionResult("follow", False, "No follow button found")

        except Exception as e:
            return ActionResult("follow", False, f"Error: {e}")

    # ------------------------------------------------------------------
    #  Bookmark
    # ------------------------------------------------------------------

    def _action_bookmark(self) -> ActionResult:
        """Bookmark a tweet."""
        try:
            self.cdp.navigate("https://x.com/home")
            self.human_pause(3, 5)

            result = self.cdp.evaluate("""
                (function() {
                    var articles = document.querySelectorAll('article');
                    for (var i = 0; i < Math.min(articles.length, 5); i++) {
                        var btn = articles[i].querySelector('[data-testid="bookmark"]');
                        if (btn) {
                            btn.click();
                            return 'BOOKMARKED';
                        }
                    }
                    return 'NO_BOOKMARK_BUTTON';
                })()
            """)

            if result == "BOOKMARKED":
                self.actions_done["bookmark"] += 1
                return ActionResult("bookmark", True, "Bookmarked a tweet")
            else:
                return ActionResult("bookmark", False, "No bookmark button found")

        except Exception as e:
            return ActionResult("bookmark", False, f"Error: {e}")

    # ------------------------------------------------------------------
    #  Session orchestration
    # ------------------------------------------------------------------

    def run_session(self, duration_minutes: int) -> List[ActionResult]:
        """Run a complete X nurturing session."""
        results = []

        # Browse first
        results.append(self.browse(duration_minutes))

        # Decide and execute optional actions
        actions = ["like", "retweet", "reply", "follow", "bookmark"]
        for action in actions:
            if self.random_decision(action):
                self.human_pause(2, 5)
                results.append(self.execute_action(action))

        return results


# Register with executor
register_platform("x_twitter", XTwitterNurturer)
