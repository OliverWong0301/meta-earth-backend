from fastapi import APIRouter, HTTPException, status, Depends, Body
from pydantic import BaseModel
from app.models.user import User
from app.core.security import verify_password, create_access_token, get_current_user, hash_password
from beanie import PydanticObjectId

router = APIRouter(prefix="/api/v1", tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: str


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    user = await User.find_one({"email": data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng"
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng"
        )

    # Tạo JWT token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role
    }
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "email": user.email,
        "role": user.role
    }

@router.post("/change-password")
async def change_password(
    current_password: str = Body(..., embed=True),
    new_password: str = Body(..., embed=True),
    current_user=Depends(get_current_user)
):
    """User đổi mật khẩu sau khi đăng nhập"""
    # Dùng find_one thay vì .get() để an toàn hơn với string ID
    user = await User.find_one({"_id": current_user["user_id"]})
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")

    # Kiểm tra mật khẩu cũ
    if not verify_password(current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu hiện tại không đúng"
        )

    # Cập nhật mật khẩu mới
    user.password = hash_password(new_password)
    await user.save()

    return {"message": "Đổi mật khẩu thành công"}