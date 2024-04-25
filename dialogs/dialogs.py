from aiogram_dialog import Dialog
from windows.windows import main_window, select_from_language, select_to_language

main_dialog = Dialog(main_window, select_from_language, select_to_language)
