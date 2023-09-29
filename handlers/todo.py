from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.cancel import main_menu_reply_keyboard

router = Router()


@router.callback_query(F.data == "todo")
async def todo_func(callback: CallbackQuery):
    await callback.message.answer("Тут заметки ToDo", reply_markup=main_menu_reply_keyboard)
    await callback.answer()
