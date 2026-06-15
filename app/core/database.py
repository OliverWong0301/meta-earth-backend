from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings = get_settings()

# Kết nối MongoDB
client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DATABASE_NAME]

# Các collection chính (sẽ dùng sau)
fund_collection = database.get_collection("fund")
users_collection = database.get_collection("users")