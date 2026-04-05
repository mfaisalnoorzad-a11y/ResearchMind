from fastapi import FastAPI
from app.database import Base, engine
from app.models import Article
from app.routers import articles, search, qa



app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(articles.router)
app.include_router(search.router)
app.include_router(qa.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}