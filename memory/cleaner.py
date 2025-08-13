# memory/cleaner.py

import re
from typing import List

class MemoryCleaner:
    """
    Cleans and filters noisy or irrelevant content before embedding or saving.
    Useful to prevent memory pollution.
    """

    def __init__(self, min_length: int = 100):
        self.min_length = min_length
        self.patterns_to_remove = [
            r"\[.*?\]",      # Remove [links]
            r"https?://\S+",  # Remove URLs
            r"\n{2,}",         # Remove extra newlines
            r"\s{2,}"          # Extra spaces
        ]

    def clean(self, text: str) -> str:
        for pattern in self.patterns_to_remove:
            text = re.sub(pattern, " ", text)
        text = text.strip()
        return text

    def filter_chunks(self, chunks: List[str]) -> List[str]:
        cleaned = [self.clean(chunk) for chunk in chunks]
        return [chunk for chunk in cleaned if len(chunk) >= self.min_length]