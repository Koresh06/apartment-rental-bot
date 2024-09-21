from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.tgbot.service.users_service import BotUserRepo
from app.api.api_v1.services.apartament_service import ApartamentRepo
from app.api.api_v1.services.apartament_photo_service import ApartamentPhotoRepo



@dataclass
class RequestsRepo:

    session: AsyncSession


    @property
    def users(self) -> BotUserRepo:
        
        return BotUserRepo(self.session)
    

    @property
    def apartaments(self) -> ApartamentRepo:
        
        return ApartamentRepo(self.session)
    

    @property
    def apartament_photos(self) -> ApartamentPhotoRepo:
        
        return ApartamentPhotoRepo(self.session)
    