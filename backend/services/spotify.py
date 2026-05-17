import requests
from backend.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI



SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

SPOTIFY_TOP_URL = "https://api.spotify.com/v1/me/top/artists"

def get_token(code: str):
    response = requests.post(
        SPOTIFY_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    tokens = response.json()
    return tokens["access_token"]


def get_artists(access_token: str, time_range: str):
    response = requests.get(
        SPOTIFY_TOP_URL,
        params={
            "time_range": time_range,
            "limit": 10
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    data = response.json()
    
    artists = []
    for artist in data["items"]:
        artists.append({
            "name": artist["name"],
            "image": artist["images"][0]["url"],
        })
    
    return artists

    
