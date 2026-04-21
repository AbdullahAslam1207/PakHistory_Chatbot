# Pak History Chatbot

A Flask + LangChain chatbot focused on Pakistan history and news. It supports:
- Document-grounded Q&A using local `.txt`, `.pdf`, and `.docx` files
- Internet fallback via Google Custom Search when context is insufficient
- A tool-based agent (`LangGraph ReAct`) that routes queries across retrieval, web search, and email logic

## Project Analysis (What This App Does)

The app is a backend-first chatbot with a simple web UI:

1. You upload document file paths through `POST /document`.
2. The server reads and merges document content.
3. Content is chunked and embedded with OpenAI embeddings.
4. A FAISS retriever is created and stored globally.
5. `POST /query` sends questions to an agent that can use tools:
   - `retrieval_qa_chain` for Pakistan history/context questions
   - `google_search` for news or fallback if retrieval returns "I don't know"
   - `send_email` for restricted topics (Army/Special Forces workflow)

Main stack:
- Python + Flask (`application.py`)
- LangChain + LangGraph agents
- OpenAI (`gpt-4o-mini`, `text-embedding-3-small`)
- FAISS vector store
- PyMuPDF + python-docx for document processing

## Current Project Structure

- `application.py`: Flask app, routes (`/`, `/document`, `/query`)
- `utils/documentprocessor.py`: loads and parses txt/pdf/docx
- `utils/embeddings.py`: chunking + embeddings + FAISS retriever creation
- `utils/chain.py`: retrieval chain for document Q&A
- `utils/agent.py`: LangGraph ReAct agent setup
- `tools/context.py`: tool wrapper for retrieval chain
- `tools/internet.py`: Google Custom Search + OpenAI summarization tool
- `tools/mail.py`: email tool for restricted topics
- `prompts/prompt.py`: system prompts
- `templates/index.html`: web chat UI

## Requirements

- Python 3.10+ (recommended 3.11)
- OpenAI API key
- Google Custom Search credentials (for internet tool)

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_custom_search_api_key
CX=your_google_custom_search_engine_id
```

Notes:
- `OPENAI_API_KEY` is required for both chat and embeddings.
- `GOOGLE_API_KEY` and `CX` are needed for the internet/news tool.

## Setup (Windows PowerShell)

```powershell
# from project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Project

```powershell
python application.py
```

Then open:
- `http://127.0.0.1:5000/`

## How to Use

1. Process documents first (required before queries):

```bash
curl -X POST http://127.0.0.1:5000/document \
  -H "Content-Type: application/json" \
  -d '{"document_url":["C:/path/file1.txt","C:/path/file2.pdf","C:/path/file3.docx"]}'
```

2. Ask a question:

```bash
curl -X POST http://127.0.0.1:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What happened in 1857 in Pakistan?"}'
```

## API Endpoints

- `GET /`
  - Serves chat UI from `templates/index.html`

- `POST /document`
  - Body: `{ "document_url": ["path1", "path2"] }`
  - Supports: `.pdf`, `.txt`, `.docx`
  - Initializes retriever + agent

- `POST /query`
  - Body: `{ "query": "your question" }`
  - Returns chatbot response
  - Requires `/document` to be called first

## Troubleshooting

- `No retriever available. Please process documents first.`
  - Call `POST /document` before `POST /query`.

- OpenAI/auth errors
  - Verify `OPENAI_API_KEY` in `.env`.

- Internet tool not working
  - Verify `GOOGLE_API_KEY` and `CX`.

- File parsing issues
  - Ensure file paths exist and extensions are `.txt`, `.pdf`, or `.docx`.

## Important Security Notes

- The current `tools/mail.py` contains hardcoded email credentials. Move credentials to `.env` before production use.
- The internet tool currently disables SSL verification (`verify=False`) for Google requests. Enable SSL verification for production.
- The app runs with `debug=True` in `application.py`; disable debug mode in production.

## Quick Improvement Ideas

- Add `.env.example` for safer onboarding
- Add input validation for document paths
- Add unit/integration tests
- Persist FAISS index to disk for faster restarts
- Replace global state (`retriever`, `agent`) with app-safe storage
