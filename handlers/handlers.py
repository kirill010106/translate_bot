import logging

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from config_data.config import load_config
from states.states import UserState
from dialogs.dialogs import main_dialog
from aiogram_dialog import DialogManager, StartMode, ShowMode
from sql_cursor import write_new_user, read_user_info, dump_all_db
from aiogram_dialog.api.exceptions import UnknownIntent

router = Router()
router.include_router(main_dialog)
config = load_config()


@router.message(CommandStart())
async def start_message(message: types.Message, dialog_manager: DialogManager):
    write_new_user(message.from_user.id, message.from_user.first_name)
    await dialog_manager.start(UserState.main, mode=StartMode.RESET_STACK)


@router.message(Command("dump"))
async def dump_db(message: types.Message):
    if str(message.from_user.id) == config.tg_bot.admin_ids:
        await message.answer(str(dump_all_db()))


async def on_unknown_intent(event, dialog_manager: DialogManager):
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(UserState.reload, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)