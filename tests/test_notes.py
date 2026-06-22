"""test_notes.py — basic checks for notes generation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.gemini_model import generate_notes


def test_generate_notes_returns_text():
    notes = generate_notes("A short lecture transcript about gravity.")
    assert isinstance(notes, str)
    assert len(notes) > 0
