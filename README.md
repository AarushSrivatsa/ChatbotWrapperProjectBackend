# 🚀 Chatbot Wrapper Project Backend

Production FastAPI backend with **full async I/O**, advanced RAG pipeline, and quad-mode web intelligence. Built for multi-user scale.

**Live API:** https://chatbotwrapperprojectbackend.onrender.com  
**Swagger Docs:** https://chatbotwrapperprojectbackend.onrender.com/docs

---

## 🛠️ Stack

| Component | Tech |
|-----------|------|
| 🚀 Backend | FastAPI (Fully Async) |
| 🔑 Auth | JWT (Access + Refresh) + Email OTP |
| 📧 Email | SMTP |
| 💾 Database | PostgreSQL (Supabase) |
| ⚙️ ORM | Async SQLAlchemy |
| 🔍 Vectors | Pinecone |
| 🤖 LLM | Groq (swap in one line) |
| 🧮 Embeddings | Ollama Nomic Embed Text v1.5 (768-dim) |
| 🎯 Reranker | FlashRank (ms-marco-MiniLM-L-12-v2) |
| ✂️ Chunking | RecursiveCharacterTextSplitter |
| 🌐 Web | Tavily (Search, Extract, Crawl, Map) |
| 🔗 Orchestration | LangChain |

---

## 💡 What This Actually Does

Most chatbot backends give you RAG **or** web search. This gives you **both**, with four different ways to pull information from the web—all in one conversation.

**Real scenario:** User uploads their Q3 financial report and asks *"How does our revenue growth compare to industry trends, and what's our competitor's product structure?"*

The system:
- Extracts revenue data from the uploaded PDF (RAG)
- Searches the web for current industry benchmarks  
- Crawls analyst sites for specific insights
- Maps the competitor's entire website structure
- Returns one coherent answer with all sources cited

Document memory + web intelligence working together. Not separately—**together**.

---

## ⚡ Why It's Fast

**Everything is async:**
- FastAPI async endpoints
- Async SQLAlchemy with PostgreSQL  
- Non-blocking database operations
- Concurrent request handling

When User A uploads a document, User B doesn't wait. When User C runs a web search, Users D and E keep chatting. No blocking, no waiting.

**Provider-agnostic LLM:**
- Currently running Groq for speed
- Want OpenAI? Anthropic? One line of code
- LangChain handles the abstraction  
- Never locked into a vendor

---

## 🏗️ Core Features

### 🔐 Authentication
- **Email verification with OTP** for secure signup
- JWT with dual tokens (access + refresh)
- Secure password hashing
- Password reset with OTP verification
- Token invalidation on logout
- **Every user completely isolated**

### 💬 Conversations  
- Multi-user support
- Create, list, delete conversations
- Each conversation has its own RAG config
- Persistent message history
- **Each conversation gets its own vector namespace in Pinecone**

### 🧠 RAG Pipeline

Upload PDF, DOCX, TXT—anything. System handles:

**Processing:**
- RecursiveCharacterTextSplitter breaks documents intelligently
- 400-char chunks with 75-char overlap
- Custom separators preserve semantic boundaries

**Storage:**
- **Ollama Nomic Embed Text v1.5** generates 768-dim embeddings
- Pinecone stores vectors in conversation-scoped namespaces
- User A's docs never touch User B's docs

**Retrieval:**
- Query finds top 20 similar chunks (BASE_K=20)
- Optional FlashRank reranking with ms-marco-MiniLM-L-12-v2 → best 5 (TOP_N=5)  
- Context injected into LLM prompt

```
Document Upload (User A, Conversation 1)
↓
Text Extraction
↓
Split into chunks (400 chars, 75 overlap)
↓
Generate embeddings (Ollama Nomic Embed v1.5, 768-dim)
↓
Store in Pinecone (namespace: user_A_conv_1)
↓
User A asks question
↓
Search vectors (only in user_A_conv_1)
↓
Get top 20 chunks
↓
Rerank to best 5 (optional)
↓
Feed to LLM with context
↓
Answer
```

**User B uploads to Conversation 2?** Goes to `user_B_conv_2` namespace. Zero data leakage.

