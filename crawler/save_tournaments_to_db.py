import json
import os

import psycopg
from dotenv import load_dotenv


# 1. .env 파일 읽기
load_dotenv()


# 2. 저장할 선수의 ATP Player ID 입력
player_id = input("ATP Player ID를 입력하세요: ").strip().lower()

# 3. 해당 선수의 Activity Raw JSON 읽기
with open(
    f"data/raw/{player_id}_activity_response.json",
    "r",
    encoding="utf-8"
) as file:
    activity_data = json.load(file)


# 4. PostgreSQL 연결
conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

print("PostgreSQL 연결 성공")


# 5. Activity의 연도별 대회 확인
for activity in activity_data["Activity"]:

    event_year = activity["EventYear"]

    for tournament in activity["Tournaments"]:

        location = tournament["Location"]

        # 6. tournaments 테이블에 저장
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tournaments (
                    source,
                    source_event_id,
                    event_year,
                    name,
                    country,
                    city,
                    start_date,
                    end_date,
                    event_type,
                    surface,
                    indoor_outdoor,
                    singles_draw_size,
                    doubles_draw_size
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )

                ON CONFLICT (source, source_event_id, event_year)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    country = EXCLUDED.country,
                    city = EXCLUDED.city,
                    start_date = EXCLUDED.start_date,
                    end_date = EXCLUDED.end_date,
                    event_type = EXCLUDED.event_type,
                    surface = EXCLUDED.surface,
                    indoor_outdoor = EXCLUDED.indoor_outdoor,
                    singles_draw_size = EXCLUDED.singles_draw_size,
                    doubles_draw_size = EXCLUDED.doubles_draw_size
                """,
                (
                    "ATP",
                    str(tournament["EventId"]),
                    event_year,
                    tournament["EventName"],
                    location.get("EventCountry"),
                    location.get("EventCity"),
                    tournament["EventDate"][:10],
                    tournament["PlayEndDate"][:10],
                    tournament["EventType"],
                    tournament["Surface"],
                    tournament["InOutdoor"],
                    tournament["SglDrawSize"],
                    tournament["DblDrawSize"]
                )
            )


# 7. 저장 확정
conn.commit()
conn.close()

print("대회 DB 저장/갱신 성공")