from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from models.payment import Payment
from models.user import User

from .schemas import PaymentCreate


async def get_payment_by_transaction_id(session: AsyncSession, transaction_id: str):
    stmt = await session.execute(select(Payment).where(Payment.transaction_id == transaction_id))
    payment = stmt.scalar_one_or_none()
    return payment


async def create_payment(session: AsyncSession, payment_in: PaymentCreate):
    payment = Payment(**payment_in.model_dump(exclude="signature"))
    session.add(payment)
    await session.commit()
    print(payment)
    return payment


async def get_payments_by_user_id(session: AsyncSession, user_id: int):
    stmt = await session.execute(select(Payment).where(Payment.user_id == user_id))
    payments = stmt.scalars().all()
    if not payments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": f"No payments for user {user_id}"},
        )
    return payments