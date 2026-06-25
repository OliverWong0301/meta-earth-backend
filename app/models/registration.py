from datetime import datetime
from typing import Optional, Literal
from beanie import Document
from pydantic import EmailStr, Field


class Registration(Document):
    email: EmailStr
    wallet_address: str
    meid_image_url: str
    status: Literal["pending", "granted", "declined"] = "pending"
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None
    processed_by: Optional[str] = None          # admin user id (sau này)
    decline_reason: Optional[str] = None

    class Settings:
        name = "registrations"
        indexes = [
            "email",
            "wallet_address",
            "status",
        ]