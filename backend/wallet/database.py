import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["fintech_db"]

wallet_collection = db["wallets"]
transaction_collection = db["wallet_transactions"]
