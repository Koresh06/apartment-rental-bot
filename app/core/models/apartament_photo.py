from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column


from app.core.base import Base

if TYPE_CHECKING:
    from app.core.models import Apartment



class ApartmentPhoto(Base):
    __tablename__ = "apartment_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    apartment_id: Mapped[int] = mapped_column(Integer, ForeignKey('apartments.id'))
    file_path: Mapped[str] = mapped_column(String(255), nullable=False) 

    apartment_rel: Mapped["Apartment"] = relationship("Apartment", back_populates="apaphotos_photos_rel")