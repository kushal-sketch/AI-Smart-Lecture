"""
database_manager.py
Thin wrapper around SQLite for the AI Smart Lecture Assistant.
All other modules talk to the database only through this class.
"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from config import Config


class DatabaseManager:
    def __init__(self, db_path: Path = Config.DATABASE_PATH, schema_path: Path = Config.SCHEMA_PATH):
        self.db_path = Path(db_path)
        self.schema_path = Path(schema_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with self._connect() as conn:
            with open(self.schema_path, "r") as f:
                conn.executescript(f.read())
            self._migrate(conn)

    def _migrate(self, conn):
        """Lightweight, additive migration so existing databases created
        before auth was added keep working without manual SQL surgery."""
        columns = [row["name"] for row in conn.execute("PRAGMA table_info(lectures)")]
        if "user_id" not in columns:
            conn.execute("ALTER TABLE lectures ADD COLUMN user_id INTEGER REFERENCES users(id)")

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # ---------- Lectures ----------

    def create_lecture(self, lecture_name: str, audio_path: str, language: str = "en", user_id: int = None) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO lectures (lecture_name, audio_path, language, user_id) VALUES (?, ?, ?, ?)",
                (lecture_name, audio_path, language, user_id),
            )
            self._bump_stat(conn, "total_lectures")
            return cur.lastrowid

    def update_lecture(self, lecture_id: int, **fields):
        if not fields:
            return
        fields["updated_at"] = "CURRENT_TIMESTAMP_PLACEHOLDER"
        set_clause = ", ".join(f"{k} = ?" for k in fields if k != "updated_at")
        set_clause += ", updated_at = datetime('now')"
        values = [v for k, v in fields.items() if k != "updated_at"]
        with self._connect() as conn:
            conn.execute(f"UPDATE lectures SET {set_clause} WHERE id = ?", (*values, lecture_id))

    def get_lecture(self, lecture_id: int):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM lectures WHERE id = ?", (lecture_id,)).fetchone()
            return dict(row) if row else None

    def list_lectures(self, limit: int = 100, user_id: int = None):
        with self._connect() as conn:
            if user_id is not None:
                rows = conn.execute(
                    "SELECT * FROM lectures WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
                    (user_id, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM lectures ORDER BY created_at DESC LIMIT ?", (limit,)
                ).fetchall()
            return [dict(r) for r in rows]

    # ---------- Users ----------

    def create_user(self, username: str, email: str, password_hash: str) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash),
            )
            return cur.lastrowid

    def get_user_by_id(self, user_id: int):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(row) if row else None

    def get_user_by_username(self, username: str):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            return dict(row) if row else None

    def get_user_by_email(self, email: str):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return dict(row) if row else None

    # ---------- Dashboard stats ----------

    def _bump_stat(self, conn, column: str, by: int = 1):
        conn.execute(f"UPDATE dashboard_stats SET {column} = {column} + ? WHERE id = 1", (by,))

    def increment_stat(self, column: str, by: int = 1):
        with self._connect() as conn:
            self._bump_stat(conn, column, by)

    def get_dashboard_stats(self) -> dict:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM dashboard_stats WHERE id = 1").fetchone()
            return dict(row) if row else {}
