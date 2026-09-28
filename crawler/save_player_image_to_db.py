import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


load_dotenv()

player_id = input("ATP Player ID: ").strip()

metadata_path = (
    Path("data/raw")
    / f"{player_id}_image_metadata.json"
)

if not metadata_path.exists():
    raise FileNotFoundError(
        f"이미지 Metadata 파일을 찾을 수 없습니다: {metadata_path}"
    )

with open(metadata_path, "r", encoding="utf-8") as file:
    image_data = json.load(file)

if image_data.get("player_id") != player_id:
    raise ValueError(
        f"입력한 player_id({player_id})와 "
        f"Metadata의 player_id"
        f"({image_data.get('player_id')})가 다릅니다."
    )

connection = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

insert_sql = """
INSERT INTO player_images (
    player_id,
    source,
    source_page_url,
    source_image_url,
    image_path,
    mime_type,
    collected_at,
    collection_method
)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
)
ON CONFLICT (player_id, source)
DO UPDATE SET
    source_page_url = EXCLUDED.source_page_url,
    source_image_url = EXCLUDED.source_image_url,
    image_path = EXCLUDED.image_path,
    mime_type = EXCLUDED.mime_type,
    collected_at = EXCLUDED.collected_at,
    collection_method = EXCLUDED.collection_method;
"""

try:
    with connection.cursor() as cursor:
        cursor.execute(
            insert_sql,
            (
                player_id,
                image_data["source"],
                image_data["source_page_url"],
                image_data["source_image_url"],
                image_data["file_path"],
                image_data["mime_type"],
                image_data["collected_at"],
                image_data["collection_method"]
            )
        )

    connection.commit()

finally:
    connection.close()


print("\n선수 이미지 DB 저장 완료")
print("Player ID:", player_id)
print("Source:", image_data["source"])
print("Image Path:", image_data["file_path"])
print("Image URL:", image_data["source_image_url"])