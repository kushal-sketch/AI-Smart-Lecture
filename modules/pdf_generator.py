"""
pdf_generator.py
Builds a single PDF report containing transcript, notes, quiz and
flashcards for a lecture, using ReportLab.
"""
import json
from pathlib import Path
from config import Config

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
)


def _styles():
    base = getSampleStyleSheet()
    base.add(ParagraphStyle(name="LectureTitle", fontSize=22, leading=26,
                             textColor=colors.HexColor("#1F2A44"), spaceAfter=18))
    base.add(ParagraphStyle(name="SectionHeading", fontSize=15, leading=18,
                             textColor=colors.HexColor("#C77B2B"), spaceBefore=12, spaceAfter=10))
    base.add(ParagraphStyle(name="Body", fontSize=10.5, leading=15,
                             textColor=colors.HexColor("#2B2B2B")))
    return base


def build_pdf_report(lecture: dict) -> str:
    Config.PDF_FOLDER.mkdir(parents=True, exist_ok=True)
    out_path = Config.PDF_FOLDER / f"lecture_{lecture['id']:03d}_report.pdf"

    styles = _styles()
    doc = SimpleDocTemplate(str(out_path), pagesize=A4,
                             topMargin=2.2*cm, bottomMargin=2.2*cm,
                             leftMargin=2*cm, rightMargin=2*cm)
    story = []

    story.append(Paragraph("AI Smart Lecture Assistant — Report", styles["LectureTitle"]))
    story.append(Paragraph(lecture.get("lecture_name", "Untitled lecture"), styles["Body"]))
    story.append(Spacer(1, 0.6*cm))

    # Transcript
    if lecture.get("transcript_path"):
        story.append(Paragraph("Transcript", styles["SectionHeading"]))
        text = Path(lecture["transcript_path"]).read_text(encoding="utf-8")
        story.append(Paragraph(text.replace("\n", "<br/>"), styles["Body"]))
        story.append(PageBreak())

    # Notes
    if lecture.get("notes_path"):
        story.append(Paragraph("Study Notes", styles["SectionHeading"]))
        text = Path(lecture["notes_path"]).read_text(encoding="utf-8")
        story.append(Paragraph(text.replace("\n", "<br/>"), styles["Body"]))
        story.append(PageBreak())

    # Quiz
    if lecture.get("quiz_path"):
        story.append(Paragraph("Quiz", styles["SectionHeading"]))
        quiz = json.loads(Path(lecture["quiz_path"]).read_text(encoding="utf-8"))
        for i, q in enumerate(quiz, 1):
            story.append(Paragraph(f"{i}. {q['question']}", styles["Body"]))
            for opt in q.get("options", []):
                story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&bull; {opt}", styles["Body"]))
            story.append(Spacer(1, 0.25*cm))
        story.append(PageBreak())

    # Flashcards
    if lecture.get("flashcards_path"):
        story.append(Paragraph("Flashcards", styles["SectionHeading"]))
        cards = json.loads(Path(lecture["flashcards_path"]).read_text(encoding="utf-8"))
        data = [["Front", "Back"]] + [[c["front"], c["back"]] for c in cards]
        table = Table(data, colWidths=[7*cm, 7*cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F2A44")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 9.5),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F4EE")]),
        ]))
        story.append(table)

    doc.build(story)
    return str(out_path)
