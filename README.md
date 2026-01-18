# PageIndex RAG + NotebookLM-style Frontend

This project demonstrates a complete Retrieval-Augmented Generation (RAG) system using **PageIndex** (Vectorless RAG) for the backend and a modern **Next.js** application for the frontend, styled like NotebookLM.

It features a full-stack architecture with:
- **Backend**: Python (FastAPI), SQLModel (SQLite), PageIndex SDK, and MCP Server support.
- **Frontend**: Next.js, TailwindCSS, Shadcn/UI.
- **RAG**: "Vectorless" retrieval using PageIndex's simulation of human reading patterns.
- **MCP**: Model Context Protocol support (SSE endpoint) for exposing RAG tools to AI assistants.

## 🚀 Features

- **Document Management**: Upload PDF documents to build a knowledge base.
- **Chat Interface**: Interactive chat with your documents using PageIndex's reasoning engine.
- **Source Transparency**: See which documents are available and select them for context.
- **MCP Server**: Exposes `query_knowledge_base` and `list_available_documents` as MCP tools.
- **Authentication**: Secure user registration and login (JWT).

## 🛠 Prerequisites

- **Python 3.12+** (Managed by `uv` recommended)
- **Node.js 18+**
- **PageIndex API Key**: Get one at [pageindex.ai](https://pageindex.ai)
- **Gemini API Key** (or other LLM key supported by PageIndex, if applicable)

## 📦 Installation

### 1. Backend Setup

The backend is built with **FastAPI** and managed by **uv**.

```bash
cd backend

# Initialize and install dependencies
uv sync

# Configure Environment Variables
cp .env.example .env
# Open .env and add your PAGEINDEX_API_KEY
```

**Run the Backend:**

```bash
./start.sh
# OR manually:
# uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend runs on `http://localhost:8000`.
- **API Docs**: `http://localhost:8000/docs`
- **MCP SSE Endpoint**: `http://localhost:8000/mcp/sse`

### 2. Frontend Setup

The frontend is a **Next.js** app.

```bash
cd frontend

# Install dependencies
npm install

# Run Development Server
npm run dev
```

The frontend runs on `http://localhost:3000`.

## 📖 Usage

1. **Register/Login**: Create an account on the frontend.
2. **Upload**: Use the "Add Source" button to upload PDF documents.
3. **Chat**: Select one or more uploaded documents from the sidebar and start asking questions.

## 🏗 Architecture

- **`backend/`**:
  - `app/api.py`: REST endpoints.
  - `app/rag.py`: PageIndex integration logic.
  - `app/mcp_server.py`: MCP tool definitions.
  - `app/db.py`: SQLite database models.
- **`frontend/`**:
  - `app/dashboard`: Main chat interface.
  - `components/`: UI components (ChatInterface, FileUploader).
  - `lib/api.ts`: API client.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
