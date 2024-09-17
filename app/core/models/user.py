from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base import Base

if TYPE_CHECKING:
    from app.core.models import Apartment, Booking


class Users(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(100))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    update_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    apartment_rel: Mapped[List["Apartment"]] = relationship("Apartment", back_populates="user_rel", cascade="all, delete")
    booking_rel: Mapped[List["Booking"]] = relationship("Booking", back_populates="user_rel", cascade="all, delete")


