import json
import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def save_raw_to_db(player_id):
    player_id = player_id.strip().lower()

    # Overview Raw JSON 읽기
    with open(
        f"data/raw/{player_id}_overview.json",
        "r",
        encoding="utf-8"
    ) as file:
        raw_data = json.load(file)

    # Player ID 확인
    raw_player_id = raw_data["player_id"].lower()

    if player_id != raw_player_id:
        raise ValueError(
            f"Player ID 불일치: 입력={player_id}, Raw Data={raw_player_id}"
        )

    # PostgreSQL 연결
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    print("PostgreSQL 연결 성공")

    # raw_data 테이블에 저장
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

    conn.commit()

    print("Overview Raw Data DB 저장 성공")

    conn.close()


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID: "
    ).strip().lower()

    save_raw_to_db(player_id)