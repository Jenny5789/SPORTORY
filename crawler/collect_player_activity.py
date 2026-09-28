import base64
import json
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


player_id = input("ATP Player ID를 입력하세요: ").strip().lower()
player_slug = input("ATP Player Slug를 입력하세요: ").strip().lower()

activity_page_url = (
    f"https://www.atptour.com/en/players/"
    f"{player_slug}/{player_id}/player-activity"
)

target_pattern = f"/activity/sgl/{player_id}/"


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
    print("\nATP 선수 Player Activity 페이지 접속")
    print(f"Player ID: {player_id}")
    print(f"Player Slug: {player_slug}")
    print(f"URL: {activity_page_url}")

    driver.get(activity_page_url)

    time.sleep(5)

    performance_logs = driver.get_log("performance")

    activity_data = None
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

        print("\nActivity 응답 발견")
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

            activity_data = json.loads(body)
            source_url = response_url

            break

        except Exception as error:
            print(f"응답 Body 읽기 실패: {error}")

    if activity_data is None:
        raise RuntimeError(
            "Activity 응답을 찾지 못했습니다."
        )

    if "PlayerId" not in activity_data:
        raise RuntimeError(
            "Activity 응답에 PlayerId 필드가 없습니다."
        )

    if activity_data["PlayerId"].lower() != player_id:
        raise RuntimeError(
            "요청한 Player ID와 Activity 응답의 PlayerId가 다릅니다."
        )

    if "Activity" not in activity_data:
        raise RuntimeError(
            "Activity 응답에 Activity 필드가 없습니다."
        )

    if not isinstance(activity_data["Activity"], list):
        raise RuntimeError(
            "Activity 데이터가 리스트 형식이 아닙니다."
        )

    output_path = (
        f"data/raw/"
        f"{player_id}_activity_response.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            activity_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    tournament_count = sum(
        len(activity.get("Tournaments", []))
        for activity in activity_data["Activity"]
    )

    print("\nActivity 수집 완료")
    print(f"Player ID: {player_id}")
    print(f"연도 그룹 수: {len(activity_data['Activity'])}")
    print(f"대회 수: {tournament_count}")
    print(f"Source URL: {source_url}")
    print(f"저장 위치: {output_path}")

finally:
    driver.quit()