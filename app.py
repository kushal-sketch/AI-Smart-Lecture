"""
app.py
AI Smart Lecture Assistant — Flask entry point.

Run with:
    python app.py
Then open http://127.0.0.1:5000
"""
import os
from pathlib import Path
from flask import (
    Flask, render_template, request, redirect, url_for, flash,
    send_file, abort, jsonify
)
from werkzeug.utils import secure_filename
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)

from config import Config
from database.database_manager import DatabaseManager
from modules.auth_manager import User

from modules.speech_to_text import process_audio_to_transcript
from modules.notes_generator import generate_notes_from_transcript
from modules.quiz_generator import generate_quiz_from_transcript
from modules.flashcard_generator import generate_flashcards_from_transcript
from modules.translator import translate_content
from modules.pdf_generator import build_pdf_report
from modules.history_manager import get_history
from modules.dashboard_manager import get_dashboard_data
from modules.qa_manager import ask_about_lecture

import json
import markdown as md_lib

app = Flask(__name__)
app.config.from_object(Config)
db = DatabaseManager()
@app.template_filter('markdown')
def render_markdown(text):
    return md_lib.markdown(text, extensions=['extra'])

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access that page."
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(user_id):
    row = db.get_user_by_id(int(user_id))
    return User(row) if row else None


for folder in [
    Config.UPLOAD_FOLDER, Config.TEMP_FOLDER, Config.TRANSCRIPT_FOLDER,
    Config.NOTES_FOLDER, Config.QUIZ_FOLDER, Config.FLASHCARD_FOLDER, Config.PDF_FOLDER,
]:
    folder.mkdir(parents=True, exist_ok=True)


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_AUDIO_EXTENSIONS


def _owned_lecture_or_404(lecture_id: int):
    """Fetches a lecture and aborts 404 if it doesn't exist or belongs to
    someone else — keeps each user's lectures private."""
    lecture = db.get_lecture(lecture_id)
    if not lecture or lecture.get("user_id") != current_user.id:
        abort(404)
    return lecture


# ---------------------------------------------------------------- auth --

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    if not username or not email or not password:
        flash("All fields are required.", "error")
        return redirect(url_for("signup"))

    if password != confirm:
        flash("Passwords don't match.", "error")
        return redirect(url_for("signup"))

    if len(password) < 6:
        flash("Password must be at least 6 characters.", "error")
        return redirect(url_for("signup"))

    if db.get_user_by_username(username):
        flash("That username is already taken.", "error")
        return redirect(url_for("signup"))

    if db.get_user_by_email(email):
        flash("An account with that email already exists.", "error")
        return redirect(url_for("signup"))

    user_id = db.create_user(username, email, User.hash_password(password))
    user = User(db.get_user_by_id(user_id))
    login_user(user)
    flash(f"Welcome, {username}! Your account has been created.", "success")
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    row = db.get_user_by_username(username)
    user = User(row) if row else None

    if not user or not user.check_password(password):
        flash("Incorrect username or password.", "error")
        return redirect(url_for("login"))

    login_user(user)
    flash(f"Welcome back, {user.username}!", "success")
    next_page = request.args.get("next")
    return redirect(next_page or url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for("login"))


# ---------------------------------------------------------------- routes --

@app.route("/")
def index():
    user_id = current_user.id if current_user.is_authenticated else None
    data = get_dashboard_data(db, user_id=user_id)
    return render_template("index.html", stats=data["stats"], recent=data["recent_lectures"])


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "GET":
        return render_template("upload.html", languages=Config.SUPPORTED_LANGUAGES)

    file = request.files.get("audio_file")
    lecture_name = request.form.get("lecture_name", "").strip()
    language = request.form.get("language", "en")

    if not file or file.filename == "":
        flash("Please choose an audio file (.mp3 or .wav).", "error")
        return redirect(url_for("upload"))

    if not _allowed_file(file.filename):
        flash("Unsupported file type. Use .mp3, .wav or .m4a.", "error")
        return redirect(url_for("upload"))

    filename = secure_filename(file.filename)
    save_path = Config.UPLOAD_FOLDER / filename
    file.save(save_path)

    if not lecture_name:
        lecture_name = Path(filename).stem.replace("_", " ").title()

    lecture_id = db.create_lecture(lecture_name, str(save_path), language=language, user_id=current_user.id)

    return redirect(url_for("process_lecture", lecture_id=lecture_id))


