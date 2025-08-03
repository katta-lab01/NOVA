import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import logging

class NewsScraper:
    """
    Scrapes news or blog articles from general websites using HTML parsing.
    Works best on clean article-style pages.
    """

    def __init__(self, min_length: int = 100):
        self.min_length = min_length

    def scrape(self, url: str, query: Optional[str] = None) -> List[str]:
        try:
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (compatible; NOVA/1.0)"
            })
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

            return chunks

        except Exception as e:
            logging.error(f"[NewsScraper] Failed to scrape {url}: {e}")
            return []