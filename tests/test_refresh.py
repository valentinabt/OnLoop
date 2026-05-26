import pytest
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch


client = TestClient(app, follow_redirects=False)

def test_refresh_with_no_session():
    response = client.post("/refresh")
    assert response.status_code == 200
    assert response.json() == {"error": "NO_SESSION"}

@patch("backend.main.get_refresh_token_from_session", return_value=None)
def test_refresh_with_no_refresh_token(mock_get_refresh_token_from_session):
    response = client.post("/refresh", cookies={"session_id": "abc"})
    assert response.status_code == 200
    assert response.json() == {"error": "NO_SESSION"}

@patch("backend.main.refresh_access_token", return_value=("access_token",None))
@patch("backend.main.get_refresh_token_from_session", return_value="refresh_token")
def test_refresh_with_no_new_refresh_token(mock_get_refresh_token_from_session, mock_refresh_access_token):
    response = client.post("/refresh", cookies={"session_id": "abc"})
    assert response.status_code == 200
    assert response.json() == {"error": "FAILED_TO_REFRESH"}

@patch("backend.main.refresh_access_token", return_value=(None,"new_refresh_token"))
@patch("backend.main.get_refresh_token_from_session", return_value="refresh_token")
def test_refresh_with_no_new_access_token(mock_get_refresh_token_from_session, mock_refresh_access_token):
    response = client.post("/refresh", cookies={"session_id": "abc"})
    assert response.status_code == 200
    assert response.json() == {"error": "FAILED_TO_REFRESH"}

@patch("backend.main.refresh_access_token", return_value=(None, None))
@patch("backend.main.get_refresh_token_from_session", return_value="refresh_token")
def test_refresh_with_no_refresh_tokens(mock_get_refresh_token_from_session, mock_refresh_access_token):
    response = client.post("/refresh", cookies={"session_id": "abc"})
    assert response.status_code == 200
    assert response.json() == {"error": "FAILED_TO_REFRESH"}

@patch("backend.main.update_session", return_value=None)
@patch("backend.main.refresh_access_token", return_value=("access_token","new_refresh_token"))
@patch("backend.main.get_refresh_token_from_session", return_value="refresh_token")
def test_refresh_with_no_success(mock_get_refresh_token_from_session, mock_refresh_access_token, mock_update_session):
    response = client.post("/refresh", cookies={"session_id": "abc"})
    assert response.status_code == 200
    assert response.json() == {"error": "FAILED_TO_REFRESH"}

@patch("backend.main.update_session", return_value="abc")
@patch("backend.main.refresh_access_token", return_value=("access_token", "new_refresh_token"))
@patch("backend.main.get_refresh_token_from_session", return_value="refresh_token")
def test_refresh_with_success(mock_get_refresh_token_from_session, mock_refresh_access_token, mock_update_session):
    response = client.post("/refresh", cookies={"session_id": "abc"})
    mock_update_session.assert_called_once_with("abc", "access_token", "new_refresh_token")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

