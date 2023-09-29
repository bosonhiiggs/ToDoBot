import psycopg2

from database.config_info import host, user, password, db_name


def delete_note(note_id: int) -> None:
    """
    Удаление записи по ее ID
    :param note_id: ID заметки
    :return: None
    """
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )

    query = """
        DELETE FROM Notes WHERE id = {}
    """.format(note_id)

    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


def insert_notes(user_id: int, title: str, text: str) -> None:
    """
    Создание новой заметки
    :param user_id: ID пользователя внутри БД
    :param title: Заголовок заметки
    :param text: Текст заметки
    :return: None
    """
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )

    query = """
        INSERT INTO Notes(title, text, user_id) VALUES ('{}', '{}', {})
    """.format(title, text, user_id)

    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


def show_notes(user_id: int) -> list | None:
    """
    Вносит информацию о заметках пользователя
    :param user_id: Telegram ID пользователя
    :return: Список с заметками | None
    """
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )

    query = """
        SELECT notes.id, notes.title, notes.text FROM Notes
        WHERE notes.user_id = {}
    """.format(user_id)

    with connection.cursor() as cursor:
        cursor.execute(query)
        notes_info = cursor.fetchall()
    if notes_info is not None:
        return notes_info
    else:
        return None


def update_title_note(note_id: int, title: str) -> None:
    """
    Вносит изменения в заголовок
    :param note_id: ID заметки в БД
    :param title: Новый заголовок
    :return: None
    """
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )

    query = """
        UPDATE Notes SET title = '{}' WHERE id = {}
    """.format(title, note_id)

    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


def update_text_note(note_id: int, text: str) -> None:
    """
    Вносит изменения в текст
    :param note_id: ID заметки в БД
    :param text: Новый текст
    :return: None
    """
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )

    query = """
        UPDATE Notes SET text = '{}' WHERE id = {}
    """.format(text, note_id)

    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()