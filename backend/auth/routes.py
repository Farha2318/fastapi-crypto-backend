from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from backend.database.database import SessionLocal
from backend.auth.services import (
    register_user,
    login_user,
    verify_user_otp,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas
class RegisterSchema(BaseModel):
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class OTPSchema(BaseModel):
    email: EmailStr
    otp: str

# Register API
@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    user = register_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {
        "message": "Registered successfully",
        "otp": user.otp  # demo purpose
    }

# Login API
@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = login_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "message": "OTP sent",
        "otp": user.otp
    }

# OTP Verify API
@router.post("/verify-otp")
def verify_otp(data: OTPSchema, db: Session = Depends(get_db)):
    user = verify_user_otp(db, data.email, data.otp)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    token = create_access_token(user.email)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
