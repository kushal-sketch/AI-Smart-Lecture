"""
flashcard_generator.py
Coordinates transcript -> flashcards (JSON), saving the result to disk.
"""
import json
from pathlib import Path
from config import Config
from models.gemini_model import generate_flashcards


def generate_flashcards_from_transcript(transcript_path: str, lecture_id: int, num_cards: int = 8) -> str:
    transcript = Path(transcript_path).read_text(encoding="utf-8")

    try:
        cards = generate_flashcards(transcript, num_cards=num_cards)
        if not isinstance(cards, list) or len(cards) == 0:
            raise ValueError("Empty flashcards returned")
    except Exception:
        cards = generate_flashcards("", num_cards=num_cards)

    Config.FLASHCARD_FOLDER.mkdir(parents=True, exist_ok=True)
    out_path = Config.FLASHCARD_FOLDER / f"flashcards_{lecture_id:03d}.json"
    out_path.write_text(json.dumps(cards, indent=2), encoding="utf-8")

    return str(out_path)