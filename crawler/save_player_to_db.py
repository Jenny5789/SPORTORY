import json
import os

import psycopg
from dotenv import load_dotenv


# 1. .env 파일 읽기
load_dotenv()


def save_player_to_db(player_id, player_slug):
    player_id = player_id.strip().lower()
    player_slug = player_slug.strip().lower()

    # 2. 해당 선수의 Overview Raw JSON 읽기
    with open(
        f"data/raw/{player_id}_overview.json",
        "r",
        encoding="utf-8"
    ) as file:
        raw_data = json.load(file)

    player = raw_data["data"]


    # 3. PostgreSQL 연결
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    print("PostgreSQL 연결 성공")


    # 4. players 테이블에 선수 저장/갱신
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO players (
                player_id,
                player_slug,
                first_name,
                last_name,
                birth_date,
                nationality_code,
                nationality,
                birth_city,
                height_cm,
                weight_kg,
                play_hand,
                backhand,
                pro_year
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )

            ON CONFLICT (player_id)
            DO UPDATE SET
                player_slug = EXCLUDED.player_slug,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                birth_date = EXCLUDED.birth_date,
                nationality_code = EXCLUDED.nationality_code,
                nationality = EXCLUDED.nationality,
                birth_city = EXCLUDED.birth_city,
                height_cm = EXCLUDED.height_cm,
                weight_kg = EXCLUDED.weight_kg,
                play_hand = EXCLUDED.play_hand,
                backhand = EXCLUDED.backhand,
                pro_year = EXCLUDED.pro_year
            """,
            (
                player_id,
                player_slug,
                player["FirstName"],
                player["LastName"],
                player["BirthDate"][:10],
                player["NatlId"],
                player["Nationality"],
                player["BirthCity"],
                player["HeightCm"],
                player["WeightKg"],
                player["PlayHand"]["Description"],
                player["BackHand"]["Description"],
                player["ProYear"]
            )
        )


    # 5. 변경사항 확정
    conn.commit()

    print("선수 DB 저장/갱신 성공")

    conn.close()


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID를 입력하세요: "
    ).strip().lower()

    player_slug = input(
        "ATP Player Slug를 입력하세요: "
    ).strip().lower()

    save_player_to_db(player_id, player_slug)