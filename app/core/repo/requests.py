from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.tgbot.service.users_service import UserRepo



@dataclass
class RequestsRepo:

    session: AsyncSession


    @property
    def users(self) -> UserRepo:
        
        return UserRepo(self.session)