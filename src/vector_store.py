# src/vector_store.py
from dataclasses import dataclass
from typing import List, Dict, Any
import math

@dataclass
class VectorItem:
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]

class VectorStore:
    """
    Simple in-memory vector store.
    Holds embeddings + metadata and performs cosine similarity search.
    """

    def __init__(self):
        self.items: List[VectorItem] = []

    def add(self, item: VectorItem):
        self.items.append(item)

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        return dot / (norm1 * norm2)

    def search(self, query_embedding: List[float], top_k: int = 3):
        """
        Returns top_k VectorItem sorted by similarity (desc).
        """
        scored = []
        for item in self.items:
            score = self._cosine_similarity(query_embedding, item.embedding)
            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]
