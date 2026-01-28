# src/main.py
from .rag_pipeline import build_store_from_csv_safe, cli_loop


def main():
    store = build_store_from_csv_safe()
    cli_loop(store)


if __name__ == "__main__":
    main()
