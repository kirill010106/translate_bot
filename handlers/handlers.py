from aiogram import Router, types
from aiogram.filters import CommandStart
router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message):
    await message.answer("Добро пожаловать! Этот бот поможет вам с переводом желаемого текста.")
