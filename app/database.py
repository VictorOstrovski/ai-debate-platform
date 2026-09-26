import sqlite3

DB_NAME = "debates.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS debates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            statement TEXT NOT NULL,
            pro TEXT NOT NULL,
            con TEXT NOT NULL,
            arbiter TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_debate(
    statement: str,
    pro: str,
    con: str,
    arbiter: str
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO debates (
            statement,
            pro,
            con,
            arbiter
        )
        VALUES (?, ?, ?, ?)
    """, (
        statement,
        pro,
        con,
        arbiter
    ))

    conn.commit()

    debate_id = cursor.lastrowid

    conn.close()

    return debate_id


def get_all_debates():

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT
            id,
            statement,
            created_at
        FROM debates
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return rows


def get_debate_by_id(debate_id: int):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    row = cursor.execute("""
        SELECT *
        FROM debates
        WHERE id = ?
    """, (debate_id,)).fetchone()

    conn.close()

    return row