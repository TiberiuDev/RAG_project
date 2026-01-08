"""
prompts.py

This module contains prompt templates and helper functions for constructing prompts
used in Retrieval-Augmented Generation (RAG) IT support assistant applications.
"""

from typing import List

# System prompt instructing the assistant to use only the provided documents for answers.
SYSTEM_PROMPT = (
    "You are an IT support assistant.\n"
    "Use ONLY the provided DOCUMENTS.\n"
    "If the answer is not explicitly present, say: \"I don't know based on the provided documents.\""
)

def build_rag_prompt(question: str, retrieved_chunks: List[str]) -> str:
    """
    Build a prompt for the RAG model by combining the system prompt, retrieved document chunks, and the user's question.

    Args:
        question (str): The user's question.
        retrieved_chunks (List[str]): List of relevant document text chunks.

    Returns:
        str: The formatted prompt to be sent to the language model.
    """
    # Join retrieved document chunks with separators for clarity.
    context = "\n\n---\n\n".join(retrieved_chunks).strip()
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"DOCUMENTS:\n{context}\n\n"
        f"QUESTION:\n{question}\n\n"
        f"ANSWER:"
    )
