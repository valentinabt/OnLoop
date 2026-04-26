import requests
import redis
import uuid
from backend.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

r = redis.Redis(host='localhost', port=6379, db=0)

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

def create_session(access_token: str):
    session_id = str(uuid.uuid4())  #crea un id
    r.setex(session_id, 3600, access_token) #asocia el id con el token y pone qpara que se expire en 1 hora
    return session_id

def get_token_from_session(session_id: str):
    token = r.get(session_id)
    if not token:
        return None
    return token.decode("utf-8")

def delete_session(session_id: str):
    r.delete(session_id)
    return None
