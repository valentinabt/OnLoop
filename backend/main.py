from fastapi import FastAPI, Cookie, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import CLIENT_ID, REDIRECT_URI, FRONTEND_URL
from backend.services.spotify import get_token, get_artists, create_session, get_token_from_session, delete_session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid


app = FastAPI()


app.mount("/static", StaticFiles(directory="/app/frontend"), name="static")
@app.get("/")
def root():
   return FileResponse("/app/frontend/index.html")

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
    state = str(uuid.uuid4())  
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
def callback(code: str = None, error: str = None,state: str = None, state_cookie: str = Cookie(default=None)):
    if error:
        return RedirectResponse(f"{FRONTEND_URL}")
   
    elif not code:
        return RedirectResponse(f"{FRONTEND_URL}")
    
    elif not state or state != state_cookie:
        return RedirectResponse(f"{FRONTEND_URL}")
    
    
    access_token = get_token(code)
    session_id = create_session(access_token)
    redirect = RedirectResponse(f"{FRONTEND_URL}", status_code=302)
    redirect.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",   
        secure=True,
        
    )
    return redirect

    
@app.get("/top-artists")
def top_artists(session_id: str = Cookie(default=None), time_range: str = Query(default="short_term")): 
    if not session_id:
        return {"error": "no hay sesión activa"}  
    access_token = get_token_from_session(session_id)
    if not access_token:
        return {"error": "sesión expirada, volvé a loguearte"}
    return get_artists(access_token, time_range)

@app.get("/logout")
def logout(session_id: str = Cookie(default=None)):
    if not session_id:
        return {"error": "no hay sesión activa"}
    delete_session(session_id)
    redirect = RedirectResponse(f"{FRONTEND_URL}", status_code=302)
    redirect.delete_cookie(key="session_id")
    return redirect

