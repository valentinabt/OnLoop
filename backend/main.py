from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import FRONTEND_URL
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="/app/frontend"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=["GET","POST"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(routers.auth.router)
app.include_router(api.router)
app.include_router(pages.router)