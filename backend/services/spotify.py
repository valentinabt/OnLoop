import requests
import redis
import uuid
from backend.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password= REDIS_PASSWORD)

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

def create_session(access_token: str):
    session_id = str(uuid.uuid4())  
    r.setex(session_id, 3600, access_token) 
    return session_id

def get_token_from_session(session_id: str):
    token = r.get(session_id)
    if not token:
        return None
    return token.decode("utf-8")

def delete_session(session_id: str):
    r.delete(session_id)
    
