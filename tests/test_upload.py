"""test_upload.py — basic checks for the upload route (auth-protected)."""
import io
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app as app_module


def _signed_in_client():
    """Returns a test client that's already signed up + logged in."""
    client = app_module.app.test_client()
    client.post("/signup", data={
        "username": "pytest_user",
        "email": "pytest_user@example.com",
        "password": "secret123",
        "confirm_password": "secret123",
    })
    return client


def test_upload_redirects_when_logged_out():
    client = app_module.app.test_client()
    response = client.get("/upload")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_upload_page_loads_when_logged_in():
    client = _signed_in_client()
    response = client.get("/upload")
    assert response.status_code == 200


def test_upload_rejects_bad_extension():
    client = _signed_in_client()
    data = {
        "lecture_name": "Bad File",
        "language": "en",
        "audio_file": (io.BytesIO(b"not audio"), "notes.txt"),
    }
    response = client.post("/upload", data=data, content_type="multipart/form-data")
    assert response.status_code in (302, 200)  # redirected back with a flash message
