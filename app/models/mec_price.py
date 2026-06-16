from datetime import datetime, timezone
from beanie import Document
from pydantic import Field

class MECPrice(Document):
    price: float
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "mec_price"