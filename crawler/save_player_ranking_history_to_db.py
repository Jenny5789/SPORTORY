"""순위 이력 원본 JSON을 정제해 player_ranking_history 테이블에 UPSERT.

입력: data/raw/{player_id}_ranking_history_response.json → 출력: player_ranking_history 테이블
실행: python crawler/save_player_ranking_history_to_db.py
"""

import json
import os

import psycopg
from dotenv import load_dotenv


# 1. 환경변수 읽기
load_dotenv()


def save_player_ranking_history_to_db(player_id):
    """History 항목별 단식(Roll, Race), 복식 순위와 포인트를 player_ranking_history에 저장 또는 갱신."""
    player_id = player_id.strip().lower()

    # 2. 해당 선수의 Ranking History Raw JSON 읽기
    with open(
        f"data/raw/{player_id}_ranking_history_response.json",
        "r",
        encoding="utf-8"
    ) as file:
        ranking_data = json.load(file)


    # 3. PostgreSQL 연결
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    print("PostgreSQL 연결 성공")


    # 4. History의 각 랭킹 기록을 반복해서 저장
    # (player_id, rank_date) 기준 UPSERT: 같은 날짜 순위 중복 방지
    # RankDate는 앞 10자리(YYYY-MM-DD)만 사용, 시간 제거
    with conn.cursor() as cur:

        for history in ranking_data["History"]:

            cur.execute(
                """
                INSERT INTO player_ranking_history (
                    player_id,
                    rank_date,

                    singles_rank,
                    singles_tie,
                    singles_points,

                    race_rank,
                    race_tie,
                    race_points,

                    doubles_rank,
                    doubles_tie,
                    doubles_points
                )
                VALUES (
                    %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s
                )

                ON CONFLICT (player_id, rank_date)
                DO UPDATE SET
                    singles_rank = EXCLUDED.singles_rank,
                    singles_tie = EXCLUDED.singles_tie,
                    singles_points = EXCLUDED.singles_points,

                    race_rank = EXCLUDED.race_rank,
                    race_tie = EXCLUDED.race_tie,
                    race_points = EXCLUDED.race_points,

                    doubles_rank = EXCLUDED.doubles_rank,
                    doubles_tie = EXCLUDED.doubles_tie,
                    doubles_points = EXCLUDED.doubles_points
                """,
                (
                    player_id,
                    history["RankDate"][:10],

                    history["SglRollRank"],
                    history["SglRollTie"],
                    history["SglRollPoints"],

                    history["SglRaceRank"],
                    history["SglRaceTie"],
                    history["SglRacePoints"],

                    history["DblRollRank"],
                    history["DblRollTie"],
                    history["DblRollPoints"]
                )
            )


    # 5. 저장 확정
    conn.commit()
    conn.close()

    print("Ranking History DB 저장/갱신 성공")


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID를 입력하세요: "
    ).strip().lower()

    save_player_ranking_history_to_db(player_id)