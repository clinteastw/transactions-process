from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from accounts import crud as crud_account
from auth.auth import current_superuser, current_user
from database import get_async_session
from models.user import User
from payments.utils import (check_signature, generate_random_transaction_id,
                            generate_signature)

from . import crud as crud_payment
from .schemas import PaymentCreate, SignatureCreate

router = APIRouter(tags=["payments"])


@router.post("/generate-random-transaction-id")
def get_random_transaction_id():
    random_id = generate_random_transaction_id()
    return {"random transaction_id": random_id}


@router.post("/generate-signature")
def get_signature(data: SignatureCreate):
    print(data)
    return generate_signature(data.model_dump(exclude="signature"))


@router.post("/process")
async def create_payment(
    payment_in: PaymentCreate,
    session: AsyncSession = Depends(get_async_session)
):
    payment_details = payment_in.model_dump()
    check_signature(payment_details)
    payment = await crud_payment.get_payment_by_transaction_id(session, payment_in.transaction_id)

    if payment:
        return {"status": "This payment already been processed"}

    account = await crud_account.get_or_create_account(session=session, payment_details=payment_details)
    await crud_payment.create_payment(session=session, payment_in=payment_in)
    account.balance += payment_details["amount"]
    await session.commit()

    return {"status": "success"}


@router.get("/me", summary="Current User: Get User Payments")
async def get_my_payments(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await crud_payment.get_payments_by_user_id(session=session, user_id=user.id)


@router.get("/user/{user_id}", summary="Admin: Get Any User Payments")
async def get_payments_admin(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    admin: User = Depends(current_superuser),
):
    return await crud_payment.get_payments_by_user_id(session=session, user_id=user_id)