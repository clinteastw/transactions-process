from pydantic import BaseModel


class PaymentRead(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: float
    signature: str


class PaymentCreate(PaymentRead):
    pass


class SignatureCreate(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: float
