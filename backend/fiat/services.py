from datetime import datetime
from database.mongo import db

fiat_collection = db.fiat_transactions


class FiatService:

    @staticmethod
    async def deposit(user_id: str, amount: float, method: str):
        transaction = {
            "user_id": user_id,
            "amount": amount,
            "method": method,
            "type": "deposit",
            "status": "pending",
            "created_at": datetime.utcnow()
        }

        result = await fiat_collection.insert_one(transaction)
        transaction["_id"] = str(result.inserted_id)
        return transaction

    @staticmethod
    async def withdraw(user_id: str, amount: float, method: str):
        transaction = {
            "user_id": user_id,
            "amount": amount,
            "method": method,
            "type": "withdraw",
            "status": "pending",
            "created_at": datetime.utcnow()
        }

        result = await fiat_collection.insert_one(transaction)
        transaction["_id"] = str(result.inserted_id)
        return transaction

    @staticmethod
    async def get_user_transactions(user_id: str):
        transactions = []
        cursor = fiat_collection.find({"user_id": user_id})

        async for tx in cursor:
            tx["_id"] = str(tx["_id"])
            transactions.append(tx)

        return transactions
