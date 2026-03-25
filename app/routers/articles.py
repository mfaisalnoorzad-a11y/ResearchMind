from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ArticleCreate, ArticleResponse, ArticleUpdate
from app.database import get_db
from app.models import Article

router = APIRouter()

@router.post("/articles", status_code=201, response_model=ArticleResponse)
def article_create(article: ArticleCreate, db: Session = Depends(get_db)):
    new_article = Article(url=str(article.url), 
        title=article.title, 
        tags=article.tags, 
        notes=article.notes)
    
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@router.get("/articles", response_model=list[ArticleResponse])
def article_read(skip: int=0, limit: int=20, db: Session = Depends(get_db)):
    return db.query(Article).offset(skip).limit(limit).all()

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
    db.delete(article)
    db.commit()