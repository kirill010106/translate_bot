import logging

from aiogram import types
from aiogram_dialog.widgets.input import MessageInput

from states.states import UserState

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from sql_cursor import read_user_language, write_user_language


async def get_user_info(dialog_manager: DialogManager, **kwargs):
    return {
        "from_id": read_user_language(dialog_manager.event.from_user.id, "from"),
        "to_id": read_user_language(dialog_manager.event.from_user.id, "to"),
        # "from_language_code": dialog_manager.event.from_user.text
    }


main_window = Window(
    Const("Добро пожаловать! Этот бот поможет вам с переводом текста. Выберите исходный язык, либо система распознает его автоматически"),
    Format("Текущий исходный язык: {from_id}"),
    Format("Результат будет на языке: {to_id}"),
    Button(Const("Приступить к переводу"), id="start_translate"),
    SwitchTo(Const("Выбрать исходный язык"), id="from_language_set", state=UserState.set_from_lang),
    SwitchTo(Const("Выбрать язык переведённого текста"), id="to_language_set", state=UserState.set_to_lang),
    getter=get_user_info,
    state=UserState.main,

)


async def handle_and_back_to_menu(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["from_lang"] = message.text
    logging.info(f"{message.text}")
    write_user_language(dialog_manager.event.from_user.id, dialog_manager.dialog_data["from_lang"], "from")
    await dialog_manager.back()

async def handle_and_back_to_menu_to(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["to_lang"] = message.text
    logging.info(f"{message.text}")
    write_user_language(dialog_manager.event.from_user.id, dialog_manager.dialog_data["to_lang"], "to")
    await dialog_manager.start(UserState.main)


select_from_language = Window(
    Const("Введите код желаемого языка в виде 'xx', например 'ru'"),
    MessageInput(handle_and_back_to_menu),
    state=UserState.set_from_lang,
)

select_to_language = Window(
    Const("Введите код желаемого языка в виде 'xx', например 'ru'"),
    MessageInput(handle_and_back_to_menu_to),
    state=UserState.set_to_lang,
)

