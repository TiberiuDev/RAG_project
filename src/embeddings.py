from typing import List
from openai import OpenAI
from .config import SETTINGS

_client = OpenAI(api_key=SETTINGS.openai_api_key)

def embed(text: str) -> List[float]:
    """
    Generate an embedding vector for the given text using the specified embedding model.
    Args:
        text (str): The input text to be embedded.
    Returns:
        List[float]: The embedding vector representing the input text. Returns an empty list if the input text is empty or only whitespace.
    Raises:
        Any exceptions raised by the underlying embedding client.
    Note:
        The function expects the existence of a global `_client` with an `embeddings.create` method and a `SETTINGS.embed_model` attribute.
    """
    text = text.strip()
    if not text:
        return []

    # Calls the embedding model client to generate the embedding for the input text.
    resp = _client.embeddings.create(
        model=SETTINGS.embed_model,
        input=text
    )
    return resp.data[0].embedding
