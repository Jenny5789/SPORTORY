import json
import os

import psycopg
from dotenv import load_dotenv


# 1. 환경변수 읽기
load_dotenv()


# 2. 저장할 선수의 ATP Player ID 입력
player_id = input("ATP Player ID를 입력하세요: ").strip().lower()


# 3. 해당 선수의 Stats Raw JSON 읽기
with open(
    f"data/raw/{player_id}_stats_response.json",
    "r",
    encoding="utf-8"
) as file:
    stats_data = json.load(file)


# 4. 필요한 데이터 영역 분리
stats = stats_data["Stats"]
service = stats["ServiceRecordStats"]
return_stats = stats["ReturnRecordStats"]


# 5. 입력한 Player ID와 원본 데이터의 Player ID 확인
raw_player_id = stats["PlayerId"].lower()

if player_id != raw_player_id:
    raise ValueError(
        f"Player ID 불일치: 입력={player_id}, Raw Data={raw_player_id}"
    )


# 6. PostgreSQL 연결
conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

print("PostgreSQL 연결 성공")


# 7. player_stats 저장
with conn.cursor() as cur:
    cur.execute(
        """
        INSERT INTO player_stats (
            player_id,
            category,
            surface,
            event_year,
            rank_date,

            aces,
            double_faults,
            first_serve_percentage,
            first_serve_points_won_percentage,
            second_serve_points_won_percentage,
            break_points_faced,
            break_points_saved_percentage,
            service_games_played,
            service_games_won_percentage,
            service_points_won_percentage,

            first_serve_return_points_won_percentage,
            second_serve_return_points_won_percentage,
            break_points_opportunities,
            break_points_converted_percentage,
            return_games_played,
            return_games_won_percentage,
            return_points_won_percentage,
            total_points_won_percentage
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s
        )

        ON CONFLICT (
            player_id,
            category,
            surface,
            event_year
        )
        DO UPDATE SET
            rank_date = EXCLUDED.rank_date,

            aces = EXCLUDED.aces,
            double_faults = EXCLUDED.double_faults,
            first_serve_percentage = EXCLUDED.first_serve_percentage,
            first_serve_points_won_percentage =
                EXCLUDED.first_serve_points_won_percentage,
            second_serve_points_won_percentage =
                EXCLUDED.second_serve_points_won_percentage,
            break_points_faced = EXCLUDED.break_points_faced,
            break_points_saved_percentage =
                EXCLUDED.break_points_saved_percentage,
            service_games_played = EXCLUDED.service_games_played,
            service_games_won_percentage =
                EXCLUDED.service_games_won_percentage,
            service_points_won_percentage =
                EXCLUDED.service_points_won_percentage,

            first_serve_return_points_won_percentage =
                EXCLUDED.first_serve_return_points_won_percentage,
            second_serve_return_points_won_percentage =
                EXCLUDED.second_serve_return_points_won_percentage,
            break_points_opportunities =
                EXCLUDED.break_points_opportunities,
            break_points_converted_percentage =
                EXCLUDED.break_points_converted_percentage,
            return_games_played = EXCLUDED.return_games_played,
            return_games_won_percentage =
                EXCLUDED.return_games_won_percentage,
            return_points_won_percentage =
                EXCLUDED.return_points_won_percentage,
            total_points_won_percentage =
                EXCLUDED.total_points_won_percentage
        """,
        (
            player_id,
            stats["Category"],
            stats["Surface"],
            stats["EventYear"],
            stats["RankDate"][:10],

            service["Aces"],
            service["DoubleFaults"],
            service["FirstServePercentage"],
            service["FirstServePointsWonPercentage"],
            service["SecondServePointsWonPercentage"],
            service["BreakPointsFaced"],
            service["BreakPointsSavedPercentage"],
            service["ServiceGamesPlayed"],
            service["ServiceGamesWonPercentage"],
            service["ServicePointsWonPercentage"],

            return_stats["FirstServeReturnPointsWonPercentage"],
            return_stats["SecondServeReturnPointsWonPercentage"],
            return_stats["BreakPointsOpportunities"],
            return_stats["BreakPointsConvertedPercentage"],
            return_stats["ReturnGamesPlayed"],
            return_stats["ReturnGamesWonPercentage"],
            return_stats["ReturnPointsWonPercentage"],
            return_stats["TotalPointsWonPercentage"]
        )
    )


# 8. 저장 확정
conn.commit()
conn.close()

print("선수 Stats DB 저장/갱신 성공")