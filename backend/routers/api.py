from fastapi import FastAPI, Cookie, Query
from backend.services.sessions import get_access_token_from_session
from backend.services.spotify import get_artists

router = FastAPI()

@router.get("/api/top-artists")
def top_artists(session_id: str = Cookie(default=None), time_range: str = Query(default="short_term")): 
    if not session_id:
        return {"error": "NO_SESSION"}  
    access_token = get_access_token_from_session(session_id)
    if not access_token:
        return {"error": "NO_SESSION"}
    artists = get_artists(access_token, time_range)
    if artists == "TOKEN_EXPIRED":
        return {"error": "SESSION_EXPIRED"}
    if artists is None:
        return {"error": "FAILED_TO_FETCH_ARTISTS"}
    return artists

