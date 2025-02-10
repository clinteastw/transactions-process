from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.account import Account
from models.user import User

from .schemas import AccountCreate


async def create_account(session: AsyncSession, account_in: AccountCreate):
    account = Account(**account_in.model_dump())
    session.add(account)
    await session.commit()
    return account


async def get_accounts(session: AsyncSession, user_id: int):
    stmt = (select(User).where(User.id == user_id))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"info": f"User {user_id} not found"},
        )
    return user.accounts


async def get_or_create_account(session: AsyncSession, payment_details: dict):
    stmt = (
        select(Account)
        .where(
            and_(Account.id == payment_details["account_id"],
                 Account.user_id == payment_details["user_id"])
        )
    )
    result = await session.execute(stmt)
    account = result.scalar_one_or_none()

    if not account:
        user_stmt = select(User).where(User.id == payment_details["user_id"])
        user_result = await session.execute(user_stmt)
        user = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": f"User {payment_details.user_id} not found"},
        )
        account = Account(
            id=payment_details["account_id"], user_id=payment_details["user_id"], balance=0)
        session.add(account)
        await session.commit()

    return account
