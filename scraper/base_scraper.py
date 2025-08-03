# scraper/base_scraper.py

from typing import List, Optional
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import random
import time


class BaseScraper:
    """
    Universal web scraper that uses Playwright + BeautifulSoup
    to extract clean, readable content from any web page.
    """

    USER_AGENTS = [
        "Mozilla/5.0 ... Chrome/120.0.0.0 ...",
        "Mozilla/5.0 ... Firefox/115.0 ...",
        # Add more user agents
    ]

    def __init__(self, chunk_size: int = 512):
        self.chunk_size = chunk_size

    def get_random_user_agent(self):
        return random.choice(self.USER_AGENTS)

    async def _fetch_html(self, url: str) -> Optional[str]:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.get_random_user_agent()
                )
                page = await context.new_page()
                await page.goto(url, timeout=20000)
                await page.wait_for_load_state("networkidle", timeout=10000)
                content = await page.content()
                await browser.close()
                # Random delay to mimic human browsing
                time.sleep(random.uniform(2, 5))
                return content
        except Exception as e:
            print(f"[BaseScraper] Failed to fetch {url}: {e}")
            return None

    def _clean_html(self, html: str, query: Optional[str] = None) -> List[str]:
        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "footer", "nav", "header", "noscript", "svg"]):
            tag.decompose()

        # If a query is provided, filter elements containing the query
        if query:
            elements = [el for el in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "article", "li", "span"])
                        if query.lower() in el.get_text(separator=" ", strip=True).lower()]
        else:
            elements = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "article", "li", "span"])

        text = "\n".join([el.get_text(separator=" ", strip=True) for el in elements])

        # Clean up extra spacing
        text = re.sub(r"\n{2,}", "\n", text)
        return self._chunk_text(text)

    def _chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size):
            chunk = " ".join(words[i:i + self.chunk_size]).strip()
            if len(chunk) > 100:  # Only keep meaningful chunks
                chunks.append(chunk)
        return chunks

    async def scrape_url(self, url: str, query: Optional[str] = None) -> List[str]:
        html = await self._fetch_html(url)
        if not html:
            return []
        return self._clean_html(html, query=query)

    def scrape(self, url: str, query: Optional[str] = None) -> List[str]:
        return asyncio.run(self.scrape_url(url, query=query))
