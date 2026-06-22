"""
dashboard_manager.py
Read-side helper for dashboard analytics.

`stats` are app-wide totals (across all users of this instance).
`recent_lectures` is scoped to the given user_id so each person only
sees their own lectures, not everyone else's.
"""
from database.database_manager import DatabaseManager


def get_dashboard_data(db: DatabaseManager, user_id: int = None) -> dict:
    stats = db.get_dashboard_stats()
    recent = db.list_lectures(limit=5, user_id=user_id) if user_id is not None else []
    return {"stats": stats, "recent_lectures": recent}
