"""
auth_manager.py
Flask-Login integration: a thin User wrapper around the `users` table
row, plus password hashing helpers. Keeps app.py free of password
handling details.
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    """Wraps a `users` table row so Flask-Login can track session state."""

    def __init__(self, row: dict):
        self.id = row["id"]
        self.username = row["username"]
        self.email = row["email"]
        self.password_hash = row["password_hash"]

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password)
