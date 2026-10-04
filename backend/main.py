from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routers.players import router as players_router


app = FastAPI(
    title="SPORTORY API",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://sportory.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/images",
    StaticFiles(directory="data/player_images"),
    name="images"
)


app.include_router(players_router)


@app.get("/")
def root():
    return {
        "message": "SPORTORY API"
    }