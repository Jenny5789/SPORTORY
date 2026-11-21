"""PostgreSQL(Supabase) 연결 생성 모듈."""

import os

import psycopg
from dotenv import load_dotenv


# DB 접속 정보는 코드에 두지 않고 .env 환경 변수에서 로드
load_dotenv()


def get_connection():
    """환경 변수(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD) 기반 psycopg 연결 반환."""
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )