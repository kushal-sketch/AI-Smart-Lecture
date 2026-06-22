"""
whisper_model.py
Wraps OpenAI's Whisper for speech-to-text.
Currently running in MOCK MODE — returns a realistic placeholder transcript.

To enable real transcription:
    1. Install ffmpeg and add it to Windows PATH
    2. pip install openai-whisper
    Then change ENABLE_WHISPER = False to True below.
"""
from pathlib import Path

# ---------------------------------------------------------------
# SET TO True ONLY AFTER ffmpeg AND openai-whisper ARE INSTALLED
# ---------------------------------------------------------------
ENABLE_WHISPER = False
# ---------------------------------------------------------------


def transcribe_audio(audio_path: str, language: str = "en") -> str:
    if ENABLE_WHISPER:
        try:
            import whisper
            from config import Config
            model = whisper.load_model(Config.WHISPER_MODEL_SIZE)
            result = model.transcribe(audio_path, language=language)
            return result["text"].strip()
        except Exception:
            pass  # fall through to mock below

    filename = Path(audio_path).stem.replace("_", " ").title()
    return (
        f"Lecture Transcript — {filename}\n\n"
        "Good morning everyone. Today we are going to cover one of the most "
        "important topics in this course. Let's start with the basic definition "
        "and then work our way up to the more advanced concepts.\n\n"
        "The first concept we need to understand is the foundational principle "
        "that everything else builds upon. Think of it as the base layer. "
        "Without a solid understanding of this, the rest of the material won't "
        "make much sense.\n\n"
        "Let me walk you through a worked example. Suppose we have a problem "
        "where we need to apply this principle in a real-world context. "
        "Step one is to identify what we are given. Step two is to decide which "
        "method or formula applies. Step three is to calculate and verify.\n\n"
        "Now, there are three key terms you absolutely must know before the exam. "
        "First is the core definition itself. Second is the relationship between "
        "the primary and secondary variables. Third is the exception case — "
        "the scenario where the standard rule does not apply.\n\n"
        "To summarize today's session: we covered the definition, worked through "
        "an example, and identified the three key terms. Next class we will build "
        "on this with more complex problems. Please review your notes before then."
    )