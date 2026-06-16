from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class NewsItemCreate(BaseModel):
    title: str
    category: str
    link: Optional[str] = None

class NewsItemResponse(BaseModel):
    id: str
    title: str
    category: str
    link: Optional[str] = None
    published_at: datetime

    class Config:
        from_attributes = True