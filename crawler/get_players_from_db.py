"""주간 정기 수집 실행: DB 등록 선수 전체의 Stats, Ranking History, Matches 수집과 저장.

입력: players 테이블 (player_id, player_slug) → 출력: raw_data, player_stats, player_ranking_history, matches 테이블, logs/collection_{날짜}.log
실행: python crawler/get_players_from_db.py (Windows 작업 스케줄러 주 2회 실행 대상)
"""

import os
import random
import time
import logging
from datetime import datetime

import psycopg
from dotenv import load_dotenv

from collect_player_stats import collect_player_stats
from save_stats_raw_to_db import save_stats_raw_to_db
from save_player_stats_to_db import save_player_stats_to_db

from collect_player_ranking_history import collect_player_ranking_history
from save_ranking_history_raw_to_db import save_ranking_history_raw_to_db
from save_player_ranking_history_to_db import save_player_ranking_history_to_db

from collect_player_activity import collect_player_activity
from save_activity_raw_to_db import save_activity_raw_to_db
from save_matches_to_db import save_matches_to_db


load_dotenv()


# 로그 폴더 생성
os.makedirs("logs", exist_ok=True)

# 날짜별 로그 파일
log_file = f"logs/collection_{datetime.now():%Y-%m-%d}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)


def run_collection():
    """players 테이블의 선수별로 Stats, Ranking History, Matches를 수집, 원본 저장, 정제 저장 순서로 처리."""

    logging.info("[START] 정기 수집 시작")

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

        for index, (player_id, player_slug) in enumerate(players):

            print()
            print("=" * 60)
            print("자동 수집 대상:", player_id, player_slug)
            print("=" * 60)

            results = []

            # 데이터 종류별 개별 try: 한 종류 실패 시 로그 기록 후 다음 종류, 다음 선수 계속 진행

            # Stats
            try:
                collect_player_stats(player_id)
                save_stats_raw_to_db(player_id)
                save_player_stats_to_db(player_id)

                print(f"[성공] Stats: {player_id}")
                results.append("Stats")

            except Exception as e:
                print(f"[실패] Stats: {player_id}")
                print(f"오류: {e}")

                logging.error(
                    f"[ERROR] {player_id} Stats - {e}"
                )

            # Ranking History
            try:
                collect_player_ranking_history(player_id)
                save_ranking_history_raw_to_db(player_id)
                save_player_ranking_history_to_db(player_id)

                print(f"[성공] Ranking History: {player_id}")
                results.append("Ranking")

            except Exception as e:
                print(f"[실패] Ranking History: {player_id}")
                print(f"오류: {e}")

                logging.error(
                    f"[ERROR] {player_id} Ranking - {e}"
                )

            # Matches
            try:
                collect_player_activity(player_id, player_slug)
                save_activity_raw_to_db(player_id)
                save_matches_to_db(player_id)

                print(f"[성공] Matches: {player_id}")
                results.append("Matches")

            except Exception as e:
                print(f"[실패] Matches: {player_id}")
                print(f"오류: {e}")

                logging.error(
                    f"[ERROR] {player_id} Matches - {e}"
                )

            # 선수별 성공 결과 기록
            if results:
                logging.info(
                    f"[SUCCESS] {player_id} {' / '.join(results)}"
                )

            # 마지막 선수 뒤에는 대기하지 않음
            # 선수 사이 5~10초 무작위 대기
            if index < len(players) - 1:
                wait_time = random.uniform(5, 10)

                print(f"다음 선수 수집까지 {wait_time:.1f}초 대기")
                time.sleep(wait_time)

        print()
        print("=" * 60)
        print("전체 선수 데이터 수집 종료")
        print("=" * 60)

        logging.info("[END] 정기 수집 완료")

    finally:
        conn.close()
        print("PostgreSQL 연결 종료")


if __name__ == "__main__":
    run_collection()