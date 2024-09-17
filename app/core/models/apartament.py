from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column


from app.core.base import Base

if TYPE_CHECKING:
    from app.core.models import Users, Status


class Apartment(Base):
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    photos: Mapped[str] = mapped_column(String(1000), nullable=True)  # Список URL фотографий (в виде строки)
    characteristics: Mapped[str] = mapped_column(String(500), nullable=True)  # Доп. характеристики квартиры

    user_rel: Mapped["Users"] = relationship("Users", back_populates="apartment_rel")
    status_rel: Mapped["Status"] = relationship("Status", back_populates="apartment_rel")