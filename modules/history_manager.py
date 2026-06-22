"""
history_manager.py
Read-side helper for the lecture history page.
"""
from database.database_manager import DatabaseManager


def get_history(db: DatabaseManager, limit: int = 100, user_id: int = None):
    return db.list_lectures(limit=limit, user_id=user_id)
