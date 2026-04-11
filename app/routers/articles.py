from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from app.schemas import ArticleCreate, ArticleResponse, ArticleUpdate, ArticleListResponse
from app.database import get_db
from app.models import Article
from app.services.extractor import extract_content
from app.services.ai_service import summarize
from app.services.vector_store import add_article, remove_article, search

router = APIRouter()

@router.post("/articles", status_code=201, response_model=ArticleResponse)
def article_create(article: ArticleCreate, db: Session = Depends(get_db)):
    new_article = Article(url=str(article.url), 
        title=article.title, 
        tags=article.tags, 
        notes=article.notes)
    
    try:
        content = extract_content(str(article.url))
        
        if content:
            new_article.content = content
            new_article.summary = summarize(content) 
    except Exception:
        pass # article saves without content/summary

    db.add(new_article)
    try:
        db.commit()
        db.refresh(new_article)

        if new_article.content:
            add_article(str(new_article.id), new_article.content)

        return new_article
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, 
            detail="Resource already exists or violates database constraints."
        )

@router.get("/articles", response_model=ArticleListResponse)
def article_read(skip: int=0, limit: int=20, tag: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Article)
    if tag:
        query = query.filter(Article.tags.contains(tag))
    
    articles = query.offset(skip).limit(limit).all()
    return ArticleListResponse(count=len(articles), articles=articles)

@router.post("/articles/{id}/summarize", response_model=ArticleResponse)
def article_sum(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    content = extract_content(str(article.url))

    if content:
        article.summary = summarize(content)
    
    db.commit()
    db.refresh(article)
    return article

@router.get("/articles/{id}", response_model=ArticleResponse)
def article_id(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.patch("/articles/{id}", response_model=ArticleResponse)
def article_update(id: int, article_update: ArticleUpdate, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if article_update.tags is not None:
        article.tags = article_update.tags
    
    if article_update.notes is not None:
        article.notes = article_update.notes
    
    db.commit()
    db.refresh(article)
    return article

@router.delete("/articles/{id}", status_code=204)
def article_delete(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    remove_article(str(article.id))
    db.delete(article)
    db.commit()

@router.get("/articles/{id}/related", response_model=list[ArticleResponse])
def search_related_articles(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if not article.content:
        return []

    results = search(article.content, 6)
    ids = [int(i) for i in results["ids"][0]]
    ids = [i for i in ids if i != id]  # filter out the current article
    if not ids:
        return []

    articles = db.query(Article).filter(Article.id.in_(ids)).all()
    articles_by_id = {article.id: article for article in articles}
    return [articles_by_id[article_id] for article_id in ids if article_id in articles_by_id]
