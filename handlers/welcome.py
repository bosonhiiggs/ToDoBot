from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from database.user import register
from keyboards.main_menu_kb import calling_main_menu, main_menu_keyboard


router = Router()


@router.message(Command("start"))
async def cmd_welcome(message: Message):
    """
    Реакция бота на команду start. Происходит регистрация пользователя в базе данных за счет Telegram ID
    :param message: start
    :return: Вывод приветственного сообщения и клавиатуры
    """
    await message.answer("Вход...")

    try:
        await register(message.from_user.id)
    finally:
        await message.answer(text="Привет!\nЯ ToDo Bot!", reply_markup=calling_main_menu)


@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery):
    """
    Реакция на нажатие Inline кнопки "Главное меню"
    :param callback: callback кнопки
    :return: Главное меню (клавиатура)
    """
    await callback.message.answer("Главное меню", reply_markup=main_menu_keyboard)
    await callback.answer()


@router.message(F.text == "Главное меню")
async def msg_main_menu(message: Message):
    """
    Реакция на текст в чате "Главное меню"
    :param message:
    :return:
    """
    await message.answer("Главное меню", reply_markup=main_menu_keyboard)
