from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Article
from app.schemas import ArticleResponse
from app.database import get_db
from app.services.vector_store import search

router = APIRouter()

@router.get("/search", response_model=list[ArticleResponse])
def searching(q: str, limit: int=5, db: Session = Depends(get_db)):
    vector_results = search(q, limit)
    ids = [int(id) for id in vector_results["ids"][0]]

    article = db.query(Article).filter(Article.id.in_(ids)).all()
    return article
    