from datetime import datetime
from typing import Any, Optional
from bson import ObjectId
from pydantic import BaseModel, Field, BeforeValidator, PlainSerializer
from typing_extensions import Annotated

def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

PyObjectId = Annotated[
    ObjectId,
    BeforeValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
]

class NewsItemResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    title: str
    category: str
    link: Optional[str] = None
    published_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True