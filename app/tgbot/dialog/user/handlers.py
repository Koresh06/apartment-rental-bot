from typing import Any
from aiogram.types import Message, CallbackQuery, User
from aiogram.enums.parse_mode import ParseMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog import DialogManager, StartMode

from app.core.repo.requests import RequestsRepo
from app.core.config import settings

from app.tgbot.dialog.user.keyboard import new_user
from app.tgbot.dialog.user.state import MainSG


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

    await message.answer(text=(
        f"🎉 Поздравляем, {full_name}! Вы успешно завершили регистрацию.\n\n"
        f"📱 Ваш номер телефона: {text}\n"
        "✨ Теперь вы можете пользоваться всеми возможностями нашего сервиса. "
        "Если у вас возникнут вопросы, мы всегда рады помочь!"
    )
)
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)
    

