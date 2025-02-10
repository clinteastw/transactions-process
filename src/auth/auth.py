from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

from config import SECRET_KEY
from database import User

from .manager import get_user_manager

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_superuser = fastapi_users.current_user(superuser=True)
current_active_user = fastapi_users.current_user(active=True)
current_user = fastapi_users.current_user()
