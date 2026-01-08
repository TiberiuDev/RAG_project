from typing import List, Optional, Tuple
from .config import SETTINGS
from .chunking import chunk_text_by_tokens
from .embeddings import embed
from .vector_store import InMemoryVectorStore, VectorItem
from .retrieval import top_k_search
from .prompts import build_rag_prompt
from .llm_client import ask_llm

def load_documents() -> str:
    if not SETTINGS.docs_path.exists():
        raise FileNotFoundError(f"docs.txt not found at: {SETTINGS.docs_path}")
    return SETTINGS.docs_path.read_text(encoding="utf-8", errors="ignore")

def build_store(doc_text: str) -> InMemoryVectorStore:
    """
    Splits the input document text into token-based chunks, generates embeddings for each chunk,
    and stores them in an in-memory vector store.
    Args:
        doc_text (str): The full text of the document to be indexed.
    Returns:
        InMemoryVectorStore: A vector store containing all chunk embeddings and their metadata.
    Notes:
        - Chunking parameters (chunk size, overlap, tokenizer model) are taken from SETTINGS.
        - Embeddings are generated using the `embed` function.
        - Each chunk is stored with its text, embedding, and a unique chunk ID in the metadata.
        - Progress is printed every 10 chunks during indexing.
    """
    # Split the document text into overlapping token-based chunks
    chunks = chunk_text_by_tokens(
        doc_text,
        chunk_size_tokens=SETTINGS.chunk_size_tokens,
        overlap_tokens=SETTINGS.overlap_tokens,
        model_name=SETTINGS.tokenizer_model
    )

    # Initialize an in-memory vector store to hold chunk embeddings
    store = InMemoryVectorStore()
    print(f"Indexing {len(chunks)} token-chunks with real embeddings...")

    # For each chunk, generate its embedding and add it to the store
    for i, ch in enumerate(chunks):
        if i % 10 == 0:
            print(f"  chunk {i+1}/{len(chunks)}")
        emb = embed(ch)
        store.add(VectorItem(text=ch, embedding=emb, metadata={"chunk_id": i}))

    return store

def retrieve(question: str, store: InMemoryVectorStore) -> Tuple[float, List[str]]:
    # Embed the question for similarity search
    q_emb = embed(question)
    # Retrieve top-k most similar chunks from the store
    scored = top_k_search(q_emb, store, k=SETTINGS.top_k)

    if not scored:
        return -1.0, []
    # Get the top similarity score and corresponding chunk texts
    top_score = scored[0][0]
    docs = [item.text for _, item in scored]
    return top_score, docs

def answer_question(question: str, store: Optional[InMemoryVectorStore] = None) -> str:
    # If no store is provided, load documents and build the store
    if store is None:
        doc_text = load_documents()
        store = build_store(doc_text)

    # Retrieve relevant chunks for the question
    top_score, retrieved = retrieve(question, store)

    # Fallback: if similarity is too low, do not answer
    if top_score < SETTINGS.similarity_threshold:
        return "I don't know based on the provided documents."

    # Build the prompt for the LLM using the question and retrieved chunks
    prompt = build_rag_prompt(question, retrieved)
    # Get the answer from the LLM
    return ask_llm(prompt)
