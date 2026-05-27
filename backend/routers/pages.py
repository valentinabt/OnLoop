from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
def root():
    return FileResponse("/app/frontend/pages/login/login.html")

@router.get("/top-artists")
def top_artists_page():
    return FileResponse("/app/frontend/pages/top-artists/top-artists.html")