---

## 🌐 Quad Web Intelligence (Tavily)

The system automatically picks the right web tool for your question. All four modes work together to find the best information.

### 🔍 **Search** - Find Information Across the Web
Real-time web search optimized for AI applications. Analyzes 20+ sources simultaneously, filters out ads and irrelevant content, returns clean structured snippets with citations. Perfect for latest news, stock prices, industry trends, and best practices.

### 📄 **Extract** - Clean Content from Specific URLs
Pulls raw content from URLs (up to 20 at once) and strips away ads, popups, navigation bars, cookie banners. Two modes: basic (fast) or advanced (includes tables, embedded content). Use when you already know which URLs you need.

### 🕷️ **Crawl** - Navigate Sites with Natural Language Goals
Smart website exploration using natural language instructions. Starts from a base URL, intelligently follows links using breadth-first search, filters content based on your goal. Can go multiple levels deep. Use when you need specific info but don't know exact URLs.

### 🗺️ **Map** - Discover Entire Website Structures
Creates complete map of a website's structure—every internal link, organized hierarchically. Traverses sites in parallel, discovers all internal pages, returns just the URLs. Can filter by path patterns. Use to see what exists before diving in.

---

### 🎯 How They Work Together

**Scenario:** User asks *"How does Company X's pricing compare to industry standards?"*

1. **Search** → finds current industry pricing articles  
2. **Extract** → pulls clean content from Company X's pricing page
3. **Crawl** → navigates competitor sites to find hidden pricing tiers
4. **Map** → discovers all pricing-related pages across competitor domains

**Result:** One comprehensive answer with data from RAG docs + all four web modes, fully cited.

---

## 📡 API Routes

### 💻 Swagger UI
https://chatbotwrapperprojectbackend.onrender.com/docs

### 🔐 Authentication
- `POST /auth/signup/send-otp` - Send OTP to email for signup
- `POST /auth/signup/verify-otp/{email}` - Verify OTP and create account
- `POST /auth/login` - Get access + refresh tokens  
- `POST /auth/refresh` - Refresh both tokens  
- `POST /auth/reset-password/send-otp` - Send OTP for password reset
- `POST /auth/reset-password/{email}` - Reset password with OTP

### 💬 Conversations (Auth Required)
- `GET /conversations/` - List all conversations  
- `POST /conversations/` - Create new conversation  
- `DELETE /conversations/{conversation_id}` - Delete conversation

### 📨 Messages (Auth Required)
- `GET /conversations/{conversation_id}/messages/` - Get message history  
- `POST /conversations/{conversation_id}/messages/` - Send message  
- `POST /conversations/{conversation_id}/messages/document` - Upload document

**Auth:** Protected routes need `Bearer <token>` in Authorization header

**Try it live:** https://chatbotwrapperprojectbackend.onrender.com/docs

---

## 🔒 Security

- Email verification with OTP before account creation
- Passwords hashed with industry standards
- JWT tokens expire  
- Password reset via secure OTP flow
- Database-level user isolation
- Pydantic validates all inputs
- SQLAlchemy prevents injection

---

## 🎯 The Architecture

**User Isolation:** Every user's data completely separate. Conversations scoped to users. Documents scoped to conversations. No cross-contamination.

**RAG + Web Search:** Not one or the other—both. Documents provide context, web search provides current info. Combined intelligently.

**Flexibility:** Swap LLM providers in one line. Toggle reranking on/off. Configure chunk sizes. Change retrieval parameters. Built to adapt.

**Speed:** Async everything. Non-blocking I/O. Concurrent requests. Multiple users hitting the API simultaneously? No problem.

---

## 🙏 Built With

- **FastAPI** - Async web framework
- **LangChain** - RAG orchestration + LLM abstraction  
- **Groq** - Fast inference
- **Ollama** - Local embeddings (Nomic Embed Text v1.5)
- **Pinecone** - Vector storage
- **Tavily** - Web intelligence (Search, Extract, Crawl, Map)
- **FlashRank** - Ultra-fast reranking (ms-marco-MiniLM-L-12-v2 model)

---

**Modern async Python with production-grade architecture.**
