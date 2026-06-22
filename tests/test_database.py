"""test_database.py — basic checks for DatabaseManager."""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.database_manager import DatabaseManager
from config import Config


def test_create_and_fetch_lecture():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        db = DatabaseManager(db_path=db_path, schema_path=Config.SCHEMA_PATH)

        lecture_id = db.create_lecture("Test Lecture", "/tmp/audio.mp3", language="en")
        lecture = db.get_lecture(lecture_id)

        assert lecture is not None
        assert lecture["lecture_name"] == "Test Lecture"
        assert lecture["status"] == "uploaded"


def test_dashboard_stats_increment():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        db = DatabaseManager(db_path=db_path, schema_path=Config.SCHEMA_PATH)

        db.create_lecture("Lecture A", "/tmp/a.mp3")
        stats = db.get_dashboard_stats()
        assert stats["total_lectures"] == 1
