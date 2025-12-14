from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_core.documents import Document
from uuid import uuid4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_compressors import FlashrankRerank
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.tools import tool
FlashrankRerank.model_rebuild()

load_dotenv()

pc = Pinecone()

# Global settings
INDEX_NAME = "chatbot-wrapper-project"
EMBEDDING_MODEL = OllamaEmbeddings(model="nomic-embed-text:v1.5")
CHUNK_SIZE = 400
CHUNK_OVERLAP = 75
SEPARATORS = ["\n\n", "\n", ".", ",", " ", ""]
BASE_K = 20
TOP_N = 5
USE_RERANKING = True
RERANK_MODEL = "ms-marco-MiniLM-L-12-v2"

# Ensure index exists
if not pc.has_index(INDEX_NAME):
    pc.create_index(
        name=INDEX_NAME,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
index = pc.Index(INDEX_NAME)


def add_to_rag(conversation_id: int, text: str) -> str:
    """Insert text into vector database for a specific conversation."""
    namespace = str(conversation_id)
    
    vector_store = PineconeVectorStore(
        index=index,
        embedding=EMBEDDING_MODEL,
        namespace=namespace
    )
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS
    ) 
    
    doc = [Document(page_content=text)]
    documents = splitter.split_documents(doc)
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=uuids)
    
    return f"Insertion Successful: {len(documents)} chunks created"

def make_query_rag_tool(conversation_id: int):

    def _rag_runtime(query: str) -> str:
        """Actual RAG logic. Pydantic never inspects this."""

        namespace = str(conversation_id)

        vector_store = PineconeVectorStore(
            index=index,
            embedding=EMBEDDING_MODEL,
            namespace=namespace
        )

        base_retriever = vector_store.as_retriever(
            search_kwargs={"k": BASE_K}
        )

        if USE_RERANKING:
            retriever = ContextualCompressionRetriever(
                base_retriever=base_retriever,
                base_compressor=FlashrankRerank(
                    model=RERANK_MODEL,
                    top_n=TOP_N
                )
            )
        else:
            retriever = base_retriever

        doc_results = retriever.invoke(query)

        formatted_docs = []
        for i, doc in enumerate(doc_results, 1):
            formatted_docs.append(
                f"---DOCUMENT {i}---\n{doc.page_content}\n---END OF DOCUMENT {i}---"
            )

        return "\n\n".join(formatted_docs) or "No relevant information found."

    @tool
    def query_rag(query: str) -> str:
        """Retrieve relevant documents for a query from a specific conversation."""
        return _rag_runtime(query)

    return query_rag


def clear_rag(conversation_id: int) -> str:
    """Delete all documents for a specific conversation."""
    namespace = str(conversation_id)
    index.delete(namespace=namespace, delete_all=True)
    return f"RAG memory of conversation {conversation_id} was successfully wiped out"