from aiogram import F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.user import get_user_id
from database.notes import update_title_note, update_text_note, insert_notes, show_notes, delete_note

from keyboards.cancel import main_menu_reply_keyboard
from keyboards.notes import notes_builder_kb, note_action_kb
from keyboards.yes_no import yes_no_kb

from states import Notes

router = Router()


@router.callback_query(F.data == "notes")
async def todo_func(callback: CallbackQuery, state: FSMContext):
    """
    Возвращает список заметок (Notes) из БД
    :param callback: Inline кнопка
    :param state: Состояние конечного автомата Notes
    :return: str
    """
    tg_id = callback.from_user.id
    user_id = get_user_id(tg_id)
    await state.set_state(Notes.show_notes)

    await callback.message.answer("Тут заметки Notes", reply_markup=main_menu_reply_keyboard)
    data_notes = show_notes(user_id)
    choose_data = dict()

    if data_notes:

        for i in range(1, len(data_notes) + 1):
            choose_data[i] = data_notes[i - 1]

        answer_text = ''

        notes_keyboard = notes_builder_kb(count_notes=len(data_notes))

        for i_key, i_value in choose_data.items():
            choose_num = i_key
            title_notes = i_value[1]
            text_notes = i_value[2]

            answer_text += f"------------------{choose_num}------------------\n" \
                           f"{html.bold(html.quote(title_notes))}\n" \
                           f"\t{text_notes}\n---------------------------------------\n\n"

        await callback.message.answer(
            answer_text,
            parse_mode="HTML",
            reply_markup=notes_keyboard.as_markup(resize_keyboard=True)
        )

        await state.update_data(live_notes=choose_data)

    else:
        notes_keyboard = notes_builder_kb(count_notes=len(data_notes))
        await callback.message.answer("Увы! Список пуст", reply_markup=notes_keyboard.as_markup(resize_keyboard=True))

    await state.set_state(Notes.choose_notes)
    await callback.answer()


@router.message(Notes.choose_notes, F.text.in_("Новая заметка"))
async def create_note(message: Message, state: FSMContext):
    """
    Создание новой заметки (Заголовок)
    :param message: запрос new
    :param state: Состояние конечного автомата Notes
    :return: None
    """
    await message.answer("Создание новой заметки")
    await message.answer("Введите заголовок")
    await state.set_state(Notes.create_title)


@router.message(Notes.create_title, F.text)
async def create_title(message: Message, state: FSMContext):
    """
    Внесение заголовка в буфер конечного автомата
    :param message: Заголовок
    :param state: Состояние конечного автомата
    :return: None
    """
    await state.update_data(title=message.text)
    await message.answer("Отлично! Теперь введите текст")
    await state.set_state(Notes.create_text)


@router.message(Notes.create_text, F.text)
async def create_text(message: Message, state: FSMContext):
    """
    Внесение текста в буфер, а потом передача данных в запрос БД
    :param message: Текст
    :param state: Состояние конечного автомата
    :return: None
    """
    await state.update_data(text=message.text)
    await message.answer("Отлично!", reply_markup=main_menu_reply_keyboard)

    note_data = await state.get_data()
    note_title_data = note_data["title"]
    note_text_data = note_data["text"]

    tg_id = message.from_user.id
    user_id = get_user_id(tg_id)

    insert_notes(user_id, note_title_data, note_text_data)

    # await state.set_state(Notes.show_notes)
    await state.clear()


@router.message(Notes.choose_notes, F.text)
async def choose_note(message: Message, state: FSMContext):
    """
    Возвращаем конкретную заметку (Notes) по запросу
    :param message: запрос
    :param state: Состояние конечного автомата Notes
    :return: str
    """
    await message.answer("Waiting...", reply_markup=main_menu_reply_keyboard)
    user_notes = await state.get_data()
    user_choose = message.text
    choosing_data = user_notes['live_notes'][int(user_choose)]
    await state.update_data(note=choosing_data)
    answer_text = f"{html.bold(html.quote(choosing_data[1]))}\n{choosing_data[2]}"
    await message.answer(answer_text, parse_mode="HTML", reply_markup=note_action_kb())
    await state.set_state(Notes.choose_edit)


@router.callback_query(Notes.choose_edit, F.data == "title")
async def note_edit(callback: CallbackQuery, state: FSMContext):
    """
    Редактирование заголовка выбранной заметки
    :param callback: Команда "title"
    :param state: Состояние конечного автомата
    :return: None
    """
    await callback.message.answer("Введите новый заголовок", reply_markup=main_menu_reply_keyboard)
    await state.set_state(Notes.choose_edit_title)
    await callback.answer()


@router.message(Notes.choose_edit_title, F.text)
async def note_title_edit(message: Message, state: FSMContext):
    """
    Внесение нового заголовка в БД
    :param message: Новый заголовок
    :param state: Состояние конечного автомата
    :return: None
    """
    new_title = message.text
    user_data_note = await state.get_data()
    choosing_note = user_data_note["note"]
    note_id = choosing_note[0]
    update_title_note(note_id, new_title)
    await message.answer("Заголовок поменян", reply_markup=main_menu_reply_keyboard)
    await state.clear()


@router.callback_query(Notes.choose_edit, F.data == "text")
async def note_edit(callback: CallbackQuery, state: FSMContext):
    """
    Редактирование текста выбранной заметки
    :param callback: Команда "text"
    :param state: Состояние конечного автомата
    :return: None
    """
    await callback.message.answer("Введите новый текст", reply_markup=main_menu_reply_keyboard)
    await state.set_state(Notes.choose_edit_text)
    await callback.answer()


@router.message(Notes.choose_edit_text, F.text)
async def note_text_edit(message: Message, state: FSMContext):
    """
    Внесение нового текста в БД
    :param message: Новый текст
    :param state: Состояние конечного автомата
    :return: None
    """
    new_text = message.text
    user_data_note = await state.get_data()
    choosing_note = user_data_note["note"]
    note_id = choosing_note[0]

    update_text_note(note_id, new_text)
    await message.answer("Текст поменян", reply_markup=main_menu_reply_keyboard)
    await state.clear()


@router.callback_query(Notes.choose_edit, F.data == "delete")
async def note_delete(callback: CallbackQuery, state: FSMContext):
    """
    Запрос на подтверждение удаления
    :param callback: Команда delete
    :param state: Состояние конечного автомата
    :return: None
    """
    yes_no = yes_no_kb()
    await callback.message.answer("Вы уверены?", reply_markup=yes_no)
    await state.set_state(Notes.delete_notes)
    await callback.answer()


@router.message(Notes.delete_notes, F.text.in_("Да"))
async def confirm_delete(message: Message, state: FSMContext):
    """
    Удаление заметки из БД
    :param message: Подтверждение
    :param state: Состояние конечного автомата
    :return: None
    """
    user_data_note = await state.get_data()
    choosing_note = user_data_note["note"]
    note_id = choosing_note[0]

    delete_note(note_id)

    await message.answer("Удаление прошло успешно", reply_markup=main_menu_reply_keyboard)


@router.message(Notes.delete_notes, F.text.in_("Нет"))
async def confirm_delete(message: Message, state: FSMContext):
    """
    Очищение стека конечного автомата
    :param message: Отрицание
    :param state: Состояние конечного автомата
    :return: None
    """
    await state.clear()
    await message.answer("Удаление отменено", reply_markup=main_menu_reply_keyboard)
