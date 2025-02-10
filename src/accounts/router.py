from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from accounts import crud
from accounts.schemas import AccountCreate
from auth.auth import current_superuser, current_user
from database import get_async_session
from models.user import User

router = APIRouter(tags=["accounts"])


@router.post("/create", response_model=None)
async def create_account(
    account_in: AccountCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await crud.create_account(session=session, account_in=account_in)


@router.get("/me", summary="Current User: Get User Accounts")
async def get_my_accounts(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    accounts = await crud.get_accounts(session=session, user_id=user.id)
    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"info": f"You have no accounts"},
        )
    return accounts


@router.get("/user/{user_id}", summary="Admin: Get Any User Accounts")
async def get_accounts_admin(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    admin: User = Depends(current_superuser),
):
    accounts = await crud.get_accounts(session=session, user_id=user_id)
    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"info": f"No accounts for user {user_id}"},
        )
    return accounts
