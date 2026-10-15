import sqlite3

DB_PATH = "reviews.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review TEXT NOT NULL,
                label TEXT NOT NULL,
                theme TEXT NOT NULL,
                score INTEGER NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_results(review, label, theme, score):
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO reviews (review, label, theme, score) VALUES (?, ?, ?, ?)",
            (review, label, theme, score),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def read_history():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            "SELECT id, review, label, theme, score FROM reviews ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
