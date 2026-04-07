# ResearchMind

A research assistant API that helps save, summarize, and search academic articles using AI.

Built with FastAPI, PostgreSQL, ChromaDB, and Claude AI.

## Motivation

ResearchMind was created to solve a common problem with many AI tools. They can sound helpful, but they sometimes generate summaries from their own background knowledge instead of the actual source, and in some cases they even return links that are inaccurate or not real. ResearchMind takes a more reliable approach by working from real user-provided article URLs, extracting the actual content, generating summaries from that content, and supporting semantic search across saved research. Because of this, it works less like a generic chatbot and more like a trustworthy research workflow based on real sources.

## Features

- Save articles by URL with automatic content extraction
- AI-powered summarization using Claude
- Semantic search across saved articles using vector embeddings
- RAG-based Q&A with source citations across your research library
- Re-trigger summarization on any saved article
- Full CRUD operations with error handling and input validation

## Tech Stack

- **FastAPI** -- REST API framework with automatic OpenAPI docs
- **PostgreSQL + SQLAlchemy** -- relational database and ORM
- **ChromaDB + sentence-transformers** -- vector database for semantic search
- **Claude API (Anthropic)** -- AI summarization and RAG Q&A
- **trafilatura** -- web content extraction

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/articles` | Save a new article (auto-extracts content and generates summary) |
| GET | `/articles` | List all saved articles (with pagination) |
| GET | `/articles/{id}` | Get a single article by ID |
| PATCH | `/articles/{id}` | Update an article's tags or notes |
| DELETE | `/articles/{id}` | Delete an article |
| POST | `/articles/{id}/summarize` | Re-generate the AI summary for an article |
| GET | `/search?q=query` | Semantic search across saved articles |
| POST | `/qa` | Ask a question and get an AI-generated answer with source citations |

## Setup

1. Clone the repo and create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/researchmind
   ANTHROPIC_API_KEY=your-key-here
   ```

4. Start PostgreSQL and create the database:
   ```
   sudo service postgresql start
   sudo -u postgres psql -c "CREATE DATABASE researchmind;"
   ```

5. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

6. Open `http://localhost:8000/docs` to explore the API.

## Status

Core features complete. Currently adding related articles, testing, Docker, and deployment.
