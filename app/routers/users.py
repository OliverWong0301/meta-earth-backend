from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


# Response model
class UserProfile(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    wallet_address: Optional[str] = None
    status: str


# Update request model
class UpdateProfile(BaseModel):
    full_name: Optional[str] = None
    wallet_address: Optional[str] = None


@router.get("/me", response_model=UserProfile)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Lấy thông tin profile của user đang đăng nhập"""
    return UserProfile(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        wallet_address=current_user.wallet_address,
        status=current_user.status
    )


@router.put("/me", response_model=UserProfile)
async def update_my_profile(
    update_data: UpdateProfile,
    current_user: User = Depends(get_current_user)
):
    """Cập nhật profile của user đang đăng nhập"""
    updated = False

    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name
        updated = True

    if update_data.wallet_address is not None:
        current_user.wallet_address = update_data.wallet_address
        updated = True

    if updated:
        current_user.updated_at = __import__("datetime").datetime.utcnow()
        await current_user.save()

    return UserProfile(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        wallet_address=current_user.wallet_address,
        status=current_user.status
    )