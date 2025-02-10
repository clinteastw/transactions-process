from fastapi_users.password import PasswordHelper
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from users.schemas import UserCreate

password_helper = PasswordHelper()


async def create_user(session: AsyncSession, user_in: UserCreate):
    user_data = user_in.model_dump()
    hashed_password = password_helper.hash(user_data["password"])
    new_user = User(
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=hashed_password,
    )
    session.add(new_user)
    await session.commit()
    return new_user.email
