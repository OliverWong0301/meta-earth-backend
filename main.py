from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.database import client, database
from app.routers.news import router as news_router
from app.routers.mec_price import router as mec_price_router
from beanie import init_beanie
from app.models.news import NewsItem
from app.models.mec_price import MECPrice

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo Beanie + kết nối MongoDB
    await init_beanie(
        database=database,
        document_models=[NewsItem, MECPrice]
    )
    print("✅ Kết nối MongoDB và khởi tạo Beanie thành công")
    yield
    await client.close()
    print("🛑 Đã ngắt kết nối MongoDB")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(news_router)
app.include_router(mec_price_router)

@app.get("/")
async def root():
    return {"message": "Backend Meta Earth VN đang chạy"}