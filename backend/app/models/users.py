from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import List, Optional
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, unique=True, nullable=False
    )
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=datetime.now)

    family: Mapped["Family"] = relationship(
        "Family", back_populates="members", overlaps="owned_family,owner"
    )
    owned_family: Mapped["Family"] = relationship(
        "Family", back_populates="owner", overlaps="family"
    )
    info: Mapped["UserInfo"] = relationship("UserInfo", back_populates="user")


class UserInfo(Base):
    __tablename__ = "user_info"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="info")


class Family(Base):
    __tablename__ = "families"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship(
        "User", back_populates="owned_family", overlaps="family"
    )
    members: Mapped[List["User"]] = relationship(
        "User", back_populates="family", overlaps="owned_family,owner"
    )
