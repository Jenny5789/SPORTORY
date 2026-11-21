"""SPORTORY FastAPI 앱 진입점.

CORS 설정, 선수 이미지 정적 경로(/images) 등록, /players 라우터 연결.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routers.players import router as players_router


app = FastAPI(
    title="SPORTORY API",
    version="0.1.0"
)


# 프론트엔드 출처만 허용: 로컬 Vite 개발 서버(5173, 5174), Vercel 배포 도메인
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://sportory.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 로컬 data/player_images 폴더를 /images 경로로 제공 (실행 위치 기준 상대 경로)
app.mount(
    "/images",
    StaticFiles(directory="data/player_images"),
    name="images"
)


app.include_router(players_router)


@app.get("/")
def root():
    """GET /: API 이름 메시지 반환."""
    return {
        "message": "SPORTORY API"
    }