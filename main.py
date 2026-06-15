from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.database import client

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kết nối MongoDB khi server khởi động
    print("✅ Kết nối MongoDB thành công")
    yield
    # Ngắt kết nối khi server tắt
    client.close()
    print("🛑 Đã ngắt kết nối MongoDB")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Backend Meta Earth VN đang chạy"}