from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import CLIENT_ID, REDIRECT_URI
from backend.services.spotify import get_token, get_artists


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
   
    access_token = get_token(code)
    return RedirectResponse(f"http://127.0.0.1:5500/index.html?access_token={access_token}", status_code=302)


@app.get("/top-artists")
def top_artists(access_token: str):
 
   return get_artists(access_token)
    
