from fastapi import APIRouter, HTTPException
from app.models.mec_price import MECPrice
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter(prefix="/price", tags=["MEC Price"])

class MECPriceUpdate(BaseModel):
    price: float

@router.get("/mec")
async def get_mec_price():
    price_doc = await MECPrice.find_one(sort=[("updated_at", -1)])
    if not price_doc:
        raise HTTPException(status_code=404, detail="Chưa có giá MEC")
    return {"price": price_doc.price, "updated_at": price_doc.updated_at}

@router.post("/mec")
async def update_mec_price(data: MECPriceUpdate):
    new_price = MECPrice(price=data.price, updated_at=datetime.now(timezone.utc))
    await new_price.insert()
    return {"message": "Cập nhật giá thành công", "price": data.price}