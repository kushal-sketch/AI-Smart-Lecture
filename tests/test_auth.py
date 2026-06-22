"""test_auth.py — basic checks for signup / login / logout."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app as app_module


def test_signup_then_protected_route_accessible():
    client = app_module.app.test_client()
    response = client.post("/signup", data={
        "username": "auth_test_user",
        "email": "auth_test_user@example.com",
        "password": "secret123",
        "confirm_password": "secret123",
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.get("/upload")
    assert response.status_code == 200


def test_signup_rejects_mismatched_passwords():
    client = app_module.app.test_client()
    response = client.post("/signup", data={
        "username": "mismatch_user",
        "email": "mismatch_user@example.com",
        "password": "secret123",
        "confirm_password": "different",
    }, follow_redirects=True)
    assert b"Passwords don" in response.data


def test_login_rejects_wrong_password():
    client = app_module.app.test_client()
    client.post("/signup", data={
        "username": "wrongpass_user",
        "email": "wrongpass_user@example.com",
        "password": "secret123",
        "confirm_password": "secret123",
    })
    client.get("/logout")
    response = client.post("/login", data={
        "username": "wrongpass_user",
        "password": "incorrect",
    }, follow_redirects=True)
    assert b"Incorrect username or password" in response.data
