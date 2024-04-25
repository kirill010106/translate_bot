from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from states.states import UserState
from dialogs.dialogs import main_dialog
from aiogram_dialog import DialogManager, StartMode
from sql_cursor import write_new_user, read_user_info
router = Router()
router.include_router(main_dialog)


@router.message(CommandStart())
async def start_message(message: types.Message, dialog_manager: DialogManager):
    k = 0
    if k == 0:
        write_new_user(message.from_user.id, message.from_user.first_name)
        k += 1
    await dialog_manager.start(UserState.main, mode=StartMode.RESET_STACK)


@router.message(Command("dump"))
async def dump_db(message: types.Message):
    await message.answer(str(read_user_info(message.from_user.id)))


# async def set_from_language(callback: CallbackQuery, button: Button,
#                      dialog_manager: DialogManager):
#     await dialog_manager.start(UserState.set_from_lang, mode=StartMode.RESET_STACK)
