from fastapi import APIRouter, HTTPException
from app.models.mec_price import MECPrice
from pydantic import BaseModel, Field
from datetime import datetime, timezone

router = APIRouter(prefix="/price", tags=["MEC Price"])

class MECPriceUpdate(BaseModel):
    price: float = Field(..., gt=0, description="Giá phải lớn hơn 0")

@router.get("/mec")
async def get_mec_price():
    # Lấy giá mới nhất
    latest = await MECPrice.find_one(sort=[("updated_at", -1)])
    if not latest:
        raise HTTPException(status_code=404, detail="Chưa có giá MEC")

    # Lấy giá cập nhật trước đó (second latest)
    previous = await MECPrice.find_one(
        MECPrice.updated_at < latest.updated_at,
        sort=[("updated_at", -1)]
    )

    if previous and previous.price > 0:
        change = ((latest.price - previous.price) / previous.price) * 100
    else:
        change = 0.0

    return {
        "price": latest.price,
        "change": round(change, 2),           # ← field mới
        "updated_at": latest.updated_at
    }

@router.post("/mec")
async def update_mec_price(data: MECPriceUpdate):
    new_price = MECPrice(price=data.price, updated_at=datetime.now(timezone.utc))
    await new_price.insert()
    return {"message": "Cập nhật giá thành công", "price": data.price}