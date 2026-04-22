from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/login")

def login():
    scope = "user-top-read%20user-read-private"
    url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={scope}"
        f"&show_dialog=true"
    )
    return RedirectResponse(url)

@app.get("/callback")
def callback(code: str = None, error: str = None):
    if error:
        return RedirectResponse("http://127.0.0.1:5500/index.html")
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
    access_token = tokens["access_token"]
    return RedirectResponse(f"http://127.0.0.1:5500/index.html?access_token={access_token}", status_code=302)

@app.get("/top-artists")
def top_artists(access_token: str):
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
    print(response.status_code, response.text)
    data = response.json()
    
    artists = []
    for artist in data["items"]:
        artists.append({
            "name": artist["name"],
            "image": artist["images"][0]["url"],
        })
    
    return artists