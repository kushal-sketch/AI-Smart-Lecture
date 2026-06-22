"""
gemini_model.py
Wraps Google's Gemini API for notes / quiz / flashcard / Q&A generation.
Falls back to realistic mock content when GEMINI_API_KEY is not set.

To go live:
    pip install google-generativeai
    Add your key below where it says: GEMINI_API_KEY = "your-key-here"
"""
import json
from config import Config

# ---------------------------------------------------------------
# ADD YOUR GEMINI API KEY HERE
# Get a free key from: https://aistudio.google.com
# Leave it empty ("") to use realistic mock content instead
# ---------------------------------------------------------------
GEMINI_API_KEY = ""  # e.g. "AIzaSyABC123..."
# ---------------------------------------------------------------

_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client
    key = GEMINI_API_KEY or Config.GEMINI_API_KEY
    if not key:
        _client = False
        return _client
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        _client = genai.GenerativeModel("gemini-2.0-flash")
    except Exception:
        _client = False
    return _client


def _ask_gemini(prompt: str) -> str:
    client = _get_client()
    if not client:
        return ""
    try:
        response = client.generate_content(prompt)
        return response.text
    except Exception:
        return ""


def generate_notes(transcript: str) -> str:
    text = _ask_gemini(
        f"Summarize this lecture transcript into clear, well-organized study "
        f"notes with headings and bullet points:\n\n{transcript}"
    )
    if text:
        return text

    return (
        "## Overview\n\n"
        "This lecture introduced the foundational concepts of the topic, "
        "explained through clear definitions, worked examples, and key term "
        "revision.\n\n"
        "## Core Concepts\n\n"
        "- **Foundational Principle** — The base idea that all further concepts "
        "build upon. Must be understood before moving to advanced material.\n"
        "- **Primary and Secondary Variables** — The relationship between the "
        "main input and its dependent outputs in any given problem.\n"
        "- **Exception Case** — The specific scenario where the standard rule "
        "does not apply; always check for this in exam questions.\n\n"
        "## Worked Example\n\n"
        "1. Identify what is given in the problem.\n"
        "2. Select the correct method or formula.\n"
        "3. Calculate the result and verify it makes sense.\n\n"
        "## Key Terms to Remember\n\n"
        "- **Core Definition** — The precise meaning of the central concept.\n"
        "- **Variable Relationship** — How the primary and secondary values interact.\n"
        "- **Exception Condition** — When the standard rule is overridden.\n\n"
        "## What to Review Before Next Class\n\n"
        "- Re-read the core definition and write it in your own words.\n"
        "- Redo the worked example without looking at your notes.\n"
        "- Identify one real-world scenario where the exception case would apply."
    )


def generate_quiz(transcript: str, num_questions: int = 5) -> list:
    text = _ask_gemini(
        f"Create {num_questions} multiple-choice questions (4 options each, "
        f"mark the correct one) from this transcript, return as JSON list with "
        f"fields question, options, answer:\n\n{transcript}"
    )
    if text:
        try:
            return json.loads(text)
        except Exception:
            pass

    return [
        {
            "question": "What is the purpose of the foundational principle introduced in this lecture?",
            "options": [
                "It is an optional background topic",
                "It serves as the base layer that all further concepts build upon",
                "It only applies to advanced problems",
                "It replaces the need to study key terms"
            ],
            "answer": "It serves as the base layer that all further concepts build upon",
        },
        {
            "question": "What is the first step in the worked example demonstrated in the lecture?",
            "options": [
                "Calculate the final result immediately",
                "Select the formula before reading the problem",
                "Identify what is given in the problem",
                "Check for the exception case first"
            ],
            "answer": "Identify what is given in the problem",
        },
        {
            "question": "Which of the following best describes the 'exception case'?",
            "options": [
                "A simpler version of the standard rule",
                "The scenario where the standard rule does not apply",
                "An advanced topic covered in the next lecture",
                "A rule that only applies to primary variables"
            ],
            "answer": "The scenario where the standard rule does not apply",
        },
        {
            "question": "How many key terms were highlighted as essential before the exam?",
            "options": ["Two", "Four", "Five", "Three"],
            "answer": "Three",
        },
        {
            "question": "What should students do before the next class according to the lecture?",
            "options": [
                "Read ahead to the next chapter only",
                "Skip revision and attempt new problems",
                "Review notes and redo the worked example independently",
                "Only memorise the exception case"
            ],
            "answer": "Review notes and redo the worked example independently",
        },
    ]


def generate_flashcards(transcript: str, num_cards: int = 8) -> list:
    text = _ask_gemini(
        f"Create {num_cards} revision flashcards (term/definition pairs) from "
        f"this transcript, return as JSON list with fields front and back:\n\n{transcript}"
    )
    if text:
        try:
            return json.loads(text)
        except Exception:
            pass

    return [
        {
            "front": "What is the foundational principle?",
            "back": "The base concept that all further topics in this subject build upon. It must be understood before moving to advanced material."
        },
        {
            "front": "What are the three key terms from this lecture?",
            "back": "1. Core Definition  2. Variable Relationship  3. Exception Condition"
        },
        {
            "front": "What is the exception case?",
            "back": "The specific scenario where the standard rule does not apply. Always check for this in exam questions."
        },
        {
            "front": "Step 1 of the worked example",
            "back": "Identify what is given in the problem before doing anything else."
        },
        {
            "front": "Step 2 of the worked example",
            "back": "Select the correct method or formula that applies to the given information."
        },
        {
            "front": "Step 3 of the worked example",
            "back": "Calculate the result and verify that it makes logical sense."
        },
        {
            "front": "What is the relationship between primary and secondary variables?",
            "back": "The secondary variable is dependent on the primary variable. A change in the primary directly affects the secondary."
        },
        {
            "front": "What is the best way to prepare for the next class?",
            "back": "Re-read the core definition, redo the worked example without notes, and find a real-world example of the exception case."
        },
    ]


def answer_question(transcript: str, question: str) -> str:
    text = _ask_gemini(
        f"You are a helpful study assistant. Using ONLY the information in "
        f"this lecture transcript, answer the student's question clearly and "
        f"concisely. If the transcript doesn't cover it, say so.\n\n"
        f"Transcript:\n{transcript}\n\n"
        f"Question: {question}\n"
        f"Answer:"
    )
    if text:
        return text.strip()

    return (
        f"Based on this lecture, here is what's relevant to your question "
        f"'{question}':\n\n"
        f"The lecture covered the foundational principle, walked through a "
        f"three-step worked example (identify → select method → calculate and "
        f"verify), and highlighted three key terms: Core Definition, Variable "
        f"Relationship, and Exception Condition.\n\n"
        f"For a more precise answer grounded in your actual audio content, "
        f"add your Gemini API key at the top of models/gemini_model.py."
    )