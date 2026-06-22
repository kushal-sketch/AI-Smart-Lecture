"""
qa_manager.py
Powers the "Ask AI about this lecture" feature. Reads the lecture's own
transcript and asks Gemini (or the mock fallback) a grounded question
about it, so answers are based on what was actually said in class
rather than the model's general knowledge.
"""
from pathlib import Path
from models.gemini_model import answer_question


def ask_about_lecture(transcript_path: str, question: str) -> str:
    transcript = Path(transcript_path).read_text(encoding="utf-8")
    return answer_question(transcript, question)
