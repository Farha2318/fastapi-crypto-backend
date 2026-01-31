import string, random
from datetime import datetime
from wallet.database import wallet_collection, transaction_collection

# -------------------------
# Generate crypto wallet address
# -------------------------
def generate_crypto_address(length=34):
    chars = string.ascii_letters + string.digits
    return "CRYPTO_" + "".join(random.choice(chars) for _ in range(length))

# -------------------------
# Create Wallet
# -------------------------
async def create_wallet(user_id: str, currency: str, wallet_type: str):
    wallet_type = wallet_type.upper()
    wallet_address = None
    if wallet_type == "CRYPTO":
        wallet_address = generate_crypto_address()

    wallet = {
        "user_id": user_id,
        "currency": currency.upper(),
        "wallet_type": wallet_type,
        "wallet_address": wallet_address,
        "balance": 0.0,
        "locked_balance": 0.0,
        "status": "ACTIVE",
        "created_at": datetime.utcnow()
    }
    result = await wallet_collection.insert_one(wallet)
    wallet["_id"] = result.inserted_id
    return wallet

# -------------------------
# Get Wallet
# -------------------------
async def get_wallet(user_id: str, currency: str):
    return await wallet_collection.find_one({
        "user_id": user_id,
        "currency": currency.upper()
    })

# Other operations (credit, debit, lock, unlock) remain same
async def credit_wallet(user_id: str, currency: str, amount: float):
    wallet = await get_wallet(user_id, currency)
    if not wallet:
        raise Exception("Wallet not found")

    await wallet_collection.update_one(
        {"_id": wallet["_id"]},
        {"$inc": {"balance": amount}}
    )

    await transaction_collection.insert_one({
        "user_id": user_id,
        "currency": currency.upper(),
        "amount": amount,
        "type": "CREDIT",
        "created_at": datetime.utcnow()
    })

async def debit_wallet(user_id: str, currency: str, amount: float):
    wallet = await get_wallet(user_id, currency)
    if not wallet:
        raise Exception("Wallet not found")
    if wallet["balance"] < amount:
        raise Exception("Insufficient balance")

    await wallet_collection.update_one(
        {"_id": wallet["_id"]},
        {"$inc": {"balance": -amount}}
    )

async def lock_balance(user_id: str, currency: str, amount: float):
    wallet = await get_wallet(user_id, currency)
    if not wallet:
        raise Exception("Wallet not found")
    if wallet["balance"] < amount:
        raise Exception("Insufficient balance to lock")

    await wallet_collection.update_one(
        {"_id": wallet["_id"]},
        {"$inc": {"balance": -amount, "locked_balance": amount}}
    )

async def unlock_balance(user_id: str, currency: str, amount: float):
    wallet = await get_wallet(user_id, currency)
    if not wallet:
        raise Exception("Wallet not found")

    await wallet_collection.update_one(
        {"_id": wallet["_id"]},
        {"$inc": {"balance": amount, "locked_balance": -amount}}
    )
