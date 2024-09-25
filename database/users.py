import sqlite3
from aiogram.types import Message


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('users.db')
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY,
                         username INTEGER NOT NULL,
                         score INTEGER DEFAULT 0,
                         life INTEGER DEFAULT 3);''')
    except sqlite3.Error as e:
        print(e)


async def handle_new_user(message: Message):
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        cursor = conn.cursor()
        user_exists = cursor.execute("SELECT 1 FROM users WHERE username=?", (message.from_user.id,)).fetchone()
        if user_exists is None:
            cursor.execute("INSERT INTO users (username, score, life) VALUES (?,?,?)", (message.from_user.id, 0, 3))
            conn.commit()
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

        







users_template: dict[str: int] = {
    'score': 0,
    'life': 3
}

users_db = {}


liders_db: dict[str: int] = {}