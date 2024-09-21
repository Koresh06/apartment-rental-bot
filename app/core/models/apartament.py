from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import ARRAY, Boolean, Column, Integer, String, ForeignKey, Date, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column


from app.core.base import Base

if TYPE_CHECKING:
    from app.core.models import Booking, ApartmentPhoto


class Apartment(Base):

    __tablename__ = "apartments"
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    rooms: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    characteristics: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)

    booking_rel: Mapped[List["Booking"]] = relationship("Booking", back_populates="apartment_rel", cascade="all, delete")
    apaphotos_photos_rel: Mapped[List["ApartmentPhoto"]] = relationship("ApartmentPhoto", back_populates="apartment_rel", cascade="all, delete")