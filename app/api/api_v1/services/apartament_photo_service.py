from pathlib import Path
from typing import Optional

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.api_v1.save_path_photo import remove_photos
from app.core.models import Users  

from app.core.models.apartament import Apartment
from app.core.models.apartament_photo import ApartmentPhoto
from app.core.repo.base import BaseRepo


class ApartamentPhotoRepo(BaseRepo):

    async def add_path_photo_apartament(
        self,
        photo: ApartmentPhoto,
        
    ) -> Optional[Result]:
        try:
            self.session.add(photo)
            await self.session.commit()
        except Exception as ex:
            await self.session.rollback()
            raise ex


    async def delete_photos_by_apartment_id(self, apartment_id: int):
        # Запрос на получение фотографий для квартиры
        query = select(ApartmentPhoto).where(ApartmentPhoto.apartment_id == apartment_id)
        result = await self.session.execute(query)
        photos = result.scalars().all()  # Получаем список экземпляров модели
    
        # Удаляем каждую фотографию
        for photo in photos:
            await self.session.delete(photo)  # Удаляем объект из базы данных
        remove_photos(apartment_id)

        await self.session.commit()  # Сохраняем изменения в базе данных
        

    