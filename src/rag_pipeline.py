# src/rag_pipeline.py
import re
import traceback
from typing import Optional

from .csv_loader import load_error_records_from_csv
from .embeddings import embed_text
from .vector_store import VectorStore, VectorItem


def build_store_from_csv_safe() -> VectorStore:
    """
    Loads records from CSV, generates embeddings, and stores them in an in-memory VectorStore.
    """
    try:
        print("Loading records from CSV...")
        records = load_error_records_from_csv()
        print(f"Loaded {len(records)} records.")
    except FileNotFoundError as fe:
        print("CSV file not found. Put the csv in data/ or update SETTINGS.")
        print("Detail:", fe)
        raise SystemExit(1)
    except Exception:
        print("Failed reading CSV:")
        traceback.print_exc()
        raise SystemExit(1)

    store = VectorStore()
    print("Indexing records (embeddings)...")

    for i, rec in enumerate(records, start=1):
        text = rec.as_text()

        try:
            emb = embed_text(text)
        except Exception as e:
            print(f"Embedding error on record {i} (code={rec.error_code}): {e}")
            traceback.print_exc()
            raise SystemExit(1)

        store.add(
            VectorItem(
                text=text,
                embedding=emb,
                metadata={
                    "error_code": rec.error_code,
                    "sheet": rec.sheet,
                    "origin_field": rec.origin_field,
                    "owner": rec.owner,
                },
            )
        )

        if i % 10 == 0 or i == len(records):
            print(f"  indexed {i}/{len(records)}")

    print("Indexing complete.")
    return store


def format_hr_answer(item_text: str) -> str:
    """
    Converts the raw record text into a human-friendly output for HR.
    """
    lines = item_text.splitlines()
    fields = {}

    for ln in lines:
        if ":" in ln:
            k, v = ln.split(":", 1)
            fields[k.strip()] = v.strip()

    return (
        f"Meaning: {fields.get('Title', 'N/A')}\n"
        f"Non-technical explanation: {fields.get('Non-technical explanation', 'N/A')}\n"
        f"Where to correct: {fields.get('Origin field', 'N/A')}\n"
        f"Owner: {fields.get('Owner / Responsible', 'N/A')}\n"
    )


def simple_answer_pipeline(
    question: str,
    store: VectorStore,
    similarity_threshold: Optional[float] = 0.60,
) -> str:
    """
    1) Exact-match on error code if present (e.g., E5)
    2) Otherwise semantic search top-1
    3) Optional threshold fallback to avoid out-of-domain answers
    """
    # Exact match on codes like E5, E11 etc.
    code_match = re.search(r"\b(E\d+)\b", question, flags=re.IGNORECASE)
    if code_match:
        code = code_match.group(1).upper()
        for item in store.items:
            meta_code = (item.metadata.get("error_code") or "").upper()
            if meta_code == code:
                return format_hr_answer(item.text)

    # Semantic search (top-1)
    q_emb = embed_text(question)
    results = store.search(q_emb, top_k=3)
    if not results:
        return (
            "I can only help with Hire Sync validation errors from the internal checklist.\n"
            "Please paste the exact error message or provide the error ID (e.g., E5)."
        )

    best_score, best_item = results[0]

    # Threshold fallback (prevents answering unrelated questions)
    if similarity_threshold is not None and best_score < similarity_threshold:
        # if still somewhat related, return best match instead of refusing
        if best_score >= 0.45:
            return format_hr_answer(best_item.text)
        return (
            "I can only help with Hire Sync validation errors from the internal checklist.\n"
            "Please paste the exact error message or provide the error ID (e.g., E5)."
        )

    return format_hr_answer(best_item.text)


def cli_loop(store: VectorStore) -> None:
    """
    Simple interactive CLI loop.
    """
    print("\nREADY: Type a question about an error (or 'exit' to quit).")

    while True:
        try:
            q = input("Q> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not q:
            continue

        if q.lower() in {"exit", "quit"}:
            print("Bye.")
            break

        try:
            ans = simple_answer_pipeline(q, store=store)
            print("\n" + ans + "\n")
        except Exception:
            print("Failed to answer the question. See detail below:")
            traceback.print_exc()
