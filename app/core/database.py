from pymongo import AsyncMongoClient
from app.core.config import get_settings

settings = get_settings()

# Kết nối MongoDB bằng PyMongo Async (khuyến nghị với Beanie 2.x)
client = AsyncMongoClient(settings.MONGO_URI)
database = client[settings.DATABASE_NAME]