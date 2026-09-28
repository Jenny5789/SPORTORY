from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.routers.players import router as players_router


app = FastAPI(
    title="SPORTORY API",
    version="0.1.0"
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