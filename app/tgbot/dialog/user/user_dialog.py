from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Next, Row, Back, Url, Group, SwitchTo
from app.tgbot.bot import dp
from app.core.config import settings
from app.tgbot.dialog.user.getters import username_getter
from app.tgbot.dialog.user.handlers import correct_phone_handler, error_phone_handler
from app.tgbot.dialog.user.state import MainSG, StartSG
from app.tgbot.dialog.user.utils import phone_check
from app.core.repo.requests import RequestsRepo



# start_dialog = Dialog(
#     Window(
#         Format("Привет, {username}!", when="new_user"),
#         Format("Вы новый пользователь, {username}!", when="not_new_user"),
#         Next(
#             Const(text="Введите номер телефона"),
#             id="id_phone",
#             when="not_new_user",
#         ),
#         Format("Панель администратора", when="check_admin"),
#         Url(
#             text=Const("🔰 Панель администратора"),
#             url=Const(settings.api.web_server_admin),
#             id="admin_panel",
#             when="check_admin",
#         ),
#         getter=username_getter,
#         state=StartSG.start,
#     ),
#     Window(
#         Const(text="Введите номер телефона"),
#         TextInput(
#             id="phone_input",
#             type_factory=phone_check,
#             on_success=correct_phone_handler,
#             on_error=error_phone_handler,
#         ),
#         Back(Const("◀️ Назад"), id="back"),
#         state=StartSG.phone,
#     ),
# )

async def catalog_handler(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.answer("Здесь будет каталог квартир")

async def profile_handler(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.answer("Здесь будет ваш профиль")

async def faq_handler(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.answer("Здесь будет FAQ")


start_dialog = Dialog(
    Window(
        Format("Вы новый пользователь, {username}!", when="new_user"),
        Next(
            Const(text="Пройти регистрацию ▶"),
            id="registration",
            when="new_user",
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
    )
)

main_dialog = Dialog(
    Window(
        Const("<b>Главное меню</b>", when="not_new_user"),
        Group(
            Button(Const("🏠 Каталог квартир"), id="catalog", on_click=catalog_handler),
            Button(Const("👤 Мой профиль"), id="profile", on_click=profile_handler),
            Button(Const("❓ FAQ"), id="faq", on_click=faq_handler),
            width=2,  # количество кнопок в строке
            when="not_new_user"
        ),
        Url(
            text=Const("🔰 Панель администратора"),
            url=Const(settings.api.web_server_admin),
            id="admin_panel",
            when="check_admin",
        ),
        state=MainSG.main,
        getter=username_getter,
    )
)


@dp.message(CommandStart())
async def command_start_process(callback: CallbackQuery, dialog_manager: DialogManager):
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    user = await repo.users.check_user(callback.from_user.id)

    if user or callback.from_user.id == settings.bot.admin_id:
        await dialog_manager.start(state=MainSG.main, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
