"""새로 수집한 Biography와 DB 저장 원문 비교, 번역 필요 여부 판단.

입력: data/raw/{player_id}_bio.json, player_bios 테이블 → 출력: 변경 여부(bool)
실행: python crawler/check_bio_changed.py
"""

import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


load_dotenv()


def check_bio_changed(player_id):
    """Personal, Career 섹션별 원문 리스트 비교. 기존 Bio 없음 또는 변경 시 True, 동일 시 False 반환."""
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
            # item_order 순 정렬: 새 Bio 리스트와 항목 순서까지 비교
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