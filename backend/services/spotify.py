import requests
from backend.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

SPOTIFY_TOP_URL = "https://api.spotify.com/v1/me/top/artists"

def get_token(code: str):
    try:
        response = requests.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            auth=(CLIENT_ID, CLIENT_SECRET),
        )
        response.raise_for_status()
    except requests.RequestException:
        return None, None
    
    try:
        tokens = response.json()
    except ValueError:
        return None, None

    if "access_token" not in tokens or "refresh_token" not in tokens:
        return None, None
    return tokens["access_token"], tokens["refresh_token"]   
    


def get_artists(access_token: str, time_range: str):

    try:
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
        if response.status_code == 401:
            return "TOKEN_EXPIRED"
        response.raise_for_status()
        
    except requests.RequestException:
        return None
    try:
        data = response.json()
    except ValueError:
        return None
    if "items" not in data:
        return None
    artists = []
    for artist in data["items"]:
        artists.append({
            "name": artist["name"],
            "image": artist["images"][0]["url"],
        })
    
    return artists
   
    
def refresh_access_token(refresh_token: str):
    try:
        response = requests.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "redirect_uri": REDIRECT_URI,
            },
            auth=(CLIENT_ID, CLIENT_SECRET),
        )
        response.raise_for_status()
    except requests.RequestException:
        return None, None
    
    try:
        tokens = response.json()
    except ValueError:
        return None, None

    if "access_token" not in tokens:
        return None, None
    if "refresh_token" not in tokens:
        tokens["refresh_token"] = refresh_token
    return tokens["access_token"], tokens["refresh_token"]   
    