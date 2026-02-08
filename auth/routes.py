from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr

from backend.auth.services import (
    register_user,
    login_user,
    verify_user_otp,
    create_access_token
)

# 👇 IDHU THAAN NEE KETTA IMPORT (INGA PODANUM)
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class OTPSchema(BaseModel):
    email: EmailStr
    otp: str


@router.post("/register")
async def register(data: RegisterSchema):
    user = await register_user(data.email, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return {
        "message": "Registered successfully",
        "otp": user["otp"]
    }


@router.post("/login")
async def login(data: LoginSchema):
    user = await login_user(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "OTP sent",
        "otp": user["otp"]
    }


@router.post("/verify-otp")
async def verify_otp(data: OTPSchema):
    user = await verify_user_otp(data.email, data.otp)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    token = create_access_token(user["email"])
    return {
        "access_token": token,
        "token_type": "bearer"
    }


# 🔐 PROTECTED API (IDHU VACHITHAAN Authorize VARUM)
@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return {
        "email": current_user["sub"],
        "message": "You are authenticated"
    }
