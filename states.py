from aiogram.fsm.state import State, StatesGroup


class Notes(StatesGroup):
    """
    Конечный автомат для заметок и их редактирования
    """
    show_notes = State()
    choose_notes = State()

    create_title = State()
    create_text = State()

    choose_edit = State()
    choose_edit_title = State()
    choose_edit_text = State()

    delete_notes = State()
