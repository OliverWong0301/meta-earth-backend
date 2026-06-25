from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId


class RegistrationCreate(BaseModel):
    email: EmailStr
    wallet_address: str
    meid_image_url: str


class RegistrationResponse(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    email: EmailStr
    wallet_address: str
    status: Literal["pending", "granted", "declined"]
    submitted_at: datetime

    class Config:
        populate_by_name = True
        from_attributes = True


class RegistrationAdminView(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    email: EmailStr
    wallet_address: str
    meid_image_url: str
    status: Literal["pending", "granted", "declined"]
    submitted_at: datetime
    processed_at: Optional[datetime] = None
    decline_reason: Optional[str] = None

    class Config:
        populate_by_name = True
        from_attributes = True