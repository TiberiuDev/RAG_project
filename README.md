# RAG Project

A project implementing Retrieval-Augmented Generation (RAG) techniques.

## Features

- Document retrieval
- Contextual augmentation
- Integration with language models

## Getting Started

### Prerequisites

- Python 3.8+
- (Optional) [pip](https://pip.pypa.io/en/stable/installation/)
- (Optional) [Git](https://git-scm.com/)

### Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone <repo>
    cd RAG_project
    ```

2. **Configure environment variables:**
    - If you have custom settings, edit `.env` in the project root.
    - If `.env` does not exist, it will be created from `.env.example` when you start the project.

3. **Start the project using the batch file:**
    ```bat
    rag_llm.bat
    ```
    This script will:
    - Check for Python installation
    - Create and activate a virtual environment if needed
    - Install dependencies from `requirements.txt`
    - Ensure `.env` exists (copies from `.env.example` if missing)
    - Run the main application

4. **Manual start (alternative):**
    If you prefer manual steps:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    copy .env.example .env  # if .env does not exist
    python -m src.main
    ```

## Project Structure

```
RAG_project/
├── data/
├── src/
│   └── main.py
├── .env.example
├── .env         # (created on first run if missing)
├── requirements.txt
├── rag_llm.bat
└── README.md
```


## API Usage (Backend for Frontend Integration)

You can run the backend as a web API for integration with a frontend or other clients.

### Start the API server

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000
Interactive docs: http://localhost:8000/docs

### /ask Endpoint

- **POST** `/ask`
- **Request body:** `{ "question": "your question here" }`
- **Response:** `{ "answer": "..." }`

#### Example using curl

```bash
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"question\": \"E5\"}"
```

#### Example using PowerShell

```powershell
(Invoke-RestMethod -Uri "http://localhost:8000/ask" -Method Post -ContentType "application/json" -Body '{"question": "E5"}').answer
```

### CORS

CORS is enabled for all origins by default. For production, restrict `allow_origins` in `src/api.py` to your frontend's domain.

---

## Notes

- Edit `.env` to configure environment variables as needed.
- All dependencies are managed via `requirements.txt`.
- The main entry point for CLI is `src/main.py`.
- The main entry point for API is `src/api.py`.

## Troubleshooting

- If you encounter issues with missing dependencies or Python, ensure Python is installed and available in your PATH.
- For environment variable issues, check that `.env` exists and is properly configured.

---
```// filepath: c:\Users\tsuditu\Downloads\Repositories\RAG_project\README.md
# RAG Project

A project implementing Retrieval-Augmented Generation (RAG) techniques.

## Features

- Document retrieval
- Contextual augmentation
- Integration with language models

## Getting Started

### Prerequisites

- Python 3.8+
- (Optional) [pip](https://pip.pypa.io/en/stable/installation/)
- (Optional) [Git](https://git-scm.com/)

### Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone <repo>
    cd RAG_project
    ```

2. **Configure environment variables:**
    - If you have custom settings, edit `.env` in the project root.
    - If `.env` does not exist, it will be created from `.env.example` when you start the project.

3. **Start the project using the batch file:**
    ```bat
    rag_llm.bat
    ```
    This script will:
    - Check for Python installation
    - Create and activate a virtual environment if needed
    - Install dependencies from `requirements.txt`
    - Ensure `.env` exists (copies from `.env.example` if missing)
    - Run the main application

4. **Manual start (alternative):**
    If you prefer manual steps:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    copy .env.example .env  # if .env does not exist
    python -m src.main
    ```

## Project Structure

```
RAG_project/
├── data/
├── src/
│   └── main.py
├── .env.example
├── .env         # (created on first run if missing)
├── requirements.txt
├── rag_llm.bat
└── README.md
```

## Notes

- Edit `.env` to configure environment variables as needed.
- All dependencies are managed via `requirements.txt`.
- The main entry point is `src/main.py`.

## Troubleshooting

- If you encounter issues with missing dependencies or Python, ensure Python is installed and available in your PATH.
- For environment variable issues, check that `.env` exists and is properly configured.

---