"""
translator.py
Thin module-level wrapper so app.py only imports from `modules/`.
"""
from models.translator_model import translate_text


def translate_content(text: str, target_language: str) -> str:
    return translate_text(text, target_language)
