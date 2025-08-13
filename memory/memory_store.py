# memory/memory_store.py

from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict
import os
from config import MONGO_URI

# Import MemoryCleaner
from memory.cleaner import MemoryCleaner

class MemoryStore:
    """
    Handles document-level memory using MongoDB for long-term textual storage.
    Metadata like source, timestamps, type can be stored for filtering and timeline.
    """

    def __init__(self, db_name: str = "nova_memory", collection: str = "documents", min_clean_length: int = 100):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[db_name]
        self.collection = self.db[collection]
        self.cleaner = MemoryCleaner(min_length=min_clean_length)

    def save_documents(self, chunks: List[str], source: str, tags: List[str] = []):
        # Clean and filter chunks before saving
        cleaned_chunks = self.cleaner.filter_chunks(chunks)
        now = datetime.utcnow()
        docs = [
            {
                "text": chunk,
                "source": source,
                "tags": tags,
                "created_at": now
            } for chunk in cleaned_chunks
        ]
        if docs:
            self.collection.insert_many(docs)

    def search_documents(self, query: Dict, limit: int = 10) -> List[Dict]:
        return list(self.collection.find(query).sort("created_at", -1).limit(limit))

    def get_all_documents(self) -> List[Dict]:
        return list(self.collection.find().sort("created_at", -1))

    def delete_all_documents(self):
        self.collection.delete_many({})
