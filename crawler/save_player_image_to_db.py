import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from supabase import create_client


load_dotenv()


def save_player_image_to_db(player_id):
    player_id = player_id.strip().lower()

    # 이미지 Metadata
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

    # 로컬 이미지 파일
    local_image_path = Path(image_data["file_path"])

    if not local_image_path.exists():
        raise FileNotFoundError(
            f"이미지 파일을 찾을 수 없습니다: {local_image_path}"
        )

    # Supabase Storage 연결
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SECRET_KEY")

    if not supabase_url:
        raise ValueError(
            "SUPABASE_URL이 설정되어 있지 않습니다."
        )

    if not supabase_key:
        raise ValueError(
            "SUPABASE_SECRET_KEY가 설정되어 있지 않습니다."
        )

    supabase = create_client(
        supabase_url,
        supabase_key
    )

    # Storage 저장 경로
    storage_path = f"{player_id}.png"

    # 이미지 읽기
    with open(local_image_path, "rb") as file:
        image_bytes = file.read()

    # Supabase Storage 업로드
    supabase.storage.from_("player-images").upload(
        path=storage_path,
        file=image_bytes,
        file_options={
            "content-type": image_data["mime_type"],
            "upsert": "true"
        }
    )

    # Public URL 생성
    public_url = supabase.storage.from_(
        "player-images"
    ).get_public_url(storage_path)

    # PostgreSQL 연결
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
                    public_url,
                    image_data["mime_type"],
                    image_data["collected_at"],
                    image_data["collection_method"]
                )
            )

        connection.commit()

    finally:
        connection.close()

    print("\n선수 이미지 Storage/DB 저장 완료")
    print("Player ID:", player_id)
    print("Source:", image_data["source"])
    print("Storage Path:", storage_path)
    print("Public URL:", public_url)
    print("Source Image URL:", image_data["source_image_url"])


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID: "
    ).strip().lower()

    save_player_image_to_db(player_id)