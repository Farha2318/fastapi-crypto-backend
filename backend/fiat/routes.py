from fastapi import APIRouter
from fiat.services import FiatService

router = APIRouter(prefix="/fiat", tags=["Fiat"])


@router.post("/deposit")
async def fiat_deposit(user_id: str, amount: float, method: str):
    return await FiatService.deposit(user_id, amount, method)


@router.post("/withdraw")
async def fiat_withdraw(user_id: str, amount: float, method: str):
    return await FiatService.withdraw(user_id, amount, method)


@router.get("/transactions/{user_id}")
async def get_fiat_transactions(user_id: str):
    return await FiatService.get_user_transactions(user_id)
