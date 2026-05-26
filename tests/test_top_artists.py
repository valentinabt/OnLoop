import pytest
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch

client = TestClient(app, follow_redirects=False)

def test_top_artists_no_session():
    response = client.get("/api/top-artists?time_range=short_term")
    assert response.status_code == 200
    assert response.json() == {"error": "NO_SESSION"}

@patch("backend.main.get_access_token_from_session", return_value=None)
def test_top_artists_without_access_token(mock_get_access_token_from_session):
    response = client.get("/api/top-artists", cookies={"session_id": "abc"})
    assert response.status_code == 200
    assert response.json() == {"error": "NO_SESSION"}

@patch("backend.main.get_artists", return_value=None)
@patch("backend.main.get_access_token_from_session", return_value="access_token")
def test_top_artists_with_no_artists(mock_get_access_token_from_session, mock_get_artists):
    response = client.get("/api/top-artists?time_range=short_term", cookies={"session_id": "abc"})
    assert response.status_code == 200
    assert response.json() == {"error": "FAILED_TO_FETCH_ARTISTS"}

@patch("backend.main.get_artists", return_value=[{"name": "Artist1"}])
@patch("backend.main.get_access_token_from_session", return_value="access_token")
def test_top_artists_default_time_range(mock_get_access_token_from_session, mock_get_artists):
    response = client.get("/api/top-artists", cookies={"session_id": "abc"})
    assert response.status_code == 200
    assert response.json() == [{"name": "Artist1"}]
    mock_get_artists.assert_called_once_with("access_token", "short_term")
