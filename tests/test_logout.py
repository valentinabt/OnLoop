import pytest
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch
from backend.config import FRONTEND_URL 

client = TestClient(app, follow_redirects=False)

def test_logout_with_no_session():
    response = client.get("/logout")
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"
    

@patch("backend.routers.auth.delete_session", side_effect=Exception("error"))
def test_logout_with_delete_session_exception(mock_delete_session):
    response = client.get("/logout", cookies={"session_id": "abc"})
    assert response.status_code == 307
    assert response.headers["location"] == f"{FRONTEND_URL}/?r=error"

@patch("backend.routers.auth.delete_session", return_value=None)
def test_logout_sucessfull(mock_delete_session):
    response = client.get("/logout", cookies={"session_id": "abc"})
    assert response.status_code == 302
    assert response.headers["location"] == f"{FRONTEND_URL}"
    assert "session_id" not in response.cookies


