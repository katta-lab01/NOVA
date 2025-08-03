# scraper/reddit_scraper.py

import requests
from typing import List, Optional
import logging

class RedditScraper:
    """
    Scrapes top Reddit posts from a subreddit using Reddit's public JSON API.
    Requires no login or API key. Returns post title + selftext.
    """

    def __init__(self, min_score: int = 5):
        self.min_score = min_score

    def scrape(self, subreddit: str, limit: int = 5, query: Optional[str] = None) -> List[str]:
        url = f"https://www.reddit.com/r/{subreddit}/top/.json?limit={limit}&t=day"
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; NOVA/1.0)'}

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

            return chunks

        except Exception as e:
            logging.error(f"[RedditScraper] Error scraping /r/{subreddit}: {e}")
            return []
