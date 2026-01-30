from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from jose import jwt
from datetime import datetime, timedelta
import random

from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

# password hashing
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

# OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# JWT
def create_access_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

from sqlalchemy.exc import IntegrityError

def register_user(db, email, password):
    user = User(
        email=email,
        hashed_password=hash_password(password),
        otp=generate_otp()
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        return None

# Login
def login_user(db, email, password):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    user.otp = generate_otp()
    db.commit()
    return user

# OTP Verify
def verify_user_otp(db, email, otp):
    user = db.query(User).filter(User.email == email).first()
    if user and user.otp == otp:
        user.is_verified = True
        user.otp = None
        db.commit()
        return user
    return None
