from typing import List, Optional

from sqlalchemy import desc, select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.models import Users  

from app.core.repo.base import BaseRepo
from app.core.config import settings


class UsersApiRepo(BaseRepo):
    
    async def get_user_admin(self) -> Users:
        stmt = select(Users).where(Users.tg_id == settings.bot.admin_id)
        result: Result = await self.session.scalars(stmt)
        return result