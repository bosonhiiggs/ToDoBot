from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb = [[KeyboardButton(text="Главное меню")]]

main_menu_reply_keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
