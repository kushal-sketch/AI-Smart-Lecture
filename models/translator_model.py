"""
translator_model.py
Handles translation of notes/transcripts into Hindi or Bengali.
Uses `deep-translator` (Google Translate backend) when available,
otherwise returns the original text with a notice.

To go live:
    pip install deep-translator
"""
from config import Config

_LANG_CODES = {"en": "en", "hi": "hi", "bn": "bn"}


def translate_text(text: str, target_language: str = "en") -> str:
    if target_language not in Config.SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {target_language}")

    if target_language == "en":
        return text

    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="auto", target=_LANG_CODES[target_language]).translate(text)
    except Exception:
        label = Config.SUPPORTED_LANGUAGES[target_language]
        return f"[{label} translation unavailable in this environment]\n\n{text}"
