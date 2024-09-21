from typing import List, Optional

from sqlalchemy import desc, select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.models import Users  

from app.core.models.apartament import Apartment
from app.core.repo.base import BaseRepo


class ApartamentRepo(BaseRepo):

    async def create_apartament(
        self,
        new_apartament: Apartment,
        
    ) -> Optional[Result]:
        try:
            self.session.add(new_apartament)
            await self.session.commit()
            await self.session.refresh(new_apartament)
        except Exception as ex:
            await self.session.rollback()
            raise ex
        

    async def get_apartaments(self) -> Optional[List[Apartment]]:
        try:
            stmt = (
                select(Apartment)
                .options(selectinload(Apartment.apaphotos_photos_rel)) 
                .order_by(desc(Apartment.id))
            )

            result: Result = await self.session.scalars(stmt)

            return result
        except Exception as ex:
            raise ex
        
    async def get_aptament_by_id(self, apartament_id: int) -> Optional[Apartment]:
        try:
            stmt = (
                select(Apartment)
                .where(Apartment.id == apartament_id)
                .options(selectinload(Apartment.apaphotos_photos_rel))
            )

            result: Result = await self.session.execute(stmt)
            apartment = result.scalars().first()  # Получаем первый элемент из результата

            return apartment
        except Exception as ex:
            print(f"Error: {ex}")  # Выводим ошибку, если она есть
            raise ex

    
    async def update_status(self, apartament_id: int):
        try:
            stmt = select(Apartment).where(Apartment.id == apartament_id)
            result = await self.session.execute(stmt)
            apartment = result.scalar()
            if apartment:
                apartment.status = not apartment.status  # Меняем статус на противоположный
                await self.session.commit()
                await self.session.refresh(apartment)
            else:
                raise ValueError("Apartment not found")
        except Exception as ex:
            print(f"Error: {ex}")
            raise ex


    async def update_apartament_id(self, apartament_id: int, data: Apartment):
        try:
            stmt = select(Apartment).where(Apartment.id == apartament_id)
            result = await self.session.execute(stmt)
            apartment = result.scalar()
            if apartment:
                apartment.location = data.location
                apartment.description = data.description
                apartment.rooms = data.rooms
                apartment.price = data.price
                apartment.characteristics = data.characteristics
                await self.session.commit()
                await self.session.refresh(apartment)
            else:
                raise ValueError("Apartment not found")
        except Exception as ex:
            print(f"Error: {ex}")
            raise ex
        

    async def delete_apartament(self, apartament_id: int):
        try:
            stmt = select(Apartment).where(Apartment.id == apartament_id)
            result = await self.session.execute(stmt)
            apartment = result.scalar()
            await self.session.delete(apartment)
            await self.session.commit()
        except Exception as ex:
            print(f"Error: {ex}")
            raise ex