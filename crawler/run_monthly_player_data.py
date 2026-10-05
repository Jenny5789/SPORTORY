import os
import random
import time

import psycopg
from dotenv import load_dotenv

from collect_player_overview import collect_player_overview
from save_raw_to_db import save_raw_to_db
from save_player_to_db import save_player_to_db

from collect_player_bio import collect_player_bio
from save_bio_raw_to_db import save_bio_raw_to_db
from check_bio_changed import check_bio_changed
from translate_player_bio import translate_player_bio
from save_player_bios_to_db import save_player_bios_to_db

from collect_player_image import collect_player_image
from save_player_image_to_db import save_player_image_to_db


load_dotenv()


# PostgreSQL 연결
conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

print("PostgreSQL 연결 성공")


# 자동 수집 대상 선수 조회
with conn.cursor() as cur:
    cur.execute(
        """
        SELECT player_id, player_slug
        FROM players
        WHERE player_slug IS NOT NULL
        ORDER BY player_id
        """
    )

    players = cur.fetchall()

conn.close()


# 선수별 월간 데이터 수집
for player_id, player_slug in players:
    print("\n========================================")
    print("월간 수집 대상:", player_id, player_slug)
    print("========================================")

    # 1. Profile
    print("\n[Profile]")
    collect_player_overview(player_id, player_slug)
    save_raw_to_db(player_id)
    save_player_to_db(player_id, player_slug)

    # 2. Bio
    print("\n[Bio]")
    collect_player_bio(player_id, player_slug)
    save_bio_raw_to_db(player_id)

    bio_changed = check_bio_changed(player_id)

    if bio_changed:
        print("Bio 변경 확인 → Gemini 번역 실행")

        translate_player_bio(player_id)
        save_player_bios_to_db(player_id)

    else:
        print("Bio 변경 없음 → Gemini 번역 생략")

    # 3. Image
    print("\n[Image]")
    collect_player_image(player_id, player_slug)
    save_player_image_to_db(player_id)

    # 다음 선수 수집 전 대기
    wait_time = random.uniform(5, 15)

    print(
        f"\n다음 선수 수집까지 "
        f"{wait_time:.1f}초 대기"
    )

    time.sleep(wait_time)


print("\n월간 선수 데이터 수집 완료")