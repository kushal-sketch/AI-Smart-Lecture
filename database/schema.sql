-- AI Smart Lecture Assistant — SQLite schema

CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT UNIQUE NOT NULL,
    email           TEXT UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS lectures (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER REFERENCES users(id),
    lecture_name    TEXT NOT NULL,
    audio_path      TEXT NOT NULL,
    language        TEXT DEFAULT 'en',
    status          TEXT DEFAULT 'uploaded',   -- uploaded -> transcribed -> processed -> done
    transcript_path TEXT,
    notes_path      TEXT,
    quiz_path       TEXT,
    flashcards_path TEXT,
    pdf_report_path TEXT,
    duration_seconds REAL,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS dashboard_stats (
    id                  INTEGER PRIMARY KEY CHECK (id = 1),
    total_lectures      INTEGER DEFAULT 0,
    total_notes         INTEGER DEFAULT 0,
    total_quizzes       INTEGER DEFAULT 0,
    total_flashcards    INTEGER DEFAULT 0
);

INSERT OR IGNORE INTO dashboard_stats (id, total_lectures, total_notes, total_quizzes, total_flashcards)
VALUES (1, 0, 0, 0, 0);
