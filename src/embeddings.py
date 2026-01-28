# src/embeddings.py

from openai import OpenAI
from .config import SETTINGS

_client = OpenAI(api_key=SETTINGS.openai_api_key)

def embed_text(text: str) -> list[float]:
    """
    Converts text into a vector embedding using a real embedding model.
    """
    response = _client.embeddings.create(
        model=SETTINGS.embed_model,  # ex: text-embedding-3-small
        input=text
    )
    return response.data[0].embedding
