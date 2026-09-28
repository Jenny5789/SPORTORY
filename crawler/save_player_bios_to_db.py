import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


load_dotenv()

player_id = input("ATP Player ID: ").strip()

input_path = (
    Path("data/processed")
    / f"{player_id}_bio_translated.json"
)

if not input_path.exists():
    raise FileNotFoundError(
        f"번역된 Bio 파일을 찾을 수 없습니다: {input_path}"
    )

with open(input_path, "r", encoding="utf-8") as file:
    bio_data = json.load(file)

if bio_data.get("player_id") != player_id:
    raise ValueError(
        f"입력한 player_id({player_id})와 "
        f"Processed Data의 player_id"
        f"({bio_data.get('player_id')})가 다릅니다."
    )

connection = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

insert_sql = """
INSERT INTO player_bios (
    player_id,
    section,
    item_order,
    original_text,
    translated_text
)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s
)
ON CONFLICT (player_id, section, item_order)
DO UPDATE SET
    original_text = EXCLUDED.original_text,
    translated_text = EXCLUDED.translated_text;
"""

saved_count = 0

try:
    with connection.cursor() as cursor:
        for section in ["personal", "career"]:
            items = bio_data["data"][section]

            for item in items:
                cursor.execute(
                    insert_sql,
                    (
                        player_id,
                        section,
                        item["item_order"],
                        item["original_text"],
                        item["translated_text"]
                    )
                )

                saved_count += 1

    connection.commit()

finally:
    connection.close()


print("\nBio DB 저장 완료")
print("Player ID:", player_id)
print("Personal:", len(bio_data["data"]["personal"]), "개")
print("Career:", len(bio_data["data"]["career"]), "개")
print("총 저장 처리:", saved_count, "개")