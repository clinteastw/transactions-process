"""Insert test data

Revision ID: 1e684a0457ff
Revises: 4f82f99b246c
Create Date: 2025-02-08 18:15:30.735269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from src.models.user import User
from src.users.crud import password_helper
from src.models.account import Account


# revision identifiers, used by Alembic.
revision: str = '1e684a0457ff'
down_revision: Union[str, None] = '4f82f99b246c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
bind = op.get_bind()
session = Session(bind=bind)


def upgrade() -> None:
    test_admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=password_helper.hash("admin"),
        is_superuser=True,
    )
    test_user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password=password_helper.hash("testuser"),
    )
    session.add(test_user)
    session.commit()
    test_user_account = Account(
        balance=0,
        user_id=test_user.id,
    )
    session.add(test_admin)
    session.add(test_user_account)
    session.commit()


def downgrade() -> None:
    test_user_stmt = session.execute(sa.select(User).where(User.email=="testuser@example.com"))
    test_user = test_user_stmt.scalar_one_or_none()
    if test_user:
        test_user_account_stmt = session.execute(sa.select(Account).where(Account.user_id==test_user.id))
        test_user_account = test_user_account_stmt.scalar_one()
        session.delete(test_user_account)
    session.delete(test_user)
    test_admin_stmt = session.execute(sa.select(User).where(User.email=="admin@example.com"))
    test_admin = test_admin_stmt.scalar_one()
    session.delete(test_admin)
