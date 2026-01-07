# 🚀 Chatbot Wrapper Project Backend

Production FastAPI backend with **full async I/O**, advanced RAG pipeline, and quad-mode web intelligence. Built for multi-user scale.

**Live API:** https://chatbotwrapperprojectbackend.onrender.com  
**Swagger Docs:** https://chatbotwrapperprojectbackend.onrender.com/docs

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
- JWT with dual tokens (access + refresh)
- Secure password hashing
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
- Cohere Embed English v3.0 generates 1024-dim embeddings
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
Generate embeddings (Cohere, 1024-dim)
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

### 🌐 Quad Web Intelligence (Tavily)

🔍 **Search** - Real-time queries, AI-ranked results for LLMs

📄 **Extract** - Pull clean content from URLs, strip the garbage

🕷️ **Crawl** - Navigate sites with natural language ("find all pricing pages")

🗺️ **Map** - Discover entire site structures, visualize URL hierarchies

System picks the right mode automatically.

---

## 🛠️ Stack

| Component | Tech |
|-----------|------|
| 🚀 Backend | FastAPI (Fully Async) |
| 🔑 Auth | JWT (Access + Refresh) |
| 💾 Database | PostgreSQL (Supabase) |
| ⚙️ ORM | Async SQLAlchemy |
| 🔍 Vectors | Pinecone |
| 🤖 LLM | Groq (swap in one line) |
| 🧮 Embeddings | Cohere Embed English v3.0 |
| 🎯 Reranker | FlashRank (ms-marco-MiniLM-L-12-v2) |
| ✂️ Chunking | RecursiveCharacterTextSplitter |
| 🌐 Web | Tavily |
| 🔗 Orchestration | LangChain |

---

## 📡 API Routes

### 💻 Swagger UI
<img width="1707" height="841" alt="image" src="https://github.com/user-attachments/assets/957201cd-4a56-4d31-9452-57ce6887ad88" />
# 🚀 Chatbot Wrapper Project Backend

Production FastAPI backend with **full async I/O**, advanced RAG pipeline, and quad-mode web intelligence. Built for multi-user scale.

**Live API:** https://chatbotwrapperprojectbackend.onrender.com  
**Swagger Docs:** https://chatbotwrapperprojectbackend.onrender.com/docs

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
- JWT with dual tokens (access + refresh)
- Secure password hashing
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
**What it does:** Real-time web search optimized specifically for AI applications. Unlike Google or Bing which return raw links, Tavily Search analyzes 20+ sources simultaneously and extracts the most relevant content using AI ranking.

**How it works:**
- Searches across multiple sources in parallel
- AI filters out ads, navigation, and irrelevant content  
- Returns clean, structured snippets with citations
- Optimized for LLM context windows (no bloat)

**When to use:**
- *"What's the latest news about X?"*
- *"Current stock price of Y"*
- *"Industry trends in Z sector"*
- *"Best practices for [topic]"*

**Example:**
```python
response = tavily_client.search("latest AI developments 2025")
# Returns: Ranked, clean excerpts from news sites, blogs, papers
```

---

### 📄 **Extract** - Clean Content from Specific URLs
**What it does:** Pulls raw content from URLs you specify (up to 20 at once) and strips away all the garbage—ads, popups, navigation bars, cookie banners, footers.

**How it works:**
- Accepts single URL or list of URLs
- Two modes: `basic` (fast) or `advanced` (includes tables, embedded content)
- Automatically cleans HTML → returns markdown or plain text
- Preserves structure and meaning

**When to use:**
- *"Extract content from this specific article"*  
- *"Get the main text from these 5 research papers"*
- *"Pull product specs from competitor URLs"*
- You already know which URLs you need

**Example:**
```python
urls = [
    "https://arxiv.org/paper123",
    "https://competitor.com/pricing",
    "https://blog.com/analysis"
]
response = tavily_client.extract(urls=urls, extract_depth="advanced")
# Returns: Clean markdown content from each URL
```

---

### 🕷️ **Crawl** - Navigate Sites with Natural Language Goals
**What it does:** Smart website exploration that uses natural language instructions to find deeply buried information. It's like having an AI that can browse a site for you.

**How it works:**
- Starts from a base URL
- Intelligently follows links using breadth-first search
- Uses your natural language goal to filter what's relevant
- Can go multiple levels deep (`max_depth`)
- Respects robots.txt, handles dynamic content

**When to use:**
- *"Find all documentation pages about API authentication"*
- *"Get pricing information from competitor sites"*
- *"Extract all blog posts about [topic]"*
- You need specific info but don't know exact URLs

**Example:**
```python
response = tavily_client.crawl(
    url="https://docs.example.com",
    max_depth=3,
    limit=50,
    instructions="Find all pages explaining authentication methods"
)
# Returns: Only pages matching your goal, with content extracted
```

---

### 🗺️ **Map** - Discover Entire Website Structures
**What it does:** Creates a complete map of a website's structure—every internal link, organized hierarchically. Think of it as generating a sitemap on demand.

**How it works:**
- Starts from a base URL
- Traverses the site like a graph in parallel
- Discovers all internal pages
- Returns just the URLs (no content extraction)
- Can filter by path patterns (e.g., only `/docs/*`)

**When to use:**
- *"Show me the entire structure of competitor.com"*
- *"List all pages under their /products/ section"*  
- *"Plan an extraction job before crawling"*
- You need to see what exists before diving in

**Example:**
```python
response = tavily_client.map(
    url="https://competitor.com",
    max_depth=3,
    instructions="Map the entire product section"
)
# Returns: List of all discovered URLs
# ["https://competitor.com/products/item1", 
#  "https://competitor.com/products/item2", ...]
```

---

### 🎯 How They Work Together

**Scenario:** User asks *"How does Company X's pricing compare to industry standards?"*

1. **Search** → finds current industry pricing articles  
2. **Extract** → pulls clean content from Company X's pricing page
3. **Crawl** → navigates competitor sites to find hidden pricing tiers
4. **Map** → discovers all pricing-related pages across competitor domains

**Result:** One comprehensive answer with data from RAG docs + all four web modes, fully cited.

---

## 🛠️ Stack

| Component | Tech |
|-----------|------|
| 🚀 Backend | FastAPI (Fully Async) |
| 🔑 Auth | JWT (Access + Refresh) |
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

## 📡 API Routes

### 💻 Swagger UI
https://chatbotwrapperprojectbackend.onrender.com/docs

### 👤 Users
- `POST /users/register` - Sign up  
- `POST /users/login` - Get access + refresh tokens  
- `POST /users/refresh` - Refresh both tokens  
- `POST /users/logout` - Kill tokens

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

- Passwords hashed with industry standards
- JWT tokens expire  
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
