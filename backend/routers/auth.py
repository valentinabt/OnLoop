from fastapi import FastAPI, Cookie
from fastapi.responses import RedirectResponse
from backend.config import CLIENT_ID, REDIRECT_URI, FRONTEND_URL
from backend.services.spotify import get_token, refresh_access_token
from backend.services.sessions import create_session, get_refresh_token_from_session, delete_session, update_session
import secrets

router = FastAPI()

@router.get("/login")
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

@router.get("/callback")
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

 

@router.get("/logout")
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

@router.post("/refresh")
def refresh(session_id: str = Cookie(default=None)):
    if not session_id:
        return {"error": "NO_SESSION"}
    
    refresh_token = get_refresh_token_from_session(session_id)
    if not refresh_token:
        return {"error": "NO_SESSION"}
    
    access_token, refresh_token = refresh_access_token(refresh_token)
    if not access_token or not refresh_token:
        return {"error": "FAILED_TO_REFRESH"}
    
    success = update_session(session_id, access_token, refresh_token)
    if not success:
        return {"error": "FAILED_TO_REFRESH"}
    
    return {"ok": True}
