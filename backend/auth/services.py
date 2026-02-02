from backend.database.database import db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import random
from jose import jwt, JWTError

# ================= CONFIG =================
SECRET_KEY = "supersecretkey"   # later .env la move pannalam
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ================= HELPERS =================
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def generate_otp():
    return str(random.randint(100000, 999999))

def create_access_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": email,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# ================= SERVICES =================
async def register_user(email: str, password: str):
    existing_user = await db.users.find_one({"email": email})
    if existing_user:
        return None

    otp = generate_otp()

    user = {
        "email": email,
        "password": hash_password(password),
        "otp": otp,
        "is_verified": False
    }

    await db.users.insert_one(user)
    return user


async def login_user(email: str, password: str):
    user = await db.users.find_one({"email": email})
    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    otp = generate_otp()

    await db.users.update_one(
        {"email": email},
        {"$set": {"otp": otp}}
    )

    user["otp"] = otp
    return user


async def verify_user_otp(email: str, otp: str):
    user = await db.users.find_one({"email": email})
    if not user:
        return None

    if user.get("otp") != otp:
        return None

    await db.users.update_one(
        {"email": email},
        {"$set": {"is_verified": True, "otp": None}}
    )

    return user


SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None