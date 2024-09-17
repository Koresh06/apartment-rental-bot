from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Next, Row, Back, Url
from app.tgbot.bot import dp
from app.core.config import settings
from app.tgbot.dialog.user.getters import username_getter
from app.tgbot.dialog.user.handlers import correct_phone_handler, error_phone_handler
from app.tgbot.dialog.user.state import StartSG
from app.tgbot.dialog.user.utils import phone_check



start_dialog = Dialog(
    Window(
        Format("Привет, {username}!", when="new_user"),
        Format("Вы новый пользователь, {username}!", when="not_new_user"),
        Next(
            Const(text="Введите номер телефона"),
            id="id_phone",
            when="not_new_user",
        ),
        Format("Панель администратора", when="check_admin"),
        Url(
            text=Const("🔰 Панель администратора"),
            url=Const(settings.api.web_server_admin),
            id="admin_panel",
            when="check_admin",
        ),
        getter=username_getter,
        state=StartSG.start,
    ),
    Window(
        Const(text="Введите номер телефона"),
        TextInput(
            id="phone_input",
            type_factory=phone_check,
            on_success=correct_phone_handler,
            on_error=error_phone_handler,
        ),
        Back(Const("◀️ Назад"), id="back"),
        state=StartSG.phone,
    ),
)


@dp.message(CommandStart())
async def command_start_process(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)