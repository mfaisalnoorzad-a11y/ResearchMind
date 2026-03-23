from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional
from datetime import datetime

class ArticleCreate(BaseModel):
    url: HttpUrl
    title: str
    tags: Optional[str] = None
    notes: Optional[str] = None

class ArticleUpdate(BaseModel):
    tags: Optional[str] = None
    notes: Optional[str] = None

class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: HttpUrl
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime