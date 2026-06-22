"""
speech_to_text.py
Coordinates audio -> transcript, saving the result to disk.
"""
from pathlib import Path
from config import Config
from models.whisper_model import transcribe_audio


def process_audio_to_transcript(audio_path: str, lecture_id: int, language: str = "en") -> str:
    """Transcribes the audio file and saves the transcript to disk.
    Returns the path to the saved transcript file.
    """
    transcript_text = transcribe_audio(audio_path, language=language)

    Config.TRANSCRIPT_FOLDER.mkdir(parents=True, exist_ok=True)
    out_path = Config.TRANSCRIPT_FOLDER / f"transcript_{lecture_id:03d}.txt"
    out_path.write_text(transcript_text, encoding="utf-8")

    return str(out_path)
