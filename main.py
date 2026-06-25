from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.database import client, database
from app.routers.news import router as news_router
from app.routers.mec_price import router as mec_price_router
from beanie import init_beanie
# === Models cho Phase 1 ===
from app.models.registration import Registration
from app.models.user import User
from app.models.blacklist_wallet import BlacklistWallet
from app.models.blacklist_email import BlacklistEmail
from app.routers.admin import router as admin_router
from app.routers.auth import router as auth_router

# === Models cũ ===
from app.models.news import NewsItem
from app.models.mec_price import MECPrice
from fastapi.middleware.cors import CORSMiddleware

from app.routers.registration import router as registration_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo Beanie + kết nối MongoDB
    await init_beanie(
    database=database,
    document_models=[
        NewsItem,
        MECPrice,
        # Phase 1 models
        Registration,
        User,
        BlacklistWallet,
        BlacklistEmail,
    ]
)
    print("✅ Kết nối MongoDB và khởi tạo Beanie thành công")
    yield
    await client.close()
    print("🛑 Đã ngắt kết nối MongoDB")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://meta-earth-vietnam.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router)
app.include_router(mec_price_router)
# ... các include_router khác
app.include_router(registration_router)
app.include_router(admin_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Backend Meta Earth VN đang chạy"}