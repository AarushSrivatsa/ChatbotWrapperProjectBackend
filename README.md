# Chatbot Wrapper Backend

A production-ready FastAPI backend for a multi-user conversational AI application with advanced retrieval-augmented generation (RAG), web search capabilities, and intelligent document processing.

---

## 🌟 Overview

This project provides a comprehensive backend API that manages users, conversations, and messages while supporting conversation-scoped retrieval-augmented generation with optional reranking and web search integration. Built with modern Python tools and best practices, it offers a modular, scalable foundation for AI-powered chat applications.

**Key Differentiator:** Unlike typical chatbot backends that focus on either RAG or web search, this system seamlessly integrates both capabilities, allowing conversations to leverage uploaded documents AND real-time web information simultaneously.

---

## ✨ Core Features

### Authentication & User Management
- **JWT-based authentication** with HTTP Bearer tokens
- Secure user registration and login
- Password hashing with industry-standard algorithms
- User-scoped data isolation

### Conversation Management
- **Multi-user support** with isolated conversation spaces
- Create, list, and delete conversations
- Conversation-level RAG configuration
- Persistent message history

### Advanced RAG Pipeline
- **Universal document support** - Upload any document type (PDF, DOCX, TXT, etc.)
- **Recursive character text splitting** with custom separators for optimal chunk boundaries
- **Local embeddings** via Ollama (nomic-embed-text:v1.5) - no external API calls
- **Optional ms-marco-MiniLM-L-12-v2 reranker** for enhanced retrieval precision
- Configurable chunk size (400 chars) and overlap (75 chars)
- Similarity-based retrieval with BASE_K=20, refined to TOP_N=5
- Conversation-scoped vector storage in Pinecone

### Web Intelligence
- **Tavily integration** for real-time web search
- Website crawling and content extraction
- Search result processing and synthesis
- Seamless integration with conversation context

### Message System
- Text message support
- Document upload and processing
- Message history retrieval

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Backend Framework** | FastAPI | High-performance async API |
| **Authentication** | JWT | Secure token-based auth |
| **ORM** | SQLAlchemy | Database abstraction layer |
| **Database** | PostgreSQL (Supabase) | Relational data storage |
| **Vector Database** | Pinecone | Semantic search & embeddings |
| **LLM Provider** | Groq | Ultra-fast inference |
| **Embeddings** | Ollama (nomic-embed-text:v1.5) | Local semantic embeddings |
| **Reranker** | ms-marco-MiniLM-L-12-v2 | Optional precision reranking |
| **Text Splitting** | RecursiveCharacterTextSplitter | Intelligent document chunking |
| **Web Search** | Tavily | Real-time web crawling & search |
| **Orchestration** | LangChain | RAG pipeline framework |

---

## 📁 Project Structure

```text
ChatbotWrapperProject/
├── AI/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── bot.py
│   ├── rag.py
│   └── tools.py
│
├── database/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── conversations.py
│   ├── initializations.py
│   ├── messages.py
│   └── user.py
│
├── routers/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── auth.py
│   ├── conversation.py
│   ├── messages.py
│   └── user.py
│
├── .venv/
├── .env
├── .gitignore
├── config.py
├── main.py
├── README.md
├── requirements.txt
└── schemas.py
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL database (or Supabase account)
- Pinecone account
- Groq API key
- Tavily API key
- Ollama installed locally (for embeddings)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ChatbotWrapperProject
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
GROQ_API_KEY=your-groq-api-key
PINECONE_API_KEY=your-pinecone-api-key
TAVILY_API_KEY=your-tavily-api-key
```

5. **Configure application settings**

Edit `config.py` for additional configuration:

```python
# JWT Token Settings
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# AI Settings
INDEX_NAME = "chatbot-wrapper-project"
EMBEDDING_MODEL = OllamaEmbeddings(model="nomic-embed-text:v1.5")
CHUNK_SIZE = 400
CHUNK_OVERLAP = 75
SEPARATORS = ["\n\n", "\n", ".", ",", " ", ""]
BASE_K = 20
TOP_N = 5
USE_RERANKING = False
RERANK_MODEL = "ms-marco-MiniLM-L-12-v2"
```

6. **Install Ollama and pull the embedding model**
```bash
# Install Ollama (visit https://ollama.ai for your OS)
# Then pull the embedding model
ollama pull nomic-embed-text:v1.5
```

7. **Run the application**
```bash
uvicorn main:app --reload
```

The API will be available at:
- **Base URL:** `http://localhost:8000`
- **Interactive docs:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 📡 API Routes

### Users
- `POST /users/register` - Register new user
- `POST /users/login` - Login and get JWT token

### Conversations (Protected)
- `GET /conversations/` - List all conversations for authenticated user
- `POST /conversations/` - Create new conversation
- `DELETE /conversations/{conversation_id}` - Delete conversation

