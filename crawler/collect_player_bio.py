import json
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def collect_player_bio(player_id, player_slug):
    player_id = player_id.strip().lower()
    player_slug = player_slug.strip().lower()

    url = (
        f"https://www.atptour.com/en/players/"
        f"{player_slug}/{player_id}/bio"
    )

    driver = webdriver.Chrome()

    print("\nATP Bio 수집 시작")
    print("Player ID:", player_id)
    print("Player Slug:", player_slug)
    print("URL:", url)

    try:
        driver.get(url)

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".player_name")
            )
        )

        player_name = driver.find_element(
            By.CSS_SELECTOR,
            ".player_name"
        ).text.strip()

        bio_tabs = driver.find_elements(
            By.CSS_SELECTOR,
            ".atp_player-bio .tabs"
        )

        if len(bio_tabs) < 2:
            raise ValueError(
                "Personal / Career Bio 영역을 찾을 수 없습니다."
            )

        personal_items = bio_tabs[0].find_elements(
            By.CSS_SELECTOR,
            ".basic-content li"
        )

        career_items = bio_tabs[1].find_elements(
            By.CSS_SELECTOR,
            ".basic-content li"
        )

        personal = []

        for item in personal_items:
            text = item.get_attribute("textContent").strip()

            if text:
                personal.append(text)

        career = []

        for item in career_items:
            text = item.get_attribute("textContent").strip()

            if text:
                career.append(text)

        raw_data = {
            "source": "ATP",
            "source_type": "player_bio",
            "player_id": player_id,
            "source_url": url,
            "saved_at": datetime.now().astimezone().isoformat(),
            "collection_method": "selenium_html",
            "data": {
                "player_name": player_name,
                "personal": personal,
                "career": career
            }
        }

        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)

        output_path = raw_dir / f"{player_id}_bio.json"

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                raw_data,
                file,
                ensure_ascii=False,
                indent=2
            )

        print("\nBio 수집 완료")
        print("선수:", player_name)
        print("Personal:", len(personal), "개")
        print("Career:", len(career), "개")
        print("저장 위치:", output_path)

    finally:
        driver.quit()


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID: "
    ).strip().lower()

    player_slug = input(
        "ATP Player Slug: "
    ).strip().lower()

    collect_player_bio(player_id, player_slug)