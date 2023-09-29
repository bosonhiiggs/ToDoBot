from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           KeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def notes_builder_kb(count_notes):
    builder = ReplyKeyboardBuilder()
    for i in range(1, count_notes + 1):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(2)
    builder.row(KeyboardButton(text="Новая заметка"), KeyboardButton(text="Главное меню"))
    # builder.add(KeyboardButton(text="Главное меню"))
    return builder


def note_action_kb():
    action_kb = [
        [
            InlineKeyboardButton(text="Изменить заголовок", callback_data="title"),
            InlineKeyboardButton(text="Изменить текст", callback_data="text"),
        ],
        [
            InlineKeyboardButton(text="Удалить", callback_data="delete"),
        ]
    ]

    action_keyboard = InlineKeyboardMarkup(inline_keyboard=action_kb)
    return action_keyboard
