from aiogram.filters.state import StatesGroup, State


class UserState(StatesGroup):
    main = State()
    set_from_lang = State()
    set_to_lang = State()
    language_list = State()
    text_input = State()
    done = State()
    reload = State()
