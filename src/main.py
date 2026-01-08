"""
Main entry point for the Mini RAG (Retrieval-Augmented Generation) application.

This script loads documents, builds a vector store for retrieval, and provides
an interactive command-line interface for users to ask questions.
"""

from .rag_pipeline import load_documents, build_store, answer_question

def main():
    """
    Loads documents, builds the vector store, and starts the interactive Q&A loop.
    """
    print("Loading documents and building vector store...")
    doc_text = load_documents()  # Load raw documents from source

    print("Indexing documents into vector store...")
    store = build_store(doc_text)  # Build vector store for retrieval
    print("Vector store built.\n")

    print("Mini RAG ready. Type a question (or 'exit').\n")
    while True:
        q = input("Q> ").strip()
        if not q:
            continue  # Skip empty input
        if q.lower() in {"exit", "quit"}:
            break  # Exit loop on user command

        # Retrieve and generate answer using the RAG pipeline
        out = answer_question(q, store=store)
        print("\n" + out + "\n")

if __name__ == "__main__":
    main()
