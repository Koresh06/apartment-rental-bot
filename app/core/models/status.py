from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column


from app.core.base import Base

if TYPE_CHECKING:
    from app.core.models import Apartment


class Status(Base):

    __tablename__ = "status"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    apartment_id: Mapped[int] = mapped_column(Integer, ForeignKey('apartments.id'))
    status: Mapped[str] = mapped_column(String(50), default=False)  # Статусы: "свободна" - False, "занята" - True
    change_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # Дата изменения статуса

    apartment_rel: Mapped["Apartment"] = relationship("Apartment", back_populates="status_rel")