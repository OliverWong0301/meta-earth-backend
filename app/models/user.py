from datetime import datetime
from typing import Optional, Literal
from beanie import Document
from pydantic import EmailStr, Field


class User(Document):
    email: EmailStr
    password: str
    full_name: Optional[str] = None          # ← Thêm dòng này
    wallet_address: Optional[str] = None     # ← Đổi thành Optional cho dễ dùng
    mepass_user_id: Optional[str] = None
    status: Literal["active", "suspended"] = "active"
    role: Literal["user", "admin"] = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Settings:
        name = "users"
        indexes = [
            "email",
            "wallet_address",
        ]