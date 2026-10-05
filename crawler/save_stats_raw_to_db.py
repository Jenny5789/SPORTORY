import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import psycopg
from dotenv import load_dotenv


# 1. .env 파일 읽기
load_dotenv()


def save_stats_raw_to_db(player_id):
    player_id = player_id.strip().lower()

    # 2. 해당 선수의 ATP Stats Raw JSON 읽기
    with open(
        f"data/raw/{player_id}_stats_response.json",
        "r",
        encoding="utf-8"
    ) as file:
        stats_data = json.load(file)


    # 3. 전달받은 Player ID와 원본 데이터의 Player ID 확인
    raw_player_id = stats_data["Stats"]["PlayerId"].lower()

    if player_id != raw_player_id:
        raise ValueError(
            f"Player ID 불일치: 입력={player_id}, Raw Data={raw_player_id}"
        )


    # 4. Source URL 생성
    source_url = (
        f"https://www.atptour.com/en/-/www/stats/{player_id}/all/all?v=1"
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


    # 6. raw_data 테이블에 Stats 원본 저장
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
                "player_stats",
                player_id,
                source_url,
                datetime.now(ZoneInfo("Asia/Seoul")),
                "manual_devtools_poc",
                json.dumps(stats_data, ensure_ascii=False)
            )
        )


    # 7. 저장 확정
    conn.commit()
    conn.close()

    print("Stats Raw Data DB 저장 성공")


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID를 입력하세요: "
    ).strip().lower()

    save_stats_raw_to_db(player_id)