from fastapi import APIRouter, HTTPException, status
from app.models.registration import Registration
from app.models.blacklist_wallet import BlacklistWallet
from app.models.blacklist_email import BlacklistEmail
from app.schemas.registration import RegistrationCreate, RegistrationResponse

router = APIRouter(prefix="/api/v1", tags=["Registration"])


@router.post("/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def create_registration(data: RegistrationCreate):
    # 1. Kiểm tra Blacklist trước
    blacklisted_wallet = await BlacklistWallet.find_one({"wallet_address": data.wallet_address})
    blacklisted_email = await BlacklistEmail.find_one({"email": data.email})

    if blacklisted_wallet or blacklisted_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản của bạn đã bị từ chối trước đó"
        )

    # 2. Kiểm tra đã đăng ký chưa
    existing = await Registration.find_one(
        {"$or": [
            {"email": data.email},
            {"wallet_address": data.wallet_address}
        ]}
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email hoặc ví đã được đăng ký"
        )

    # 3. Tạo registration mới
    registration = Registration(
        email=data.email,
        wallet_address=data.wallet_address,
        meid_image_url=data.meid_image_url,
        status="pending"
    )
    await registration.insert()

    return registration