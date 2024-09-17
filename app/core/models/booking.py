from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column


from app.core.base import Base

if TYPE_CHECKING:
    from app.core.models import Users, Apartment


class Booking(Base):

    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id')) # Ссылка на пользователя
    apartment_id: Mapped[int] = mapped_column(Integer, ForeignKey('apartments.id')) # Ссылка на квартиру
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    booking_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) # Дата бронирования

    user_rel: Mapped["Users"] = relationship("Users", back_populates="booking_rel")
    apartment_rel: Mapped["Apartment"] = relationship("Apartment", back_populates="booking_rel")
