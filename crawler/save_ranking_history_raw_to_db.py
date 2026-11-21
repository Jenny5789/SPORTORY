"""순위 이력(Ranking History) 원본 JSON을 raw_data 테이블에 저장.

입력: data/raw/{player_id}_ranking_history_response.json → 출력: raw_data 테이블 (source_type=player_ranking_history)
실행: python crawler/save_ranking_history_raw_to_db.py
"""

import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import psycopg
from dotenv import load_dotenv


# 1. 환경변수 읽기
load_dotenv()


def save_ranking_history_raw_to_db(player_id):
    """선수 순위 이력 응답 원본을 출처, 수집 시각과 함께 raw_data에 INSERT."""
    player_id = player_id.strip().lower()

    # 2. 해당 선수의 Ranking History Raw JSON 읽기
    with open(
        f"data/raw/{player_id}_ranking_history_response.json",
        "r",
        encoding="utf-8"
    ) as file:
        ranking_data = json.load(file)


    # 3. Source URL 생성
    # 응답 파일에 URL 미포함, API 경로로 재구성
    source_url = (
        f"https://www.atptour.com/en/-/www/rank/history/{player_id}?v=1"
    )


    # 4. PostgreSQL 연결
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    print("PostgreSQL 연결 성공")


    # 5. raw_data 테이블에 원본 저장
    # ON CONFLICT 없이 INSERT
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
                "ATP",
                "player_ranking_history",
                player_id,
                source_url,
                datetime.now(ZoneInfo("Asia/Seoul")),
                "manual_devtools_poc",
                json.dumps(ranking_data, ensure_ascii=False)
            )
        )


    # 6. 저장 확정
    conn.commit()
    conn.close()

    print("Ranking History Raw Data DB 저장 성공")


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID를 입력하세요: "
    ).strip().lower()

    save_ranking_history_raw_to_db(player_id)