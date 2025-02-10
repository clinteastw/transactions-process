from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import current_superuser
from database import get_async_session
from models import User
from users.schemas import UserCreate

from . import crud as crud_user

router = APIRouter(tags=["users"])


@router.post("/create", response_model=None, summary="Admin: Create User")
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_async_session),
    admin: User = Depends(current_superuser)
):
    try:
        new_user = await crud_user.create_user(session, user_in)
        return {"status": f"You succesfully registered new user - {new_user}"}
    except SQLAlchemyError as e:
        return {"status": "An error occured"}
