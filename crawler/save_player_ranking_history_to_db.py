import json
import os

import psycopg
from dotenv import load_dotenv


# 1. 환경변수 읽기
load_dotenv()

# 저장할 선수의 ATP Player ID 입력
player_id = input("ATP Player ID를 입력하세요: ").strip().lower()


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