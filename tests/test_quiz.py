"""test_quiz.py — basic checks for quiz generation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.gemini_model import generate_quiz


def test_generate_quiz_returns_list_of_questions():
    quiz = generate_quiz("A short lecture transcript about gravity.", num_questions=3)
    assert isinstance(quiz, list)
    assert len(quiz) == 3
    for q in quiz:
        assert "question" in q
        assert "options" in q
        assert "answer" in q
