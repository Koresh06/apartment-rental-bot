from typing import Any
from aiogram.types import Message, CallbackQuery, User
from aiogram.enums.parse_mode import ParseMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog import DialogManager

from app.core.repo.requests import RequestsRepo
from app.core.config import settings

from app.tgbot.dialog.user.keyboard import new_user


# Хэндлер, который сработает на ввод некорректного номер телефона
async def error_phone_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.answer(
        text="Вы ввели некорректный номер телефона. Попробуйте еще раз"
    )

# Хэндлер, который сработает, если пользователь ввел корректный номер телефона
async def correct_phone_handler(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")

    await message.answer(text=f"Ваш номер телефона {text}")

    await repo.users.add_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        phone=text,
    )

    full_name = message.from_user.full_name or "Anonymous"

    await message.bot.send_message(
        chat_id=settings.bot.admin_id,
        text = (
            f"👤 Пользователь {full_name}\n"
            f"🆔 ID: {message.from_user.id} - зарегистрирован\n"
            f"📞 Телефон: {text}"
        ),
        reply_markup=await new_user(
            tg_id=message.from_user.id,
            full_name=full_name
        )
    )

    await dialog_manager.done()
    await message.answer(text="Регистрация прошла успешно!")