@app.route("/process/<int:lecture_id>")
@login_required
def process_lecture(lecture_id):
    """Runs the full pipeline: transcript -> notes -> quiz -> flashcards."""
    lecture = _owned_lecture_or_404(lecture_id)

    transcript_path = process_audio_to_transcript(
        lecture["audio_path"], lecture_id, language=lecture["language"]
    )
    notes_path = generate_notes_from_transcript(transcript_path, lecture_id)
    quiz_path = generate_quiz_from_transcript(transcript_path, lecture_id)
    flashcards_path = generate_flashcards_from_transcript(transcript_path, lecture_id)

    db.update_lecture(
        lecture_id,
        status="done",
        transcript_path=transcript_path,
        notes_path=notes_path,
        quiz_path=quiz_path,
        flashcards_path=flashcards_path,
    )
    db.increment_stat("total_notes")
    db.increment_stat("total_quizzes")
    db.increment_stat("total_flashcards")

    flash(f"'{lecture['lecture_name']}' processed successfully!", "success")
    return redirect(url_for("notes_page", lecture_id=lecture_id))


@app.route("/transcript/<int:lecture_id>")
@login_required
def transcript_page(lecture_id):
    lecture = _owned_lecture_or_404(lecture_id)
    if not lecture.get("transcript_path"):
        abort(404)
    text = Path(lecture["transcript_path"]).read_text(encoding="utf-8")
    return render_template("transcript.html", lecture=lecture, transcript=text)


@app.route("/notes/<int:lecture_id>")
@login_required
def notes_page(lecture_id):
    lecture = _owned_lecture_or_404(lecture_id)
    if not lecture.get("notes_path"):
        abort(404)
    text = Path(lecture["notes_path"]).read_text(encoding="utf-8")
    return render_template("notes.html", lecture=lecture, notes=text)


@app.route("/quiz/<int:lecture_id>")
@login_required
def quiz_page(lecture_id):
    lecture = _owned_lecture_or_404(lecture_id)
    if not lecture.get("quiz_path"):
        abort(404)
    quiz = json.loads(Path(lecture["quiz_path"]).read_text(encoding="utf-8"))
    return render_template("quiz.html", lecture=lecture, quiz=quiz)


@app.route("/flashcards/<int:lecture_id>")
@login_required
def flashcards_page(lecture_id):
    lecture = _owned_lecture_or_404(lecture_id)
    if not lecture.get("flashcards_path"):
        abort(404)
    cards = json.loads(Path(lecture["flashcards_path"]).read_text(encoding="utf-8"))
    return render_template("flashcards.html", lecture=lecture, cards=cards)


@app.route("/history")
@login_required
def history_page():
    lectures = get_history(db, user_id=current_user.id)
    return render_template("history.html", lectures=lectures)


@app.route("/dashboard")
@login_required
def dashboard_page():
    data = get_dashboard_data(db, user_id=current_user.id)
    return render_template("dashboard.html", stats=data["stats"], recent=data["recent_lectures"])


@app.route("/report/<int:lecture_id>")
@login_required
def report_page(lecture_id):
    lecture = _owned_lecture_or_404(lecture_id)
    return render_template("report.html", lecture=lecture)


@app.route("/report/<int:lecture_id>/download")
@login_required
def download_report(lecture_id):
    lecture = _owned_lecture_or_404(lecture_id)
    pdf_path = build_pdf_report(lecture)
    db.update_lecture(lecture_id, pdf_report_path=pdf_path)
    return send_file(pdf_path, as_attachment=True, download_name=Path(pdf_path).name)


@app.route("/translate/<int:lecture_id>")
@login_required
def translate_notes(lecture_id):
    """AJAX endpoint used by notes.html to translate notes on the fly."""
    target = request.args.get("lang", "en")
    lecture = _owned_lecture_or_404(lecture_id)
    if not lecture.get("notes_path"):
        abort(404)
    text = Path(lecture["notes_path"]).read_text(encoding="utf-8")
    translated = translate_content(text, target)
    return jsonify({"translated": translated})


@app.route("/ask/<int:lecture_id>", methods=["POST"])
@login_required
def ask_ai(lecture_id):
    """AJAX endpoint used by notes.html — answers a question grounded in
    this lecture's own transcript."""
    lecture = _owned_lecture_or_404(lecture_id)
    if not lecture.get("transcript_path"):
        abort(404)

    question = (request.get_json(silent=True) or {}).get("question", "").strip()
    if not question:
        return jsonify({"error": "Please type a question."}), 400

    answer = ask_about_lecture(lecture["transcript_path"], question)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
