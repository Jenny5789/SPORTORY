import base64
import json
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def collect_player_ranking_history(player_id):
    player_id = player_id.strip().lower()

    ranking_page_url = (
        f"https://www.atptour.com/en/players/"
        f"cswiki/{player_id}/rankings-history"
    )

    target_pattern = f"/rank/history/{player_id}"

    os.makedirs("data/raw", exist_ok=True)

    options = Options()

    options.set_capability(
        "goog:loggingPrefs",
        {"performance": "ALL"}
    )

    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd(
        "Network.enable",
        {}
    )

    try:
        print("\nATP 선수 Ranking 페이지 접속")
        print(f"Player ID: {player_id}")
        print(f"URL: {ranking_page_url}")

        driver.get(ranking_page_url)

        time.sleep(5)

        performance_logs = driver.get_log("performance")

        ranking_data = None
        source_url = None

        for log in performance_logs:
            message = json.loads(log["message"])["message"]

            if message["method"] != "Network.responseReceived":
                continue

            params = message["params"]
            response = params["response"]

            response_url = response.get("url", "")

            if target_pattern not in response_url:
                continue

            print("\nRanking History 응답 발견")
            print(f"Response URL: {response_url}")
            print(f"Status: {response.get('status')}")
            print(f"MIME Type: {response.get('mimeType')}")

            request_id = params["requestId"]

            try:
                body_result = driver.execute_cdp_cmd(
                    "Network.getResponseBody",
                    {"requestId": request_id}
                )

                body = body_result["body"]

                if body_result.get("base64Encoded"):
                    body = base64.b64decode(body).decode("utf-8")

                ranking_data = json.loads(body)
                source_url = response_url

                break

            except Exception as error:
                print(f"응답 Body 읽기 실패: {error}")

        if ranking_data is None:
            raise RuntimeError(
                "Ranking History 응답을 찾지 못했습니다."
            )

        if "History" not in ranking_data:
            raise RuntimeError(
                "Ranking History 응답에 History 필드가 없습니다."
            )

        if not isinstance(ranking_data["History"], list):
            raise RuntimeError(
                "History 데이터가 리스트 형식이 아닙니다."
            )

        output_path = (
            f"data/raw/"
            f"{player_id}_ranking_history_response.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                ranking_data,
                file,
                ensure_ascii=False,
                indent=4
            )

        print("\nRanking History 수집 완료")
        print(f"Player ID: {player_id}")
        print(f"Ranking 기록 수: {len(ranking_data['History'])}")
        print(f"Source URL: {source_url}")
        print(f"저장 위치: {output_path}")

    finally:
        driver.quit()


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID를 입력하세요: "
    ).strip().lower()

    collect_player_ranking_history(player_id)