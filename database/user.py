import psycopg2

from .config_info import host, user, password, db_name


def get_user_id(telegram_id: int) -> int:
    """
    Возвращает информацию о User_ID
    :param telegram_id: Telegram ID пользователя
    :return: user_id
    """
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )
    query = """
        SELECT users.id FROM Users WHERE users.telegram_id = {}
    """.format(telegram_id)

    with connection.cursor() as cursor:
        cursor.execute(query)

        telegram_id = cursor.fetchone()

    return telegram_id[0]


async def register(user_id: int) -> None:
    """
    Вносит информацию о пользователе
    :param user_id: Telegram ID пользователя
    :return: None
    """
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )

    query = """
            INSERT INTO Users(telegram_id) VALUES ({})
    """.format(user_id)

    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
