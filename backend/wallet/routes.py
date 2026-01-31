from fastapi import APIRouter, HTTPException, Depends
from wallet import services, schemas
# from wallet.temp_auth_stub import get_current_user 
from auth.dependencies import get_current_user


router = APIRouter(prefix="/wallet", tags=["Wallet Management"])

# -------------------------
# Create Wallet (Crypto / Fiat)
# -------------------------
@router.post("/create", response_model=schemas.WalletResponse)
async def create_wallet(data: schemas.WalletCreate, user: dict = Depends(get_current_user)):
    wallet = await services.create_wallet(
        user_id=user["user_id"],
        currency=data.currency,
        wallet_type=data.wallet_type
    )
    return wallet

# -------------------------
# Get Wallet Details
# -------------------------
@router.get("/{currency}", response_model=schemas.WalletResponse)
async def get_wallet(currency: str, user: dict = Depends(get_current_user)):
    wallet = await services.get_wallet(user["user_id"], currency)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    wallet["_id"] = str(wallet["_id"])
    return wallet

# -------------------------
# Credit Wallet
# -------------------------
@router.post("/credit/{currency}")
async def credit_wallet(currency: str, data: schemas.AmountRequest, user: dict = Depends(get_current_user)):
    try:
        await services.credit_wallet(user["user_id"], currency, data.amount)
        return {"message": "Wallet credited successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------------
# Debit Wallet
# -------------------------
@router.post("/debit/{currency}")
async def debit_wallet(currency: str, data: schemas.AmountRequest, user: dict = Depends(get_current_user)):
    try:
        await services.debit_wallet(user["user_id"], currency, data.amount)
        return {"message": "Wallet debited successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------------
# Lock Wallet Balance
# -------------------------
@router.post("/lock/{currency}")
async def lock_wallet(currency: str, data: schemas.AmountRequest, user: dict = Depends(get_current_user)):
    try:
        await services.lock_balance(user["user_id"], currency, data.amount)
        return {"message": "Amount locked successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------------
# Unlock Wallet Balance
# -------------------------
@router.post("/unlock/{currency}")
async def unlock_wallet(currency: str, data: schemas.AmountRequest, user: dict = Depends(get_current_user)):
    try:
        await services.unlock_balance(user["user_id"], currency, data.amount)
        return {"message": "Amount unlocked successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
