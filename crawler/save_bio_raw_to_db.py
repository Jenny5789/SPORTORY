import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


load_dotenv()


def save_bio_raw_to_db(player_id):
    player_id = player_id.strip().lower()

    file_path = Path("data/raw") / f"{player_id}_bio.json"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Bio Raw 파일을 찾을 수 없습니다: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    if raw_data.get("player_id") != player_id:
        raise ValueError(
            f"입력한 player_id({player_id})와 "
            f"Raw Data의 player_id({raw_data.get('player_id')})가 다릅니다."
        )

    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
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
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    raw_data["source"],
                    raw_data["source_type"],
                    raw_data["player_id"],
                    raw_data["source_url"],
                    raw_data["saved_at"],
                    raw_data["collection_method"],
                    json.dumps(
                        raw_data["data"],
                        ensure_ascii=False
                    )
                )
            )

        connection.commit()

        print("\nBio Raw Data DB 저장 완료")
        print("Player ID:", player_id)
        print("Source Type:", raw_data["source_type"])
        print(
            "Collection Method:",
            raw_data["collection_method"]
        )

    finally:
        connection.close()


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID: "
    ).strip().lower()

    save_bio_raw_to_db(player_id)