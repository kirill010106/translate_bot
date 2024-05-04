from aiogram import types
from aiogram_dialog.widgets.input import MessageInput

from states.states import UserState

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Cancel
from aiogram_dialog.widgets.text import Const, Format
from sql_cursor import read_user_language, write_user_language, swap_user_languages
from utils.compare_language import compare_language, get_list
from translate_api import translate_text

async def get_user_info(dialog_manager: DialogManager, **kwargs):
    return {
        "from_id": compare_language(read_user_language(dialog_manager.event.from_user.id, "from")),
        "to_id": compare_language(read_user_language(dialog_manager.event.from_user.id, "to")),
    }


async def swap_languages(callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    user_id = dialog_manager.event.from_user.id
    swap_user_languages(user_id)
    await dialog_manager.start(UserState.main)

reload_window = Window(
    Const("Бот был перезапущен. Для возврата в главное меню воспользуйтесь кнопкой."),
    SwitchTo(Const("Перейти в главное меню"), state=UserState.main, id="back_to_menu_from_reload"),
    state=UserState.reload
)

main_window = Window(
    Const(
        "Добро пожаловать! Этот бот поможет вам с переводом текста. Задайте нужные языки."),
    Format("Текущий исходный язык: {from_id}"),
    Format("Результат будет на языке: {to_id}"),
    SwitchTo(Const("Приступить к переводу"), id="start_translate", state=UserState.text_input),
    SwitchTo(Const("Выбрать исходный язык"), id="from_language_set", state=UserState.set_from_lang),
    SwitchTo(Const("Выбрать язык переведённого текста"), id="to_language_set", state=UserState.set_to_lang),
    Button(Format("Поменять языки местами"), id="swap_languages", on_click=swap_languages),
    SwitchTo(Const("Список языков"), id="language_list", state=UserState.language_list),
    getter=get_user_info,
    state=UserState.main,

)


async def handle_and_back_to_menu(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["from_lang"] = message.text
    write_user_language(dialog_manager.event.from_user.id, dialog_manager.dialog_data["from_lang"], "from")
    await dialog_manager.back()


async def handle_and_back_to_menu_to(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["to_lang"] = message.text
    write_user_language(dialog_manager.event.from_user.id, dialog_manager.dialog_data["to_lang"], "to")
    await dialog_manager.start(UserState.main)


select_from_language = Window(
    Const("Введите код желаемого языка в виде 'xx', например 'ru'"),
    SwitchTo(Const("Назад"), id="cancel_from_lang_change", state=UserState.main),
    MessageInput(handle_and_back_to_menu),
    state=UserState.set_from_lang,
)

select_to_language = Window(
    Const("Введите код желаемого языка в виде 'xx', например 'ru'"),
    SwitchTo(Const("Назад"), id="cancel_to_lang_change", state=UserState.main),
    MessageInput(handle_and_back_to_menu_to),
    state=UserState.set_to_lang,
)

language_list = Window(
    Const(get_list()),
    SwitchTo(Const("Назад"), id="go_back", state=UserState.main),
    state=UserState.language_list,
)


async def text_to_translate_handler(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["text_to_translate"] = message.text,
    dialog_manager.dialog_data["translated_text"] = translate_text(dialog_manager.dialog_data["text_to_translate"],
                                                                   read_user_language(dialog_manager.event.from_user.id,
                                                                                      "from"),
                                                                   read_user_language(dialog_manager.event.from_user.id,
                                                                                      "to"))
    await dialog_manager.switch_to(UserState.done)


async def text_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "translated_text":  dialog_manager.dialog_data["translated_text"]
    }


translated_text = Window(
    Const("Введите текст для перевода"),
    SwitchTo(Const("Назад"), state=UserState.main, id="main_menu"),
    MessageInput(text_to_translate_handler),
    state=UserState.text_input,
)

result = Window(
    Format("Переведённый текст:"),
    Format("{translated_text}"),
    SwitchTo(Const("Вернуться"), id="back_from_done", state=UserState.main),
    getter=text_getter,
    state=UserState.done
)
