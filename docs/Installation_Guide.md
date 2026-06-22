# Installation Guide

1. Clone or unzip the project.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Enable real AI — see the "Going live with real AI" section
   in the root `README.md`.
5. Run the app:
   ```bash
   python app.py
   ```
6. Visit `http://127.0.0.1:5000`.

The SQLite database and all `generated/` folders are created automatically
on first run.
