import os
import random
import time
import logging
from datetime import datetime

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


# 로그 폴더 생성
os.makedirs("logs", exist_ok=True)

# 날짜별 월간 수집 로그
log_file = f"logs/monthly_collection_{datetime.now():%Y-%m-%d}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)


def run_monthly_collection():

    logging.info("[START] 월간 수집 시작")

    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"
    )

    print("PostgreSQL 연결 성공")

    try:
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

    finally:
        conn.close()
        print("PostgreSQL 연결 종료")

    for index, (player_id, player_slug) in enumerate(players):

        print()
        print("=" * 60)
        print("월간 수집 대상:", player_id, player_slug)
        print("=" * 60)

        results = []

        # 1. Profile
        try:
            print("\n[Profile]")

            collect_player_overview(player_id, player_slug)
            save_raw_to_db(player_id)
            save_player_to_db(player_id, player_slug)

            print(f"[성공] Profile: {player_id}")
            results.append("Profile")

        except Exception as e:
            print(f"[실패] Profile: {player_id}")
            print(f"오류: {e}")

            logging.error(
                f"[ERROR] {player_id} Profile - {e}"
            )

        # 2. Bio
        try:
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

            print(f"[성공] Bio: {player_id}")
            results.append("Bio")

        except Exception as e:
            print(f"[실패] Bio: {player_id}")
            print(f"오류: {e}")

            logging.error(
                f"[ERROR] {player_id} Bio - {e}"
            )

        # 3. Image
        try:
            print("\n[Image]")

            collect_player_image(player_id, player_slug)
            save_player_image_to_db(player_id)

            print(f"[성공] Image: {player_id}")
            results.append("Image")

        except Exception as e:
            print(f"[실패] Image: {player_id}")
            print(f"오류: {e}")

            logging.error(
                f"[ERROR] {player_id} Image - {e}"
            )

        # 선수별 성공 결과 기록
        if results:
            logging.info(
                f"[SUCCESS] {player_id} {' / '.join(results)}"
            )

        # 마지막 선수 뒤에는 대기하지 않음
        if index < len(players) - 1:
            wait_time = random.uniform(5, 10)

            print(
                f"\n다음 선수 수집까지 "
                f"{wait_time:.1f}초 대기"
            )

            time.sleep(wait_time)

    print()
    print("=" * 60)
    print("월간 선수 데이터 수집 완료")
    print("=" * 60)

    logging.info("[END] 월간 수집 완료")


if __name__ == "__main__":
    run_monthly_collection()