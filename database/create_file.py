import psycopg2

from config_info import host, user, password, db_name

try:
    # Connecting to exist database_console_commands
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )
    connection.autocommit = True

    # Test connection
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Server version: {cursor.fetchone()}")

    # Create tables
    with connection.cursor() as cursor:

        cursor.execute(
            """CREATE TABLE Users(
                    id serial PRIMARY KEY,
                    telegram_id integer UNIQUE 
                );"""
        )

        cursor.execute(
            """CREATE TABLE ToDos(
                    id serial PRIMARY KEY,
                    title varchar(30),
                    archive_is boolean NOT NULL DEFAULT FALSE,
                    user_id integer,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                );"""
        )

        cursor.execute(
            """CREATE TABLE ToDosText(
                    id serial PRIMARY KEY,
                    text varchar(500) NOT NULL,
                    done_is boolean NOT NULL DEFAULT FALSE,
                    todo_id integer,
                    FOREIGN KEY (todo_id) REFERENCES ToDos(id)
                );"""
        )

        cursor.execute(
            """CREATE TABLE Notes(
                    id serial PRIMARY KEY,
                    title varchar(30),
                    text varchar(500) NOT NULL,
                    user_id integer,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                );"""
        )

        # connection.commit()
        print(f"[INFO] Table created successfully")


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("[INFO] PostgreSQL connection closed")
