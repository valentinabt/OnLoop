from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
def root():
   return FileResponse("/app/frontend/login.html")

@router.get("/top-artists")
def top_artists_page():
    return FileResponse("/app/frontend/top-artists.html")