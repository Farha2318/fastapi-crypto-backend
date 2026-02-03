from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "crypto_db")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
