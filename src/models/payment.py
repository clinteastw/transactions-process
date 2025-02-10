import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class Payment(Base):
    __tablename__ = "payments"
    
    transaction_id: Mapped[str] = mapped_column(unique=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    amount: Mapped[float]
    time: Mapped[datetime.datetime] = mapped_column(default=func.now())