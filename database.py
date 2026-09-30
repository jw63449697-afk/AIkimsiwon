import sqlite3
from pathlib import Path
from datetime import datetime, timezone

def _connect(database_path: str):
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(database_path, timeout=10)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(database_path: str):
    with _connect(database_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                input_text TEXT NOT NULL,
                response_text TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(guild_id, input_text, response_text)
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_learnings_lookup
            ON learnings(guild_id, input_text)
        """)
        conn.commit()

def add_learning(database_path: str, guild_id: int | None, input_text: str, response_text: str) -> bool:
    if guild_id is None:
        return False

    normalized_input = " ".join(input_text.split())
    normalized_response = response_text.strip()

    with _connect(database_path) as conn:
        cursor = conn.execute("""
            INSERT OR IGNORE INTO learnings
            (guild_id, input_text, response_text, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            guild_id,
            normalized_input,
            normalized_response,
            datetime.now(timezone.utc).isoformat()
        ))
        conn.commit()
        return cursor.rowcount == 1

def get_responses(database_path: str, guild_id: int | None, input_text: str) -> list[str]:
    if guild_id is None:
        return []

    normalized_input = " ".join(input_text.split())

    with _connect(database_path) as conn:
        rows = conn.execute("""
            SELECT response_text
            FROM learnings
            WHERE guild_id = ? AND input_text = ?
        """, (guild_id, normalized_input)).fetchall()

    return [row[0] for row in rows]

def count_inputs(database_path: str, guild_id: int | None) -> int:
    if guild_id is None:
        return 0

    with _connect(database_path) as conn:
        row = conn.execute("""
            SELECT COUNT(DISTINCT input_text)
            FROM learnings
            WHERE guild_id = ?
        """, (guild_id,)).fetchone()

    return int(row[0])
