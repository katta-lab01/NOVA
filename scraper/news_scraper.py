import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import logging
import random
import time

class NewsScraper:
    """
    Scrapes news or blog articles from general websites using HTML parsing.
    Uses randomized user-agent and delays to avoid detection.
    """

    USER_AGENTS = [
        "Mozilla/5.0 ... Chrome/120.0.0.0 ...",
        "Mozilla/5.0 ... Firefox/115.0 ...",
        # Add more user agents
    ]

    def __init__(self, min_length: int = 100, retries: int = 3):
        self.min_length = min_length
        self.retries = retries

    def get_random_user_agent(self):
        return random.choice(self.USER_AGENTS)

    def scrape(self, url: str, query: Optional[str] = None) -> List[str]:
        for attempt in range(self.retries):
            try:
                headers = {
                    "User-Agent": self.get_random_user_agent()
                }
                response = requests.get(url, timeout=10, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Remove noise
                for tag in soup(['script', 'style', 'footer', 'nav', 'header', 'svg']):
                    tag.decompose()

                # Extract paragraphs and heading content
                candidates = soup.find_all(['h1', 'h2', 'h3', 'p', 'article'])
                chunks = []
                for el in candidates:
                    text = el.get_text(separator=' ', strip=True)
                    if len(text) >= self.min_length:
                        if query:
                            if query.lower() in text.lower():
                                chunks.append(text)
                        else:
                            chunks.append(text)

                # Random delay to mimic human browsing
                time.sleep(random.uniform(1, 3))
                return chunks

            except Exception as e:
                logging.warning(f"[NewsScraper] Attempt {attempt+1} failed: {e}")
                time.sleep(random.uniform(2, 5))

        logging.error(f"[NewsScraper] Failed to scrape {url} after {self.retries} attempts.")
        return []