from fastapi import FastAPI
from app.database import Base, engine
from app.models import Article


app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}