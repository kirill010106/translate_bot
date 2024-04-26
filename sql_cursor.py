import logging
import os.path
import sqlite3
db = sqlite3.connect(os.path.abspath("users.db"))
cur = db.cursor()


def write_new_user(id: int, name: str):
    db = sqlite3.connect("users.db")
    cur = db.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO Users (user_id, user_name, selected_from_language, selected_to_language) VALUES (?,?,?,?)",
        (id, name, "default", "default")
    )
    db.commit()
    db.close()


def read_user_language(user_id: int, lang_type: str):
    db = sqlite3.connect("users.db")
    cur = db.cursor()
    if lang_type == "from":
        cur.execute(
            "SELECT selected_from_language FROM Users WHERE user_id = ?",
            (user_id,)
        )
    elif lang_type == "to":
        cur.execute(
            "SELECT selected_to_language FROM Users WHERE user_id = ?",
            (user_id,)
        )
    else:
        logging.critical(
            "TypeError: incorrect value of 'lang_type' argument. Only 'to' and 'from' params are available")
        raise "TypeError: incorrect value of 'lang_type' argument. Only 'to' and 'from' params are available"
    res = cur.fetchone()[0]
    db.close()
    return res


def write_user_language(user_id: int, lang: str, lang_type: str):
    db = sqlite3.connect("users.db")
    cur = db.cursor()
    if lang_type == "from":
        cur.execute(
            "UPDATE Users SET selected_from_language = ? WHERE user_id = ?",
            (lang, user_id)
        )
        logging.info(f"From language updated succesfully: lang:{lang}, user_id:{user_id}")
    elif lang_type == "to":
        cur.execute(
            "UPDATE Users SET selected_to_language = ? WHERE user_id = ?",
            (lang, user_id)
        )
    else:
        logging.critical(
            "TypeError: incorrect value of 'lang_type' argument. Only 'to' and 'from' params are available")
        raise "TypeError: incorrect value of 'lang_type' argument. Only 'to' and 'from' params are available"
    res = cur.fetchall()
    db.commit()
    db.close()
    return res


def read_user_info(user_id):
    db = sqlite3.connect("users.db")
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM Users WHERE user_id = ?",
        (user_id,)
    )
    res = cur.fetchall()
    db.close()
    return res

def dump_all_db():
    db = sqlite3.connect("users.db")
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM Users"
    )
    res = cur.fetchall()
    db.close()
    return res

def swap_user_languages(user_id):
    db = sqlite3.connect("users.db")
    cur = db.cursor()
    cur.execute("""
    SELECT selected_from_language FROM Users WHERE user_id = ?
    """, (user_id,))
    from_lang = cur.fetchone()[0]
    cur.execute("""
        SELECT selected_to_language FROM Users WHERE user_id = ?
        """, (user_id,))
    to_lang = cur.fetchone()[0]
    cur.execute("UPDATE Users SET selected_from_language = ? WHERE user_id = ?", (to_lang, user_id))
    cur.execute("  UPDATE Users SET selected_to_language = ? WHERE user_id = ?", (from_lang, user_id))
    db.commit()
    db.close()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS Users(
    user_id INTEGER PRIMARY KEY NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    selected_from_language STRING NOT NULL,
    selected_to_language STRING NOT NULL
    )
    """
)
# cur.execute(
#         "INSERT OR IGNORE INTO Users (user_id, user_name, selected_from_language, selected_to_language) VALUES (?,?,?,?)",
#         (1, "k", "default", "default")
#     )
# cur.execute(
#     f"UPDATE Users SET selected_from_language = 'ru' WHERE user_id = '920909140'"
# )
# cur.execute("SELECT * FROM Users")
# print(cur.fetchall())
db.commit()
db.close()
