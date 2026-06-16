from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from beanie import Document
from pydantic import Field

class NewsItem(Document):
    title: str
    category: str
    link: Optional[str] = None
    published_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

    class Settings:
        name = "news_items"


