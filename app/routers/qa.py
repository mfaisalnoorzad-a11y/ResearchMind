from fastapi import APIRouter, Depends, HTTPException
from app.schemas import QARequest, QAResponse
from app.services.vector_store import search
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Article
from app.services.ai_service import client

router = APIRouter()

@router.post("/qa", response_model=QAResponse)
def ask_questions(request: QARequest, db: Session = Depends(get_db)):
    vector_results = search(request.question, 5)
    ids = [int(id) for id in vector_results["ids"][0]]

    articles = db.query(Article).filter(Article.id.in_(ids)).all()

    context = ""
    for article in articles:
        context += f"Title: {article.title}\nContent: {article.content}\n\n"

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system="You are a research assistant. Answer the question using only the provided articles. Cite which articles you used. If the answer is not in the articles, say 'I don't have enough information.'",
            messages=[{"role": "user", "content": f"Articles:\n{context}\nQuestion: {request.question}"}]
        )

        return QAResponse(
            answer=message.content[0].text,
            sources=[{"id": a.id, "title": a.title} for a in articles]
        )

    except Exception:
        raise HTTPException(status_code=503, detail="Could not connect to AI service.")