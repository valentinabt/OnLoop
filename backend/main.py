from fastapi import FastAPI, Response, Cookie
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import CLIENT_ID, REDIRECT_URI
from backend.services.spotify import get_token, get_artists, create_session, get_token_from_session, delete_session

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
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
    session_id = create_session(access_token)
    redirect = RedirectResponse("http://127.0.0.1:5500/index.html", status_code=302)
    redirect.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",   #agrego la cookie. Cuando se redirija se va a guardar en el navegador
        secure= False,
        
    )
    return redirect

    
@app.get("/top-artists")
def top_artists(session_id: str = Cookie(default=None)):  #busca la cookie llamada session_id. Si no hay, no pone nada
    if not session_id:
        return {"error": "no hay sesión activa"}  
    access_token = get_token_from_session(session_id)
    if not access_token:
        return {"error": "sesión expirada, volvé a loguearte"}
    return get_artists(access_token)

@app.get("/logout")

def logout(session_id: str = Cookie(default=None)):
    if not session_id:
        return {"error": "no hay sesión activa"}
    delete_session(session_id)
    redirect = RedirectResponse("http://127.0.0.1:5500/index.html", status_code=302)
    redirect.delete_cookie(key="session_id")
    return redirect

