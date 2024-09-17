from aiogram_dialog import DialogManager
from aiogram.types import User

from app.core.config import settings
from app.core.repo.requests import RequestsRepo


async def username_getter(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs,
):
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    user = await repo.users.check_user(event_from_user.id)

    admin = event_from_user.id == settings.bot.admin_id


    return {
        "username": event_from_user.username,
        "new_user": not user and not admin,
        "not_new_user": user and not admin,
        "check_admin": admin,
    }