import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app, follow_redirects=False)

def test_login_redirects_to_spotify():
    response = client.get("/login")
    assert response.status_code == 307
    assert response.headers["location"].startswith("https://accounts.spotify.com/authorize")

def test_login_sets_oauth_state_cookie():
    response = client.get("/login")
    assert "oauth_state" in response.cookies

def test_login_state_is_unique():
    response1 = client.get("/login")
    response2 = client.get("/login")
    assert response1.cookies["oauth_state"] != response2.cookies["oauth_state"]