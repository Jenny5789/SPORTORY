import base64
import json
import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


player_id = input("ATP Player ID를 입력하세요: ").strip().lower()
player_slug = input("ATP Player Slug를 입력하세요: ").strip().lower()

overview_url = (
    f"https://www.atptour.com/en/players/"
    f"{player_slug}/{player_id}/overview"
)

target_pattern = f"/players/hero/{player_id}"


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
    print("\nATP 선수 Overview 페이지 접속")
    print(f"Player ID: {player_id}")
    print(f"Player Slug: {player_slug}")
    print(f"URL: {overview_url}")

    driver.get(overview_url)

    time.sleep(5)

    performance_logs = driver.get_log("performance")

    overview_data = None
    source_url = None
    response_status = None
    mime_type = None

    for log in performance_logs:
        message = json.loads(log["message"])["message"]

        if message["method"] != "Network.responseReceived":
            continue

        params = message["params"]
        response = params["response"]

        response_url = response.get("url", "")

        if target_pattern not in response_url:
            continue

        print("\nOverview 데이터 응답 발견")
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

            response_json = json.loads(body)

            overview_data = response_json
            source_url = response_url
            response_status = response.get("status")
            mime_type = response.get("mimeType")

            break

        except Exception as error:
            print(f"응답 Body 읽기 실패: {error}")

    if overview_data is None:
        raise RuntimeError(
            "Overview 데이터 응답을 찾지 못했습니다."
        )

    # ATP 응답 구조 확인
    #
    # 응답 자체가 선수 데이터인 경우:
    # {
    #   "FirstName": "...",
    #   "LastName": "...",
    #   ...
    # }
    #
    # 응답이 data로 한 번 감싸져 있는 경우:
    # {
    #   "data": {
    #       "FirstName": "...",
    #       ...
    #   }
    # }
    #
    # 두 경우 모두 SPORTORY Raw 구조에서는
    # raw_data["data"]가 실제 선수 데이터가 되도록 맞춘다.

    if (
        isinstance(overview_data, dict)
        and isinstance(overview_data.get("data"), dict)
    ):
        player_data = overview_data["data"]
    else:
        player_data = overview_data

    required_fields = [
        "FirstName",
        "LastName",
        "BirthDate",
        "NatlId",
        "Nationality",
        "HeightCm",
        "WeightKg",
        "PlayHand",
        "BackHand",
        "ProYear"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in player_data
    ]

    if missing_fields:
        raise RuntimeError(
            "필수 Overview 필드가 없습니다: "
            + ", ".join(missing_fields)
        )

    raw_data = {
        "source": "ATP",
        "source_type": "player_overview",
        "player_id": player_id,
        "source_url": source_url,
        "saved_at": datetime.now().astimezone().isoformat(),
        "collection_method": "selenium_cdp",
        "response_status": response_status,
        "mime_type": mime_type,
        "data": player_data
    }

    output_path = f"data/raw/{player_id}_overview.json"

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            raw_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("\nOverview 수집 완료")
    print(
        f"Player: "
        f"{player_data.get('FirstName')} "
        f"{player_data.get('LastName')}"
    )
    print(f"저장 위치: {output_path}")

finally:
    driver.quit()