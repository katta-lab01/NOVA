# scraper/reddit_scraper.py

import requests
from typing import List, Optional
import logging
import random
import time

# Import MemoryCleaner
from memory.cleaner import MemoryCleaner

class RedditScraper:
    """
    Scrapes top Reddit posts from a subreddit using Reddit's public JSON API.
    Uses randomized user-agent and delays to avoid detection.
    Can apply inline cleaning if needed.
    """

    USER_AGENTS = [
        "Mozilla/5.0 ... Chrome/120.0.0.0 ...",
        "Mozilla/5.0 ... Firefox/115.0 ...",
        # Add more user agents
    ]

    def __init__(self, min_score: int = 5, retries: int = 3, clean: bool = False, min_clean_length: int = 100):
        self.min_score = min_score
        self.retries = retries
        self.clean = clean
        self.cleaner = MemoryCleaner(min_length=min_clean_length) if clean else None

    def get_random_user_agent(self):
        return random.choice(self.USER_AGENTS)

    def scrape(self, subreddit: str, limit: int = 5, query: Optional[str] = None) -> List[str]:
        url = f"https://www.reddit.com/r/{subreddit}/top/.json?limit={limit}&t=day"
        for attempt in range(self.retries):
            headers = {'User-Agent': self.get_random_user_agent()}
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                posts = response.json().get("data", {}).get("children", [])

                chunks = []
                for post in posts:
                    data = post.get("data", {})
                    score = data.get("score", 0)
                    if score < self.min_score:
                        continue
                    title = data.get("title", "").strip()
                    body = data.get("selftext", "").strip()
                    content = f"Reddit Post: {title}\n{body}"
                    if query:
                        if query.lower() in title.lower() or query.lower() in body.lower():
                            chunks.append(content)
                    else:
                        chunks.append(content)

                # Inline cleaning if enabled
                if self.clean and self.cleaner:
                    chunks = self.cleaner.filter_chunks(chunks)

                time.sleep(random.uniform(1, 3))  # Random delay
                return chunks

            except Exception as e:
                logging.warning(f"[RedditScraper] Attempt {attempt+1} failed: {e}")
                time.sleep(random.uniform(2, 5))

        logging.error(f"[RedditScraper] Failed to scrape /r/{subreddit} after {self.retries} attempts.")
        return []
