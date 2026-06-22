"""
Central configuration for AI Smart Lecture Assistant.
Reads secrets from environment variables — never hardcode API keys here.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
try:
    load_dotenv(BASE_DIR / ".env")
except Exception:
    pass

class Config:
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey123")
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

    # Paths
    UPLOAD_FOLDER = BASE_DIR / "uploads" / "audio_files"
    TEMP_FOLDER = BASE_DIR / "uploads" / "temporary_files"
    TRANSCRIPT_FOLDER = BASE_DIR / "generated" / "transcripts"
    NOTES_FOLDER = BASE_DIR / "generated" / "notes"
    QUIZ_FOLDER = BASE_DIR / "generated" / "quizzes"
    FLASHCARD_FOLDER = BASE_DIR / "generated" / "flashcards"
    PDF_FOLDER = BASE_DIR / "generated" / "pdf_reports"
    DATABASE_PATH = BASE_DIR / "database" / "database.db"
    SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

    ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "m4a"}
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200 MB

    # AI providers — set these as real environment variables to go live.
    # Until then, modules/* fall back to mock/offline generators so the
    # whole app runs end-to-end with zero API keys.
    WHISPER_MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "base")
    GEMINI_API_KEY = "AQ.Ab8RN6LoHRuuFLkgNEjVpyvSo2tSriqhu_1WhdhWCAJYVpa8xw"

    SUPPORTED_LANGUAGES = {
        "en": "English",
        "hi": "Hindi",
        "bn": "Bengali",
    }