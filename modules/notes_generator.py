"""
notes_generator.py
Coordinates transcript -> study notes, saving the result to disk.
"""
from pathlib import Path
from config import Config
from models.gemini_model import generate_notes


def generate_notes_from_transcript(transcript_path: str, lecture_id: int) -> str:
    transcript = Path(transcript_path).read_text(encoding="utf-8")
    notes_text = generate_notes(transcript)

    Config.NOTES_FOLDER.mkdir(parents=True, exist_ok=True)
    out_path = Config.NOTES_FOLDER / f"notes_{lecture_id:03d}.txt"
    out_path.write_text(notes_text, encoding="utf-8")

    return str(out_path)
