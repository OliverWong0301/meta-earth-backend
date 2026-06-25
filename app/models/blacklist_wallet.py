from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field


class BlacklistWallet(Document):
    wallet_address: str
    reason: Optional[str] = None
    added_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "blacklist_wallets"
        indexes = [
            "wallet_address",
        ]