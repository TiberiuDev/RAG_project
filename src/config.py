"""
Settings dataclass for configuration management.
Attributes:
  project_root (Path): The root directory of the project.
  data_dir (Path): Directory containing data files.
  docs_path (Path): Path to the main documents file.
  chunk_size_tokens (int): Number of tokens per chunk for token-based chunking.
  overlap_tokens (int): Number of overlapping tokens between chunks.
  top_k (int): Number of top results to retrieve.
  similarity_threshold (float): Minimum similarity score for retrieval; fallback if below threshold.
  openai_api_key (str): OpenAI API key, loaded from environment variable 'OPENAI_API_KEY'.
  llm_model (str): Name of the OpenAI LLM model, loaded from 'OPENAI_LLM_MODEL' or defaults to 'gpt-4.1-mini'.
  embed_model (str): Name of the OpenAI embedding model, loaded from 'OPENAI_EMBED_MODEL' or defaults to 'text-embedding-3-small'.
  tokenizer_model (str): Tokenizer model hint, loaded from 'OPENAI_LLM_MODEL' or defaults to 'gpt-4.1-mini'.
"""

from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv


if not os.path.exists('.env'):
    print("Warning: .env file not found. Using default environment variables.")
load_dotenv()

@dataclass(frozen=True)
class Settings:
    # Paths
    project_root: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = project_root / "data"
    docs_path: Path = data_dir / "docs.txt"

    # Token-based chunking
    chunk_size_tokens: int = 70
    overlap_tokens: int = 25

    # Retrieval
    top_k: int = 4
    similarity_threshold: float = 0.22  # if top score < threshold => fallback

    # OpenAI
    try:
      openai_api_key: str = os.environ["OPENAI_API_KEY"]
      llm_model: str = os.environ["OPENAI_LLM_MODEL"]
      embed_model: str = os.environ["OPENAI_EMBED_MODEL"]
    except KeyError:
      raise RuntimeError("Missing one of required environment variable from .env file. Please check.")

    # Tokenizer model hint (used by tiktoken)
    tokenizer_model: str = os.environ["OPENAI_LLM_MODEL"]

SETTINGS = Settings()
