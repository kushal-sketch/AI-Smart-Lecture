# API Documentation

LectureMind is server-rendered, but its routes can also be called directly
(e.g. from a script or future SPA front-end).

| Route | Method | Description |
|---|---|---|
| `/` | GET | Homepage with dashboard summary + recent lectures |
| `/upload` | GET | Upload form |
| `/upload` | POST | Upload an audio file (`audio_file`, `lecture_name`, `language`) |
| `/process/<lecture_id>` | GET | Runs transcription → notes → quiz → flashcards |
| `/transcript/<lecture_id>` | GET | View transcript |
| `/notes/<lecture_id>` | GET | View study notes |
| `/quiz/<lecture_id>` | GET | View quiz |
| `/flashcards/<lecture_id>` | GET | View flashcards |
| `/history` | GET | All processed lectures |
| `/dashboard` | GET | Analytics dashboard |
| `/report/<lecture_id>` | GET | Report download page |
| `/report/<lecture_id>/download` | GET | Streams the generated PDF |
| `/translate/<lecture_id>?lang=hi` | GET (AJAX) | Returns `{ "translated": "..." }` JSON |

## Data model

`lectures` table (see `database/schema.sql`):

```
id, lecture_name, audio_path, language, status,
transcript_path, notes_path, quiz_path, flashcards_path, pdf_report_path,
duration_seconds, created_at, updated_at
```
