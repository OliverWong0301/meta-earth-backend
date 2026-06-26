import asyncio
from app.core.security import hash_password
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

async def create_admin():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DATABASE_NAME", "meta_earth_db")

    if not mongo_uri:
        print("❌ Không tìm thấy MONGO_URI trong .env")
        return

    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]

    admin_email = "admin@metaearth.vn"
    admin_password = "Admin123!"
    dummy_wallet = "admin_wallet_for_testing_001"

    existing = await db["users"].find_one({"email": admin_email})
    if existing:
        print("⚠️ Admin đã tồn tại!")
        return

    admin_doc = {
        "email": admin_email,
        "password": hash_password(admin_password),
        "wallet_address": dummy_wallet,
        "role": "admin",
        "status": "active",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "mepass_user_id": None,
        "last_login": None
    }

    result = await db["users"].insert_one(admin_doc)
    print("✅ Đã tạo Admin thành công!")
    print(f"Email: {admin_email}")
    print(f"Password: {admin_password}")
    print(f"ID: {result.inserted_id}")

asyncio.run(create_admin())