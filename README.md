# ResearchMind

ResearchMind is an AI-powered research assistant API for saving articles, extracting their content, generating summaries, running semantic search, and answering questions over your saved research with retrieval-augmented generation (RAG).

It is built as a backend-first portfolio project focused on practical AI engineering: FastAPI, PostgreSQL, SQLAlchemy, Alembic, ChromaDB, and Claude.

## Why This Exists

Many AI tools summarize from prior knowledge instead of the exact source a user gives them. ResearchMind takes a more grounded approach:

- You provide a real article URL
- The app extracts the actual article text
- It stores the source in PostgreSQL
- It indexes the content in ChromaDB for semantic retrieval
- It uses Claude to summarize and answer questions from retrieved context

The goal is not to be a generic chatbot. The goal is to create a research workflow that is source-based, inspectable, and useful for real study or project work.

## Features

- Save articles from URLs
- Extract article content with `trafilatura`
- Generate AI summaries with Claude
- Re-run summarization for saved articles
- Perform semantic search over saved articles
- Ask questions over your research library with RAG
- Find related articles by similarity
- Filter article lists by tag
- Handle duplicate URLs and service failures with clear HTTP errors
- Run with PostgreSQL locally or in Docker
- Manage schema changes with Alembic migrations

## Tech Stack

- `FastAPI` for the API layer
- `PostgreSQL` for relational storage
- `SQLAlchemy` for ORM/database access
- `Alembic` for schema migrations
- `ChromaDB` for vector storage and semantic retrieval
- `Anthropic Claude` for summarization and question answering
- `trafilatura` for article extraction
- `pytest` for API tests
- `Docker` and `docker-compose` for containerized development
- `Railway` for deployment

## Architecture

```mermaid
graph TB
    Client["Client"] --> API["FastAPI API"]
    API --> Articles["Articles Router"]
    API --> Search["Search Router"]
    API --> QA["QA Router"]

    Articles --> Postgres["PostgreSQL"]
    Articles --> Extractor["trafilatura Extractor"]
    Articles --> Claude["Claude API"]
    Articles --> Chroma["ChromaDB"]

    Search --> Chroma
    Search --> Postgres

    QA --> Chroma
    QA --> Postgres
    QA --> Claude
```

## Project Structure

```text
app/
  config.py
  database.py
  main.py
  models.py
  schemas.py
  routers/
    articles.py
    qa.py
    search.py
  services/
    ai_service.py
    extractor.py
    vector_store.py
alembic/
tests/
Dockerfile
docker-compose.yml
requirements.txt
README.md
```

## API Overview

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/articles` | Save a new article, extract content, and generate a summary |
| `GET` | `/articles` | List saved articles with optional pagination and tag filter |
| `GET` | `/articles/{id}` | Get a single article |
| `PATCH` | `/articles/{id}` | Update article tags or notes |
| `DELETE` | `/articles/{id}` | Delete an article |
| `POST` | `/articles/{id}/summarize` | Re-generate the summary for an article |
| `GET` | `/articles/{id}/related` | Find related articles using vector similarity |
| `GET` | `/search?q=...` | Semantic search across saved articles |
| `POST` | `/qa` | Ask a question over saved articles |

## Local Development

### 1. Create and activate a virtual environment

On Linux or WSL:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/researchmind
ANTHROPIC_API_KEY=your-key-here
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

Then open:

- `http://localhost:8000/docs`
- `http://localhost:8000/health`

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

The API will be available at:

- `http://localhost:8000`
- `http://localhost:8000/docs`

Important:

- Migrations do not auto-run when the container starts
- After the first startup, run:

```bash
docker compose exec api alembic upgrade head
```

If you skip that step, requests that depend on the `articles` table will fail because the schema has not been applied yet.

## Testing

Run the test suite from the project root:

```bash
python -m pytest tests/ -v
```

The tests use an isolated SQLite in-memory database and override the FastAPI database dependency.

## Deployment

ResearchMind is deployed on Railway using the included `Dockerfile`.

Deployment notes:

- Railway injects a runtime `PORT`, and the Docker startup command respects it
- Production schema changes are handled through Alembic
- After deploy, run:

```bash
alembic upgrade head
```

- ChromaDB is stored locally at `./chroma_db`
- On Railway, Chroma storage is ephemeral unless a persistent volume is attached

[researchmind](https://researchmind-production-fbdb.up.railway.app/docs)

## Example Requests

Create an article:

```bash
curl -X POST "http://localhost:8000/articles" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "title": "Example Article",
    "tags": "ai,research",
    "notes": "Useful source"
  }'
```

Semantic search:

```bash
curl "http://localhost:8000/search?q=large language models&limit=5"
```

Question answering:

```bash
curl -X POST "http://localhost:8000/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What do my saved articles say about model evaluation?"
  }'
```

## What I Learned

This project was built as a learning-focused backend and AI engineering project. Key areas covered:

- REST API design with FastAPI
- relational modeling with PostgreSQL and SQLAlchemy
- schema migration workflows with Alembic
- content extraction from real web pages
- AI summarization and prompt design with Claude
- semantic retrieval with ChromaDB
- retrieval-augmented generation (RAG)
- automated testing with pytest
- Docker-based local development
- production deployment on Railway

## Notes

- Schema management is Alembic-only
- `Base.metadata.create_all()` is intentionally not used in app startup
- Search, related articles, and QA preserve vector relevance ordering from ChromaDB

## Roadmap

Possible next steps:

- add a polished frontend
- attach persistent storage for Chroma in production
- expand test coverage for search and QA flows
- add authentication and multi-user support
- improve export options for notes and summaries

## License

This project is currently for portfolio and learning use.
