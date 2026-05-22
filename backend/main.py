from fastapi import FastAPI, Cookie, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import CLIENT_ID, REDIRECT_URI, FRONTEND_URL
from backend.services.spotify import get_artists, get_token, get_refresh_token, refresh_access_token
from backend.services.sessions import create_session, get_access_token_from_session, delete_session, update_session

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import secrets


app = FastAPI()


app.mount("/static", StaticFiles(directory="/app/frontend"), name="static")
@app.get("/")
def root():
   return FileResponse("/app/frontend/login.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=["GET","POST"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/login")

def login():
    scope = "user-top-read%20user-read-private"
    state = secrets.token_urlsafe(32)  
    redirect = RedirectResponse(
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state={state}"
        f"&scope={scope}"
        f"&show_dialog=true"
    )
    
    redirect.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        samesite="lax",   
        secure=True,
        
    )
    return redirect

@app.get("/callback")
def callback(code: str = None, error: str = None,state: str = None, oauth_state: str = Cookie(default=None)):
    
    if error:
        return RedirectResponse(f"{FRONTEND_URL}/?r=error")
   
    elif not code:
            return RedirectResponse(f"{FRONTEND_URL}/?r=error")
    
    elif not state or state != oauth_state:
        return RedirectResponse(f"{FRONTEND_URL}/?r=error")
    
    access_token, refresh_token = get_token(code)
    if access_token is None or refresh_token is None:
        return RedirectResponse(f"{FRONTEND_URL}/?r=error")
    
    session_id = create_session(access_token, refresh_token)
    if session_id is None:
        return RedirectResponse(f"{FRONTEND_URL}/r=error")
    

    redirect = RedirectResponse(f"{FRONTEND_URL}/top-artists", status_code=302)
    redirect.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",   
        secure=True,
        
    )
    return redirect

    
@app.get("/api/top-artists")
def top_artists(session_id: str = Cookie(default=None), time_range: str = Query(default="short_term")): 
    if not session_id:
        return {"error": "NO_SESSION"}  
    access_token = get_access_token_from_session(session_id)
    if not access_token:
        return {"error": "SESSION_EXPIRED"}
    artists = get_artists(access_token, time_range)
    if artists is None:
        return {"error": "FAILED_TO_FETCH_ARTISTS"}
    return artists

@app.get("/top-artists")
def top_artists_page():
    return FileResponse("/app/frontend/top-artists.html")

@app.get("/logout")
def logout(session_id: str = Cookie(default=None)):
    if not session_id:
        return RedirectResponse(f"{FRONTEND_URL}/?r=error")
    try:
        delete_session(session_id)
    except Exception:
        return RedirectResponse(f"{FRONTEND_URL}/?r=error")
    
    redirect = RedirectResponse(f"{FRONTEND_URL}", status_code=302)
    redirect.delete_cookie(key="session_id")
    return redirect

@app.get("/refresh")
def refresh(session_id: str = Cookie(default=None)):
    if not session_id:
        return {"error": "NO_SESSION"}
    
    refresh_token = get_refresh_token(session_id)
    if not refresh_token:
        return {"error": "NO_SESSION"}
    
    access_token, refresh_token = refresh_access_token(refresh_token)
    if not access_token or not refresh_token:
        return {"error": "FAILED_TO_REFRESH"}
    
    success = update_session(session_id, access_token, refresh_token)
    if not success:
        return {"error": "FAILED_TO_REFRESH"}
    
    return {"ok": True}
