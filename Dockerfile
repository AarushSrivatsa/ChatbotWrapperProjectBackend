FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install curl and other dependencies needed for Ollama
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download the embedding model
RUN ollama pull nomic-embed-text:v1.5

# Expose ports
EXPOSE 8080
EXPOSE 11434

# Start Ollama in background and then start FastAPI
CMD ollama serve & sleep 5 && uvicorn main:app --host 0.0.0.0 --port 8080