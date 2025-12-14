# Chatbot Wrapper Backend

FastAPI backend for a multi-user chatbot application with authentication, persistent chat storage, and optional conversation-scoped retrieval during response generation.

---

## Overview

This project provides a backend API that manages users, conversations, and messages, while supporting optional retrieval-augmented generation (RAG) per conversation. Relational data is stored in PostgreSQL, and vectorized context is stored separately in a vector database.

The system is functional end-to-end and is currently being refactored for better internal organization.

---

## Core Features

* FastAPI backend
* JWT authentication using HTTP Bearer tokens
* Protected routes scoped per user
* Persistent storage for:

  * Users
  * Conversations
  * Messages
* REST API for conversation and message management

---

## RAG Pipeline

The backend includes an optional retrieval pipeline that can be used during message generation.

* Conversation-scoped vector storage
* Text chunking with configurable size and overlap
* Embeddings generated using `nomic-embed-text`
* Similarity-based retrieval with configurable top-K
* Optional reranking stage for improved relevance
* Retrieved context injected into response generation

This pipeline is modular and can be enabled, disabled, or adjusted without affecting core chat functionality.

---

## Tech Stack

* **Backend:** FastAPI
* **Authentication:** JWT + HTTP Bearer
* **ORM:** SQLAlchemy
* **Database:** PostgreSQL (Supabase)
* **LLM Provider:** Groq
* **Vector Database:** Pinecone
* **Frameworks / Tooling:** LangChain, Tavily

---

## Project Structure

```text
ChatbotWrapperProject/
├── AI/                      # AI and retrieval logic
├── database/                # SQLAlchemy models and DB operations
├── routers/                 # FastAPI routes
├── schemas.py               # Pydantic schemas
├── config.py                # App configuration
├── main.py                  # FastAPI entry point
└── requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<db>
GROQ_API_KEY=your-groq-api-key
PINECONE_API_KEY=your-pinecone-api-key
TAVILY_API_KEY=your-tavily-api-key
```

---

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload
```

* API base URL: `http://localhost:8000`
* Swagger docs: `http://localhost:8000/docs`

---

## API Routes

### Users

* `POST /users/register`
* `POST /users/login`

### Conversations

* `GET /conversations/`
* `POST /conversations/`
* `POST /conversations/{conversation_id}/add-document`
* `DELETE /conversations/{conversation_id}`

### Messages

* `GET /convo/{conversation_id}/messages/`
* `POST /convo/{conversation_id}/messages/`

All routes (except register/login) require a valid JWT.

---

## Status

* Core functionality complete
* Refactor and cleanup in progress
