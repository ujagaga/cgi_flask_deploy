import sys
import sqlite3
import settings
import logging

logger = logging.getLogger(__name__)

def check_table_exists(connection, tablename):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (tablename,))
    data = cursor.fetchone()
    result = bool(data)
    cursor.close()
    return result


def init_database(connection):
    cursor = connection.cursor()

    if not check_table_exists(connection, "users"):
        sql = """
               CREATE TABLE users (
                   user TEXT NOT NULL UNIQUE,
                   token TEXT UNIQUE                
               );
               """
        cursor.execute(sql)
        connection.commit()

    if not check_table_exists(connection, "folders"):
        sql = """
        CREATE TABLE folders (
            path TEXT NOT NULL UNIQUE,
            version TEXT            
        );
        """
        cursor.execute(sql)
        connection.commit()

    cursor.close()


def open_db():
    connection = sqlite3.connect(settings.DB_NAME)
    connection.row_factory = sqlite3.Row  # So we can use row["colname"]
    return connection


def close_db(connection):
    connection.close()


def add_user(connection, user: str, token: str):
    sql = "INSERT OR REPLACE INTO users (user, token) VALUES (?, ?);"

    try:
        connection.execute(sql, (user, token))
        connection.commit()
    except Exception as exc:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.exception(f"ERROR adding user to db on line {exc_tb.tb_lineno}!\n\t{exc}")


def delete_user(connection, user: str):
    sql = "DELETE FROM users WHERE user = ?;"

    try:
        connection.execute(sql, (user,))
        connection.commit()
    except Exception as exc:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.exception(f"ERROR deleting user from db on line {exc_tb.tb_lineno}!\n\t{exc}")


def get_user(connection, user: str = None, token: str = None):
    one = True
    if user:
        sql = "SELECT * FROM users WHERE user = ?;"
        params = (user,)
    elif token:
        sql = "SELECT * FROM users WHERE token = ?;"
        params = (token,)
    else:
        sql = "SELECT * FROM users;"
        params = ()
        one = False

    user = None
    try:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        if one:
            row = cursor.fetchone()
            user = dict(row) if row else None
        else:
            rows = cursor.fetchall()
            user = []
            for r in rows:
                row_dict = dict(r)
                user.append(row_dict)

    except Exception as exc:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.exception(f"ERROR getting users from db on line {exc_tb.tb_lineno}!\n\t{exc}")
        if "no such table" in f"{exc}":
            # Try to initialize the database
            init_database(connection)
    return user


def update_user(connection, user: str, token: str):
    user_data = get_user(connection, user=user)

    if user_data:
        user_data["token"] = token
        sql = "UPDATE users SET token = ? WHERE user = ?;"
        params = (token, user)

        try:
            connection.execute(sql, params)
            connection.commit()
        except Exception as exc:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.exception(f"ERROR updating user in db on line {exc_tb.tb_lineno}!\n\t{exc}")
    else:
        add_user(connection, user, token)


def add_folder(connection, path: str, version: str):
    sql = "INSERT OR REPLACE INTO folders (path, version) VALUES (?, ?);"

    try:
        connection.execute(sql, (path, version))
        connection.commit()
    except Exception as exc:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.exception(f"ERROR adding user to db on line {exc_tb.tb_lineno}!\n\t{exc}")


def delete_folder(connection, path: str):
    sql = "DELETE FROM folders WHERE path = ?;"

    try:
        connection.execute(sql, (path,))
        connection.commit()
    except Exception as exc:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.exception(f"ERROR deleting folder from db on line {exc_tb.tb_lineno}!\n\t{exc}")


def get_folder(connection, path: str = None):
    if path:
        sql = "SELECT * FROM folders WHERE path = ?;"
        params = (path,)
        one = True
    else:
        sql = "SELECT * FROM folders;"
        params = ()
        one = False

    folders = None
    try:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        if one:
            row = cursor.fetchone()
            folders = dict(row) if row else None
        else:
            rows = cursor.fetchall()
            folders = []
            for r in rows:
                folders.append(dict(r))

    except Exception as exc:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.exception(f"ERROR getting folder from db on line {exc_tb.tb_lineno}!\n\t{exc}")
        if "no such table" in f"{exc}":
            # Try to initialize the database
            init_database(connection)
    return folders


def update_folder(connection, path: str, version: str):
    folder = get_folder(connection, path=path)

    if folder:
        sql = "UPDATE folder SET version = ? WHERE path = ?;"
        params = (version, path)

        try:
            connection.execute(sql, params)
            connection.commit()
        except Exception as exc:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.exception(f"ERROR updating folder in db on line {exc_tb.tb_lineno}!\n\t{exc}")

