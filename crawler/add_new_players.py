import os
import random
import re
import time

import psycopg
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from collect_player_overview import collect_player_overview
from save_raw_to_db import save_raw_to_db
from save_player_to_db import save_player_to_db

from collect_player_stats import collect_player_stats
from save_stats_raw_to_db import save_stats_raw_to_db
from save_player_stats_to_db import save_player_stats_to_db

from collect_player_ranking_history import collect_player_ranking_history
from save_ranking_history_raw_to_db import save_ranking_history_raw_to_db
from save_player_ranking_history_to_db import save_player_ranking_history_to_db

from collect_player_activity import collect_player_activity
from save_activity_raw_to_db import save_activity_raw_to_db
from save_matches_to_db import save_matches_to_db

from collect_player_bio import collect_player_bio
from save_bio_raw_to_db import save_bio_raw_to_db
from check_bio_changed import check_bio_changed
from translate_player_bio import translate_player_bio
from save_player_bios_to_db import save_player_bios_to_db

from collect_player_image import collect_player_image
from save_player_image_to_db import save_player_image_to_db


load_dotenv()

RANKING_URL = "https://www.atptour.com/en/rankings/singles"
NEW_PLAYER_COUNT = 10


# 1. SPORTORY DB에 이미 등록된 선수 확인
def get_existing_player_ids():

    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"
    )

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT player_id
                FROM players
                """
            )

            existing_ids = {
                row[0].lower()
                for row in cur.fetchall()
            }

        return existing_ids

    finally:
        conn.close()


# 2. ATP Singles Ranking 선수 목록 확인
def get_ranking_players():

    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        print("ATP Singles Ranking 접속")
        print(RANKING_URL)

        driver.get(RANKING_URL)

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "a[href*='/en/players/']"
                )
            )
        )

        links = driver.find_elements(
            By.CSS_SELECTOR,
            "a[href*='/en/players/']"
        )

        players = []
        seen = set()

        pattern = re.compile(
            r"/en/players/([^/]+)/([^/]+)"
        )

        for link in links:

            href = link.get_attribute("href")

            if not href:
                continue

            match = pattern.search(href)

            if not match:
                continue

            player_slug = (
                match.group(1)
                .strip()
                .lower()
            )

            player_id = (
                match.group(2)
                .strip()
                .lower()
            )

            # 같은 선수가 여러 링크에서 발견되는 경우 중복 제거
            if player_id in seen:
                continue

            name = link.text.strip()

            seen.add(player_id)

            players.append(
                {
                    "player_id": player_id,
                    "player_slug": player_slug,
                    "name": name
                }
            )

        return players

    finally:
        driver.quit()


# 3. DB에 없는 신규 선수 10명 찾기
def find_new_players(count=NEW_PLAYER_COUNT):

    existing_ids = get_existing_player_ids()

    print()
    print("현재 DB 선수 수:", len(existing_ids))

    ranking_players = get_ranking_players()

    print(
        "Ranking에서 확인한 선수:",
        len(ranking_players)
    )

    print()

    new_players = []

    for player in ranking_players:

        player_id = player["player_id"]

        # 이미 DB에 있는 선수
        if player_id in existing_ids:

            print(
                f"[EXIST] "
                f"{player['name']} "
                f"({player_id})"
            )

            continue

        # DB에 없는 신규 선수
        new_players.append(player)

        print(
            f"[NEW {len(new_players):02d}] "
            f"{player['name']} | "
            f"{player['player_id']} | "
            f"{player['player_slug']}"
        )

        if len(new_players) >= count:
            break

    return new_players


# 4. 신규 선수 전체 데이터 수집
def collect_new_player(player):

    player_id = player["player_id"]
    player_slug = player["player_slug"]
    player_name = player["name"]

    success = []
    errors = []

    # Profile
    try:
        print("\n[Profile]")

        collect_player_overview(
            player_id,
            player_slug
        )

        save_raw_to_db(player_id)

        save_player_to_db(
            player_id,
            player_slug
        )

        print(f"[SUCCESS] Profile: {player_id}")
        success.append("Profile")

    except Exception as error:
        print(f"[ERROR] Profile: {player_id}")
        print(f"오류: {error}")

        errors.append("Profile")

        # players 등록이 실패하면 나머지 DB 저장도 문제가 될 수 있으므로 종료
        return success, errors

    # Statistics
    try:
        print("\n[Statistics]")

        collect_player_stats(player_id)
        save_stats_raw_to_db(player_id)
        save_player_stats_to_db(player_id)

        print(f"[SUCCESS] Statistics: {player_id}")
        success.append("Statistics")

    except Exception as error:
        print(f"[ERROR] Statistics: {player_id}")
        print(f"오류: {error}")
        errors.append("Statistics")

    # Ranking History
    try:
        print("\n[Ranking History]")

        collect_player_ranking_history(player_id)
        save_ranking_history_raw_to_db(player_id)
        save_player_ranking_history_to_db(player_id)

        print(
            f"[SUCCESS] Ranking History: "
            f"{player_id}"
        )

        success.append("Ranking")

    except Exception as error:
        print(
            f"[ERROR] Ranking History: "
            f"{player_id}"
        )

        print(f"오류: {error}")
        errors.append("Ranking")

    # Matches
    try:
        print("\n[Matches]")

        collect_player_activity(
            player_id,
            player_slug
        )

        save_activity_raw_to_db(player_id)
        save_matches_to_db(player_id)

        print(f"[SUCCESS] Matches: {player_id}")
        success.append("Matches")

    except Exception as error:
        print(f"[ERROR] Matches: {player_id}")
        print(f"오류: {error}")
        errors.append("Matches")

    # Bio
    try:
        print("\n[Bio]")

        collect_player_bio(
            player_id,
            player_slug
        )

        save_bio_raw_to_db(player_id)

        bio_changed = check_bio_changed(
            player_id
        )

        if bio_changed:
            print(
                "Bio 신규/변경 확인 "
                "→ Gemini 번역 실행"
            )

            translate_player_bio(player_id)
            save_player_bios_to_db(player_id)

        else:
            print(
                "Bio 변경 없음 "
                "→ Gemini 번역 생략"
            )

        print(f"[SUCCESS] Bio: {player_id}")
        success.append("Bio")

    except Exception as error:
        print(f"[ERROR] Bio: {player_id}")
        print(f"오류: {error}")
        errors.append("Bio")

    # Image
    try:
        print("\n[Image]")

        collect_player_image(
            player_id,
            player_slug
        )

        save_player_image_to_db(player_id)

        print(f"[SUCCESS] Image: {player_id}")
        success.append("Image")

    except Exception as error:
        print(f"[ERROR] Image: {player_id}")
        print(f"오류: {error}")
        errors.append("Image")

    print()
    print(f"{player_name} 수집 결과")

    print(
        "성공:",
        ", ".join(success)
        if success
        else "없음"
    )

    print(
        "실패:",
        ", ".join(errors)
        if errors
        else "없음"
    )

    return success, errors


# 5. 신규 선수 10명 전체 수집 실행
def add_new_players(players):

    complete_count = 0
    error_count = 0

    print()
    print("=" * 60)
    print("신규 선수 전체 데이터 수집 시작")
    print("=" * 60)

    for index, player in enumerate(
        players,
        start=1
    ):

        print()
        print("=" * 60)

        print(
            f"[{index:02d}/{len(players):02d}] "
            f"{player['name']}"
        )

        print(
            f"Player ID: "
            f"{player['player_id']}"
        )

        print(
            f"Player Slug: "
            f"{player['player_slug']}"
        )

        print("=" * 60)

        success, errors = collect_new_player(
            player
        )

        if errors:
            error_count += 1
        else:
            complete_count += 1

        # 선수 사이 5~10초 대기
        if index < len(players):

            wait_time = random.uniform(5, 10)

            print(
                f"\n다음 선수 수집까지 "
                f"{wait_time:.1f}초 대기"
            )

            time.sleep(wait_time)

    print()
    print("=" * 60)
    print("신규 선수 전체 데이터 수집 종료")
    print("=" * 60)

    print(
        f"전체 성공 선수: "
        f"{complete_count}명"
    )

    print(
        f"일부 실패 선수: "
        f"{error_count}명"
    )


# 실행
if __name__ == "__main__":

    new_players = find_new_players(
        count=NEW_PLAYER_COUNT
    )

    print()
    print("=" * 60)
    print("추가 후보 선수")
    print("=" * 60)

    for index, player in enumerate(
        new_players,
        start=1
    ):

        print(
            f"{index:02d}. "
            f"{player['name']} | "
            f"{player['player_id']} | "
            f"{player['player_slug']}"
        )

    print()
    print(
        f"신규 선수 후보: "
        f"{len(new_players)}명"
    )

    if len(new_players) < NEW_PLAYER_COUNT:

        print()
        print(
            f"신규 선수 "
            f"{NEW_PLAYER_COUNT}명을 "
            f"찾지 못했습니다."
        )

        print(
            "데이터 수집을 진행하지 않습니다."
        )

    else:

        print()

        answer = input(
            "위 신규 선수들의 전체 데이터를 "
            "수집할까요? (y/n): "
        ).strip().lower()

        if answer == "y":

            add_new_players(
                new_players
            )

        else:

            print()
            print(
                "신규 선수 추가를 "
                "취소했습니다."
            )