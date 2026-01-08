from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class VectorItem:
    """
    A single entry stored in the vector store.

    A VectorItem represents one indexed text chunk together with:
    - its numeric embedding (vector representation),
    - optional metadata used for tracing, filtering, or debugging.

    In a RAG system, each chunk of text becomes exactly one VectorItem.
    """
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]


class InMemoryVectorStore:
    """
    A minimal in-memory vector store.

    This class stores VectorItem objects in RAM for the lifetime of
    the Python process. It acts as a simplified stand-in for a real
    vector database (e.g. FAISS, Chroma, Pinecone).

    High-level execution flow:
    1. VectorItem objects are created during document ingestion.
    2. Each VectorItem is added to the store via `add(...)`.
    3. The store keeps all items in memory without indexing or persistence.
    4. Other components retrieve all stored items and perform
       similarity search externally.

    This implementation is intentionally simple and suitable for:
    - learning and prototyping RAG systems
    - testing chunking and embedding pipelines
    - avoiding external dependencies.

    It does NOT provide:
    - vector indexing
    - similarity search
    - persistence to disk
    - concurrency or scaling guarantees.
    """

    def __init__(self) -> None:
        """
        Initialize an empty in-memory vector store.

        All vectors are kept in a simple Python list and exist only
        for the lifetime of this process.
        """
        self.items: List[VectorItem] = []

    def add(self, item: VectorItem) -> None:
        """
        Add a single VectorItem to the store.

        This method is typically called during the ingestion phase,
        after a text chunk has been embedded.
        """
        self.items.append(item)

    def all(self) -> List[VectorItem]:
        """
        Return all stored VectorItem objects.

        This method does not perform any filtering or ranking.
        Consumers of this store are expected to compute similarity
        scores and select relevant items themselves.
        """
        return self.items
