
import os

from dotenv import load_dotenv

from langchain_cohere import CohereEmbeddings

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24
REFRESH_TOKEN_EXPIRE_DAYS = 30

INDEX_NAME = "chatbot-wrapper-backend"
EMBEDDING_MODEL = CohereEmbeddings(model="embed-english-v3.0")
DIMENSIONS = 1024
CHUNK_SIZE = 400
CHUNK_OVERLAP = 75
SEPARATORS = ["\n\n", "\n", ".", ",", " ", ""]
BASE_K = 20
TOP_N = 5
USE_RERANKING = False
RERANK_MODEL = "ms-marco-MiniLM-L-12-v2"

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"
