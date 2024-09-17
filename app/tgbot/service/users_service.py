from typing import Optional

from sqlalchemy import select, Result
from app.core.models import Users  

from app.core.repo.base import BaseRepo


class UserRepo(BaseRepo):


    async def check_user(self, tg_id: int):
        user = await self.session.scalar(select(Users).where(Users.tg_id == tg_id))

        if user:
            return True
        return False
    

    async def add_user(self, tg_id: int, username: str, full_name: str, phone: str):
        try:
            new_user = Users(
                tg_id=tg_id,
                username=username,
                full_name=full_name,
                phone=phone,
            )
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user 
        except Exception as ex:
            await self.session.rollback()
            print(f"Ошибка при добавлении пользователя: {ex}")