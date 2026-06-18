from fastapi import APIRouter, HTTPException
from app.models.mec_price import MECPrice
from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/price", tags=["MEC Price"])

class MECPriceUpdate(BaseModel):
    price: float = Field(..., gt=0, description="Giá phải lớn hơn 0")

@router.get("/mec")
async def get_mec_price():
    latest = await MECPrice.find_one(sort=[("updated_at", -1)])
    if not latest:
        raise HTTPException(status_code=404, detail="Chưa có giá MEC")

    # Tính change 24h
    twenty_four_hours_ago = datetime.now(timezone.utc) - timedelta(hours=24)

    old_price_doc = await MECPrice.find_one(
        MECPrice.updated_at <= twenty_four_hours_ago,
        sort=[("updated_at", -1)]
    )

    if old_price_doc and old_price_doc.price > 0:
        change24h = ((latest.price - old_price_doc.price) / old_price_doc.price) * 100
    else:
        change24h = 0.0

    return {
        "price": latest.price,
        "change24h": round(change24h, 2),
        "updated_at": latest.updated_at
    }

@router.post("/mec")
async def update_mec_price(data: MECPriceUpdate):
    new_price = MECPrice(price=data.price, updated_at=datetime.now(timezone.utc))
    await new_price.insert()
    return {"message": "Cập nhật giá thành công", "price": data.price}