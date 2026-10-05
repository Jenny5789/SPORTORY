import os
import random
import time

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


conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

print("PostgreSQL 연결 성공")


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


for player_id, player_slug in players:
    print("자동 수집 대상:", player_id, player_slug)

    # Stats
    collect_player_stats(player_id)
    save_stats_raw_to_db(player_id)
    save_player_stats_to_db(player_id)

    # Ranking History
    collect_player_ranking_history(player_id)
    save_ranking_history_raw_to_db(player_id)
    save_player_ranking_history_to_db(player_id)

    # Matches
    collect_player_activity(player_id, player_slug)
    save_activity_raw_to_db(player_id)
    save_matches_to_db(player_id)

    wait_time = random.uniform(5, 15)
    print(f"다음 선수 수집까지 {wait_time:.1f}초 대기")
    time.sleep(wait_time)


conn.close()