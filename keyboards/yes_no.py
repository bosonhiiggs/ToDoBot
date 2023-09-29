from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def yes_no_kb():
    yn_kb = [
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет"),
        ]
    ]

    yes_no_keyboard = ReplyKeyboardMarkup(
        keyboard=yn_kb,
        resize_keyboard=True,
        input_field_placeholder="Подтвердите действие"
    )
    return yes_no_keyboard