### Messages (Protected)
- `GET /conversations/{conversation_id}/messages/` - Get all messages in conversation
- `POST /conversations/{conversation_id}/messages/` - Send message and get AI response
- `POST /conversations/{conversation_id}/messages/document` - Upload document to conversation

All protected routes require authentication via Bearer token in the Authorization header.

---

## 🧠 RAG Pipeline Architecture

```
Document Upload
    ↓
Text Extraction
    ↓
Recursive Character Splitting (400 chars, 75 overlap)
    ↓
Embedding Generation (Ollama nomic-embed-text:v1.5)
    ↓
Vector Storage (Pinecone)
    ↓
User Query → Vector Similarity Search
    ↓
Top-K Retrieval (BASE_K=20)
    ↓
Optional Reranking (ms-marco-MiniLM-L-12-v2, TOP_N=5)
    ↓
Context Injection → LLM Generation (Groq)
```

### RAG Components

#### 1. Document Chunking
**RecursiveCharacterTextSplitter** ensures intelligent splitting:
- Preserves semantic boundaries
- Chunk size: **400 characters**
- Overlap: **75 characters**
- Custom separators: `["\n\n", "\n", ".", ",", " ", ""]`
- Recursive splitting maintains document structure

#### 2. Embedding Generation
**Ollama nomic-embed-text:v1.5** provides:
- **Local embedding generation** (no external API calls)
- High-quality semantic embeddings
- Fast inference with GPU acceleration (if available)
- Privacy-preserving (data never leaves your infrastructure)
- Cost-effective for high-volume applications

#### 3. Vector Storage
**Pinecone** features:
- Conversation-scoped namespaces
- Index name: `chatbot-wrapper-project`
- Fast similarity search
- Metadata filtering
- Scalable to millions of vectors

#### 4. Retrieval & Reranking
**Two-stage retrieval (optional):**
1. **Broad retrieval:** BASE_K=**20** candidates from vector search
2. **Precision reranking:** Optional reranking with **ms-marco-MiniLM-L-12-v2** to TOP_N=**5** most relevant chunks

**Reranking toggle:**
- Set `USE_RERANKING=True` in `config.py` to enable the reranking stage
- When disabled, the system returns the top 5 results directly from vector search
- Reranking improves precision but adds latency

**ms-marco-MiniLM-L-12-v2 advantages:**
- Cross-encoder architecture for accurate relevance scoring
- Trained on MS MARCO dataset for passage ranking
- Lightweight model suitable for real-time applications
- Significantly improves precision over vector search alone

#### 5. Context Injection
Retrieved context is injected into the system prompt before sending to Groq LLM for generation.

---

## 🌐 Web Search Integration

### Tavily Features

- **Real-time search:** Query the web for current information
- **Content extraction:** Clean, formatted content from web pages
- **Source tracking:** Maintain citation information
- **Result synthesis:** Combine multiple sources intelligently

### Use Cases

1. **Current Events:** Questions requiring up-to-date information
2. **Fact Checking:** Verify information against web sources
3. **Supplemental Context:** Enhance RAG responses with web data
4. **Research Queries:** Gather information from multiple sources

---

## ⚙️ Configuration

### Environment Variables (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `GROQ_API_KEY` | ✅ | Groq API key for LLM |
| `PINECONE_API_KEY` | ✅ | Pinecone API key |
| `TAVILY_API_KEY` | ✅ | Tavily API key |

### Application Settings (config.py)

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | - | JWT secret key |
| `ALGORITHM` | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_HOURS` | 24 | Token expiration (hours) |
| `INDEX_NAME` | chatbot-wrapper-project | Pinecone index name |
| `CHUNK_SIZE` | 400 | Text chunk size |
| `CHUNK_OVERLAP` | 75 | Chunk overlap |
| `BASE_K` | 20 | Initial retrieval count |
| `TOP_N` | 5 | Final result count |
| `USE_RERANKING` | False | Enable reranking |
| `RERANK_MODEL` | ms-marco-MiniLM-L-12-v2 | Reranker model |

---

## 🔒 Security

- **Password Hashing:** All passwords hashed using secure algorithms
- **JWT Tokens:** 24-hour token expiration
- **User Isolation:** Strict database-level access controls
- **Input Validation:** Pydantic schemas validate all inputs
- **SQL Injection Protection:** SQLAlchemy ORM prevents injection attacks

---

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **LangChain** for RAG orchestration tools
- **Groq** for lightning-fast inference
- **Ollama** for local embedding generation
- **Pinecone** for vector database infrastructure
- **Tavily** for web search capabilities
- **ms-marco-MiniLM-L-12-v2** for optional reranking

---

**Built with modern Python tools and best practices.**
