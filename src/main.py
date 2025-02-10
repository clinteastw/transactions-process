import uvicorn
from fastapi import FastAPI

from accounts.router import router as account_router
from auth.auth import auth_backend, fastapi_users
from payments.router import router as payment_router
from users.router import router as user_router
from users.schemas import UserCreate, UserRead, UserUpdate

app = FastAPI(
    title="Transactions App"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    account_router,
    prefix="/accounts",
)

app.include_router(
    payment_router,
    prefix="/payments",
)

app.include_router(
    user_router,
    prefix="/users",
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
