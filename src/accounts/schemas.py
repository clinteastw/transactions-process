from pydantic import BaseModel


class AccountCreate(BaseModel):
    balance: float
    user_id: int


class AccountUpdate(AccountCreate):
    balance: float
