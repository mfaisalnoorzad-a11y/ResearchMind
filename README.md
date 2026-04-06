# ResearchMind

A research assistant API that helps save, summarize, and search academic articles using AI.

Built with FastAPI, PostgreSQL, ChromaDB, and Claude AI.

## Motivation

ResearchMind was created to solve a common problem with many AI tools. They can sound helpful, but they sometimes generate summaries from their own background knowledge instead of the actual source, and in some cases they even return links that are inaccurate or not real. ResearchMind takes a more reliable approach by working from real user-provided article URLs, extracting the actual content, generating summaries from that content, and supporting semantic search across saved research. Because of this, it works less like a generic chatbot and more like a trustworthy research workflow based on real sources.

## Features

- Save articles by URL with automatic content extraction
- AI-powered summarization using Claude
- Semantic search across saved articles using vector embeddings
- Full CRUD operations for article management

## Tech Stack

- **FastAPI** -- REST API framework
- **PostgreSQL + SQLAlchemy** -- relational database and ORM
- **ChromaDB + sentence-transformers** -- vector database for semantic search
- **Claude API (Anthropic)** -- AI summarization
- **trafilatura** -- web content extraction

## Status

Work in progress. More features and documentation coming soon.
