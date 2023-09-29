from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


call_mm_kb = [[InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]]

calling_main_menu = InlineKeyboardMarkup(inline_keyboard=call_mm_kb)


mm_kb = [
    [
        InlineKeyboardButton(text='ToDo', callback_data="todo"),
        InlineKeyboardButton(text='Notes', callback_data="notes"),
    ]
]
main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=mm_kb)

