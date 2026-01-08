"""
retrieval.py

This module provides functions for computing cosine similarity between vectors and retrieving
the top-k most similar items from an in-memory vector store.
"""

from typing import List, Tuple
import math
from .vector_store import InMemoryVectorStore, VectorItem

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """
    Compute the cosine similarity between two vectors.

    Args:
        v1 (List[float]): First vector.
        v2 (List[float]): Second vector.

    Returns:
        float: Cosine similarity score, or -1.0 if vectors are invalid.
    """
    # Check for valid input vectors
    if not v1 or not v2 or len(v1) != len(v2):
        return -1.0
    # Compute dot product and norms
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a * a for a in v1)) or 1.0
    n2 = math.sqrt(sum(b * b for b in v2)) or 1.0
    return dot / (n1 * n2)

def top_k_search(query_emb: List[float], store: InMemoryVectorStore, k: int) -> List[Tuple[float, VectorItem]]:
    """
    Retrieve the top-k items from the vector store most similar to the query embedding.

    Args:
        query_emb (List[float]): Query embedding vector.
        store (InMemoryVectorStore): The vector store to search.
        k (int): Number of top items to return.

    Returns:
        List[Tuple[float, VectorItem]]: List of tuples (similarity score, VectorItem), sorted by score descending.
    """
    scored: List[Tuple[float, VectorItem]] = []
    # Score each item in the store by cosine similarity to the query
    for item in store.all():
        score = cosine_similarity(query_emb, item.embedding)
        scored.append((score, item))
    # Sort items by similarity score in descending order
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:k]
