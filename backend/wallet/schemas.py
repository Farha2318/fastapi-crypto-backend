from pydantic import BaseModel
from typing import Optional

class WalletCreate(BaseModel):
    currency: str
    wallet_type: str  # CRYPTO or FIAT

class WalletResponse(BaseModel):
    user_id: str
    currency: str
    wallet_type: str
    wallet_address: Optional[str]
    balance: float
    locked_balance: float
    status: str

class AmountRequest(BaseModel):
    amount: float
