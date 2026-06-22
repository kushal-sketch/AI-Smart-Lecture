"""
quiz_generator.py
Coordinates transcript -> MCQ quiz (JSON), saving the result to disk.
"""
import json
from pathlib import Path
from config import Config
from models.gemini_model import generate_quiz


def generate_quiz_from_transcript(transcript_path: str, lecture_id: int, num_questions: int = 5) -> str:
    transcript = Path(transcript_path).read_text(encoding="utf-8")

    try:
        quiz = generate_quiz(transcript, num_questions=num_questions)
        # Validate it's a non-empty list before saving
        if not isinstance(quiz, list) or len(quiz) == 0:
            raise ValueError("Empty quiz returned")
    except Exception:
        # Fallback to default mock quiz
        quiz = generate_quiz("", num_questions=num_questions)

    Config.QUIZ_FOLDER.mkdir(parents=True, exist_ok=True)
    out_path = Config.QUIZ_FOLDER / f"quiz_{lecture_id:03d}.json"
    out_path.write_text(json.dumps(quiz, indent=2), encoding="utf-8")

    return str(out_path)