from __future__ import annotations
from fastapi import APIRouter, Query
from typing import List
from app.models.news import NewsItem
from app.schemas.news import NewsItemResponse

router = APIRouter(prefix="/ticker", tags=["News Ticker"])

@router.get("/news", response_model=List[NewsItemResponse])
async def get_latest_news(limit: int = Query(4, le=10)):
    news_list = await NewsItem.find(
        {"is_active": True}
    ).sort("-published_at").limit(limit).to_list()

    return news_list