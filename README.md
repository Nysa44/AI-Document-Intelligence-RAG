# AI Document Intelligence & RAG Assistant

A complete Retrieval-Augmented Generation (RAG) application for querying project documents with semantic search, FAISS vector retrieval, and LLM-generated answers with source citations.

## Core pipeline

PDF / DOCX / TXT / MD → text extraction → chunking → Sentence-Transformer embeddings → FAISS semantic search → top-K retrieval → LLM response → cited sources.

## Features

- PDF, DOCX, TXT and Markdown ingestion
- Automatic text extraction
- Configurable chunking and overlap
- Real pretrained `all-MiniLM-L6-v2` embeddings
- FAISS vector search
- Top-K semantic retrieval
- OpenAI LLM integration
- Source-aware responses
- Retrieval-only fallback when no LLM API key is configured
- Chat-style web interface
- REST API
- Persistent FAISS index
- Docker support
- GitHub Actions CI
- Sample project documents

## Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python setup_model.py
```

Copy `.env.example` to `.env` and add your OpenAI API key if you want generated answers:

```text
OPENAI_API_KEY=your_key_here
```

The application still performs real semantic retrieval without an API key and displays the retrieved context rather than pretending an LLM generated it.

Start:

```bash
python app.py
```

Open http://127.0.0.1:5000

## API

`GET /api/health`

`GET /api/stats`

`POST /api/upload` — multipart field `files`

`POST /api/query`:

```json
{"question":"What are the main project risks?"}
```

## Project structure

```text
├── app.py
├── setup_model.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── rag/
│   ├── document_loader.py
│   ├── chunker.py
│   ├── vector_store.py
│   ├── generator.py
│   └── engine.py
├── data/
│   ├── sample_documents/
│   ├── uploads/
│   └── index/
├── templates/
├── static/
└── .github/workflows/ci.yml
```

## Stack

Python, Flask, FAISS, Sentence Transformers, Hugging Face, OpenAI API, PyPDF, python-docx, JavaScript, Docker, GitHub Actions.

## Responsible-use note

The system answers from retrieved document context. Important decisions should always be checked against the original documents.
