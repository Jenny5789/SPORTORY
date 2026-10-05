import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


load_dotenv()


def check_bio_changed(player_id):
    player_id = player_id.strip().lower()

    # 새로 수집한 Bio Raw JSON 읽기
    input_path = Path("data/raw") / f"{player_id}_bio.json"

    if not input_path.exists():
        raise FileNotFoundError(
            f"Bio Raw 파일을 찾을 수 없습니다: {input_path}"
        )

    with open(input_path, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    new_personal = raw_data["data"]["personal"]
    new_career = raw_data["data"]["career"]

    # DB 연결
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT section, item_order, original_text
                FROM player_bios
                WHERE player_id = %s
                ORDER BY section, item_order
                """,
                (player_id,)
            )

            rows = cur.fetchall()

    finally:
        conn.close()

    # DB에 Bio가 하나도 없다면 신규 선수이므로 번역 필요
    if not rows:
        print("기존 Bio 없음 → 번역 필요")
        return True

    old_personal = []
    old_career = []

    for section, item_order, original_text in rows:
        if section == "personal":
            old_personal.append(original_text)

        elif section == "career":
            old_career.append(original_text)

    # 새 Raw Bio와 기존 DB Bio 비교
    if (
        new_personal == old_personal
        and new_career == old_career
    ):
        print("Bio 변경 없음 → 번역 불필요")
        return False

    print("Bio 변경 감지 → 번역 필요")
    return True


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID: "
    ).strip().lower()

    changed = check_bio_changed(player_id)

    print("변경 여부:", changed)