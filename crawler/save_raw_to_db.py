import json
import os

import psycopg
from dotenv import load_dotenv


# 1. .env 파일 읽기
load_dotenv()


# 2. 저장할 선수의 ATP Player ID 입력
player_id = input("ATP Player ID를 입력하세요: ").strip().lower()


# 3. 해당 선수의 Overview Raw JSON 읽기
with open(
    f"data/raw/{player_id}_overview.json",
    "r",
    encoding="utf-8"
) as file:
    raw_data = json.load(file)


# 4. 입력한 Player ID와 Raw Data의 Player ID 확인
raw_player_id = raw_data["player_id"].lower()

if player_id != raw_player_id:
    raise ValueError(
        f"Player ID 불일치: 입력={player_id}, Raw Data={raw_player_id}"
    )


# 5. PostgreSQL 연결
conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

print("PostgreSQL 연결 성공")


# 6. raw_data 테이블에 저장
with conn.cursor() as cur:
    cur.execute(
        """
        INSERT INTO raw_data (
            source,
            source_type,
            source_player_id,
            source_url,
            saved_at,
            collection_method,
            raw_json
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            raw_data["source"],
            raw_data["source_type"],
            raw_data["player_id"],
            raw_data["source_url"],
            raw_data["saved_at"],
            raw_data["collection_method"],
            json.dumps(raw_data, ensure_ascii=False)
        )
    )


# 7. 저장 확정
conn.commit()

print("Raw Data DB 저장 성공")

conn.close()