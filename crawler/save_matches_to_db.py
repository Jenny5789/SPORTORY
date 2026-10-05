import json
import os

import psycopg
from dotenv import load_dotenv


# 1. 환경변수 읽기
load_dotenv()


def save_matches_to_db(player_id):
    player_id = player_id.strip().lower()

    # 2. 해당 선수의 Activity Raw JSON 읽기
    with open(
        f"data/raw/{player_id}_activity_response.json",
        "r",
        encoding="utf-8"
    ) as file:
        activity_data = json.load(file)


    # 3. 입력한 Player ID와 원본 데이터의 Player ID 확인
    raw_player_id = activity_data["PlayerId"].lower()

    if player_id != raw_player_id:
        raise ValueError(
            f"Player ID 불일치: 입력={player_id}, Raw Data={raw_player_id}"
        )


    # 4. PostgreSQL 연결
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    print("PostgreSQL 연결 성공")


    # 5. 연도별 Activity 순회
    with conn.cursor() as cur:

        for activity in activity_data["Activity"]:

            event_year = activity["EventYear"]

            # 해당 연도의 대회 순회
            for tournament in activity["Tournaments"]:

                source_event_id = str(tournament["EventId"])

                # 6. 해당 대회의 SPORTORY tournament_id 찾기
                cur.execute(
                    """
                    SELECT tournament_id
                    FROM tournaments
                    WHERE source = %s
                      AND source_event_id = %s
                      AND event_year = %s
                    """,
                    (
                        "ATP",
                        source_event_id,
                        event_year
                    )
                )

                tournament_row = cur.fetchone()

                if tournament_row is None:
                    print(
                        f"대회 없음: {event_year} "
                        f"{tournament['EventName']}"
                    )
                    continue

                tournament_id = tournament_row[0]


                # 7. 해당 대회의 경기 순회
                for match in tournament["Matches"]:

                    round_data = match.get("Round") or {}

                    # 8. matches 테이블 저장
                    cur.execute(
                        """
                        INSERT INTO matches (
                            tournament_id,
                            player_id,
                            source,
                            source_match_id,

                            round_id,
                            round_name,
                            win_loss,

                            opponent_id,
                            opponent_first_name,
                            opponent_last_name,
                            opponent_nationality_code,
                            opponent_rank,

                            set1_player,
                            set1_opponent,
                            set1_tiebreak,

                            set2_player,
                            set2_opponent,
                            set2_tiebreak,

                            set3_player,
                            set3_opponent,

                            set4_player,
                            set4_opponent
                        )
                        VALUES (
                            %s, %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s,
                            %s, %s
                        )

                        ON CONFLICT (
                            tournament_id,
                            player_id,
                            source_match_id
                        )
                        DO UPDATE SET
                            round_id = EXCLUDED.round_id,
                            round_name = EXCLUDED.round_name,
                            win_loss = EXCLUDED.win_loss,

                            opponent_id = EXCLUDED.opponent_id,
                            opponent_first_name = EXCLUDED.opponent_first_name,
                            opponent_last_name = EXCLUDED.opponent_last_name,
                            opponent_nationality_code =
                                EXCLUDED.opponent_nationality_code,
                            opponent_rank = EXCLUDED.opponent_rank,

                            set1_player = EXCLUDED.set1_player,
                            set1_opponent = EXCLUDED.set1_opponent,
                            set1_tiebreak = EXCLUDED.set1_tiebreak,

                            set2_player = EXCLUDED.set2_player,
                            set2_opponent = EXCLUDED.set2_opponent,
                            set2_tiebreak = EXCLUDED.set2_tiebreak,

                            set3_player = EXCLUDED.set3_player,
                            set3_opponent = EXCLUDED.set3_opponent,

                            set4_player = EXCLUDED.set4_player,
                            set4_opponent = EXCLUDED.set4_opponent
                        """,
                        (
                            tournament_id,
                            player_id,
                            "ATP",
                            match["MatchId"],

                            round_data.get("Id"),
                            round_data.get("LongName"),
                            match.get("WinLoss"),

                            match.get("OpponentId"),
                            match.get("OpponentFirstName"),
                            match.get("OpponentLastName"),
                            match.get("OpponentNatlId"),
                            match.get("OpponentRank"),

                            match.get("Set1Player"),
                            match.get("Set1Opponent"),
                            match.get("Set1Tie"),

                            match.get("Set2Player"),
                            match.get("Set2Opponent"),
                            match.get("Set2Tie"),

                            match.get("Set3Player"),
                            match.get("Set3Opponent"),

                            match.get("Set4Player"),
                            match.get("Set4Opponent")
                        )
                    )


    # 9. 저장 확정
    conn.commit()
    conn.close()

    print("경기 DB 저장/갱신 성공")


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID를 입력하세요: "
    ).strip().lower()

    save_matches_to_db(player_id)