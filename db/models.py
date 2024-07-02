from datetime import datetime
from sqlalchemy import String, func, Text, Integer, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import mapped_column, relationship, Mapped
from .base import Base


class UserORM(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
