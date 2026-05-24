import pytest
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch
from backend.config import FRONTEND_URL


client = TestClient(app, follow_redirects=False)

def test_callback_error_parameter():
    response = client.get("/callback?error=access_denied&state=abc", cookies={"oauth_state": "abc"})
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"

def test_callback_without_code():
    response = client.get("/callback?code=456&state=abc", cookies={"oauth_state": "abc"})
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"

def test_callback_without_state():
    response = client.get("/callback?code=456", cookies={"oauth_state": "abc"})
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"

def test_callback_without_cookie():
    response = client.get("/callback?code=456&state=abc")
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"

def test_callback_missmatched_state():
    response = client.get("/callback?error=access_denied&state=abc", cookies={"oauth_state": "abcd"})
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"

@patch("backend.main.get_token", return_value=(None, "refresh_token"))
def test_callback_accesstoken_fails(mock_get_token):
    response = client.get("/callback?code=123&state=abc", cookies={"oauth_state": "abc"})
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"


@patch("backend.main.get_token", return_value=("access_token", None))
def test_callback_refreshtoken_fails(mock_get_token):
    response = client.get("/callback?code=123&state=abc", cookies={"oauth_state": "abc"})
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"

@patch("backend.main.get_token", return_value=(None, None))
def test_callback_token_fails(mock_get_token):
    response = client.get("/callback?code=123&state=abc", cookies={"oauth_state": "abc"})
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"

@patch("backend.main.create_session", return_value=None)
def test_callback_create_session_fails(mock_create_session):
    response = client.get("/callback?code=123&state=abc", cookies={"oauth_state": "abc"})
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"

@patch("backend.main.create_session", return_value="session_id")
@patch("backend.main.get_token", return_value=("access_token", "refresh_token"))
def test_callback_successful(mock_get_token, mock_create_session):
    response = client.get("/callback?code=123&state=abc", cookies={"oauth_state": "abc"})

    assert response.status_code == 302
    assert response.headers["location"].endswith("/top-artists")
    assert "session_id" in response.cookies
