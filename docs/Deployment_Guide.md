# Deployment Guide

## Render

1. Push the project to a GitHub repo.
2. Create a new **Web Service** on Render, pointing at the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add `GEMINI_API_KEY` (and any others) under Environment Variables.
6. Note: Render's free tier has an ephemeral filesystem — uploaded audio and
   generated files won't persist across deploys/restarts. Use a persistent
   disk or external storage (S3, etc.) for production use.

## Railway

1. Push the project to a GitHub repo.
2. Create a new project on Railway, import the repo.
3. Railway auto-detects Python; set the start command to:
   `gunicorn app:app`
4. Add environment variables (`GEMINI_API_KEY`, etc.) in the Railway dashboard.
5. Attach a Railway volume if you need uploaded/generated files to persist.

## Production checklist

- [ ] Set a real `SECRET_KEY` via environment variable
- [ ] Set `FLASK_DEBUG=0`
- [ ] Add `gunicorn` to `requirements.txt`
- [ ] Configure persistent storage for `uploads/` and `generated/`
- [ ] Consider moving SQLite to a managed Postgres instance for multi-user scale
