from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import EmailStr, Field


class BlacklistEmail(Document):
    email: EmailStr
    reason: Optional[str] = None
    added_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "blacklist_emails"
        indexes = [
            "email",
        ]