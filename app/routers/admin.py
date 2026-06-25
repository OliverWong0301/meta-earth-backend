from fastapi import APIRouter, HTTPException, status, Query, Body
from typing import List, Optional
from datetime import datetime
from app.models.registration import Registration
from app.models.user import User
from app.schemas.registration import RegistrationAdminView
from app.core.security import hash_password, generate_temp_password

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.get("/registrations/pending", response_model=List[RegistrationAdminView])
async def get_pending_registrations(limit: int = Query(50, le=200)):
    registrations = await Registration.find(
        {"status": "pending"}
    ).sort("-submitted_at").limit(limit).to_list()
    return registrations


@router.get("/registrations/{registration_id}", response_model=RegistrationAdminView)
async def get_registration_detail(registration_id: str):
    registration = await Registration.get(registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn đăng ký")
    return registration


@router.post("/registrations/{registration_id}/grant", status_code=status.HTTP_200_OK)
async def grant_registration(registration_id: str):
    """Admin duyệt đơn đăng ký"""
    registration = await Registration.get(registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn đăng ký")

    if registration.status != "pending":
        raise HTTPException(status_code=400, detail="Đơn này đã được xử lý")

    # Tạo password ngẫu nhiên
    temp_password = generate_temp_password()

    # Hash password trước khi lưu
    hashed_password = hash_password(temp_password)

    # Cập nhật trạng thái registration
    registration.status = "granted"
    registration.processed_at = datetime.utcnow()
    await registration.save()

    # Tạo User account với password đã hash
    user = User(
        email=registration.email,
        password=hashed_password,
        wallet_address=registration.wallet_address,
        status="active",
        role="user"
    )
    await user.insert()

    return {
        "message": "Đã duyệt thành công",
        "registration_id": str(registration.id),
        "user_id": str(user.id),
        "temp_password": temp_password,          # Admin có thể gửi cho user
        "note": "Hãy gửi mật khẩu tạm này cho người dùng và yêu cầu đổi mật khẩu sau khi đăng nhập"
    }


@router.post("/registrations/{registration_id}/decline", status_code=status.HTTP_200_OK)
async def decline_registration(
    registration_id: str,
    reason: Optional[str] = Body(None, embed=True)
):
    """Admin từ chối đơn đăng ký"""
    registration = await Registration.get(registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn đăng ký")

    if registration.status != "pending":
        raise HTTPException(status_code=400, detail="Đơn này đã được xử lý")

    registration.status = "declined"
    registration.processed_at = datetime.utcnow()
    registration.decline_reason = reason
    await registration.save()

    return {
        "message": "Đã từ chối đơn đăng ký",
        "registration_id": str(registration.id)
    }


@router.get("/users")
async def get_all_users(limit: int = Query(50, le=200)):
    """Admin xem danh sách User (dùng để test)"""
    users = await User.find_all().limit(limit).to_list()
    return users