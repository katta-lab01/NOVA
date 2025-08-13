# memory/embedder.py

from typing import List, Optional
import logging
from sentence_transformers import SentenceTransformer

# Import NewsScraper and RedditScraper
from scraper.news_scraper import NewsScraper
from scraper.reddit_scraper import RedditScraper

# Import MemoryCleaner
from memory.cleaner import MemoryCleaner

class Embedder:
    """
    Handles text embedding using a local SentenceTransformer model.
    Can optionally clean text before encoding.
    No external API calls required.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", clean_before_encode: bool = False, min_clean_length: int = 100):
        try:
            self.model = SentenceTransformer(model_name)
            self.clean_before_encode = clean_before_encode
            self.cleaner = MemoryCleaner(min_length=min_clean_length) if clean_before_encode else None
        except Exception as e:
            logging.error(f"[Embedder] Failed to load embedding model '{model_name}': {e}")
            raise

    def embed_text_chunks(self, chunks: List[str]) -> List[List[float]]:
        try:
            if self.clean_before_encode and self.cleaner:
                chunks = self.cleaner.filter_chunks(chunks)
            embeddings = self.model.encode(chunks, show_progress_bar=False, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            logging.error(f"[Embedder] Failed to embed text chunks: {e}")
            return []

    def embed_news_from_url(self, url: str, query: Optional[str] = None) -> List[List[float]]:
        """
        Scrapes news paragraphs from a URL and returns their embeddings.
        Optionally cleans paragraphs before embedding.
        """
        try:
            news_scraper = NewsScraper()
            paragraphs = news_scraper.scrape(url, query=query)
            if not paragraphs:
                logging.warning(f"[Embedder] No news paragraphs found for URL: {url}")
                return []
            return self.embed_text_chunks(paragraphs)
        except Exception as e:
            logging.error(f"[Embedder] Failed to embed news from {url}: {e}")
            return []

    def embed_reddit_threads(self, subreddit: str, limit: int = 5, query: Optional[str] = None) -> List[List[float]]:
        """
        Scrapes Reddit threads from a subreddit and returns their embeddings.
        Optionally cleans threads before embedding.
        """
        try:
            reddit_scraper = RedditScraper()
            threads = reddit_scraper.scrape(subreddit, limit=limit, query=query)
            if not threads:
                logging.warning(f"[Embedder] No Reddit threads found for subreddit: {subreddit}")
                return []
            return self.embed_text_chunks(threads)
        except Exception as e:
            logging.error(f"[Embedder] Failed to embed Reddit threads from /r/{subreddit}: {e}")
            return []
