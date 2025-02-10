from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Account(Base):
    __tablename__ = "accounts"
    
    balance: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    user: Mapped["User"] = relationship(back_populates="accounts", foreign_keys=[user_id], cascade="all, delete")