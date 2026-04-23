import requests
from backend.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

def get_token(code: str):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    tokens = response.json()
    return tokens["access_token"]


def get_artists(access_token: str):
    response = requests.get(
        "https://api.spotify.com/v1/me/top/artists",
        params={
            "time_range": "short_term",
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