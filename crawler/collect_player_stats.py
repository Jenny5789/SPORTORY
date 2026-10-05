import base64
import json
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def collect_player_stats(player_id):
    player_id = player_id.strip().lower()

    stats_page_url = (
        f"https://www.atptour.com/en/players/"
        f"enwiki/{player_id}/player-stats"
    )

    target_pattern = f"/stats/{player_id}/all/all"

    os.makedirs("data/raw", exist_ok=True)

    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


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
        print("\nATP 선수 Player Stats 페이지 접속")
        print(f"Player ID: {player_id}")
        print(f"URL: {stats_page_url}")

        driver.get(stats_page_url)

        time.sleep(5)

        performance_logs = driver.get_log("performance")

        stats_data = None
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

            print("\nStats 응답 발견")
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

                stats_data = json.loads(body)
                source_url = response_url

                break

            except Exception as error:
                print(f"응답 Body 읽기 실패: {error}")

        if stats_data is None:
            raise RuntimeError(
                "Stats 응답을 찾지 못했습니다."
            )

        if "Stats" not in stats_data:
            raise RuntimeError(
                "Stats 응답에 Stats 필드가 없습니다."
            )

        stats = stats_data["Stats"]

        if "PlayerId" not in stats:
            raise RuntimeError(
                "Stats 데이터에 PlayerId 필드가 없습니다."
            )

        if stats["PlayerId"].lower() != player_id:
            raise RuntimeError(
                "요청한 Player ID와 Stats 응답의 PlayerId가 다릅니다."
            )

        if "ServiceRecordStats" not in stats:
            raise RuntimeError(
                "Stats 데이터에 ServiceRecordStats가 없습니다."
            )

        if "ReturnRecordStats" not in stats:
            raise RuntimeError(
                "Stats 데이터에 ReturnRecordStats가 없습니다."
            )

        output_path = (
            f"data/raw/"
            f"{player_id}_stats_response.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                stats_data,
                file,
                ensure_ascii=False,
                indent=4
            )

        print("\nStats 수집 완료")
        print(f"Player ID: {player_id}")
        print(f"Category: {stats.get('Category')}")
        print(f"Surface: {stats.get('Surface')}")
        print(f"Event Year: {stats.get('EventYear')}")
        print(f"Source URL: {source_url}")
        print(f"저장 위치: {output_path}")

    finally:
        driver.quit()


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID를 입력하세요: "
    ).strip().lower()

    collect_player_stats(player_id)