"""
Module for splitting text into overlapping chunks based on token count.
"""

from typing import List
import tiktoken

def chunk_text_by_tokens(
    text: str,
    chunk_size_tokens: int,
    overlap_tokens: int,
    model_name: str
) -> List[str]:
    """
    Splits the input text into overlapping chunks based on token count.

    Args:
        text (str): The input text to be chunked.
        chunk_size_tokens (int): The number of tokens per chunk.
        overlap_tokens (int): The number of tokens to overlap between chunks.
        model_name (str): The model name for tiktoken encoding.

    Returns:
        List[str]: A list of text chunks.

    Raises:
        ValueError: If overlap_tokens is greater than or equal to chunk_size_tokens.
    """
    if overlap_tokens >= chunk_size_tokens:
        raise ValueError("overlap_tokens must be < chunk_size_tokens")

    # Get the encoding for the specified model
    enc = tiktoken.encoding_for_model(model_name)
    # Encode the text into tokens
    tokens = enc.encode(text)

    chunks: List[str] = []
    start = 0
    n = len(tokens)

    # Iterate over the tokens, creating overlapping chunks
    while start < n:
        end = min(start + chunk_size_tokens, n)
        # Decode the current chunk of tokens back to text
        chunk = enc.decode(tokens[start:end]).strip()
        if chunk:
            chunks.append(chunk)

        if end == n:
            break

        # Move the start index forward, keeping the specified overlap
        start = end - overlap_tokens

    return chunks
