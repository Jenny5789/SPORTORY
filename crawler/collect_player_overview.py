"""ATP 선수 프로필(Overview) API 응답 수집.

입력: player_id, player_slug → 출력: data/raw/{player_id}_overview.json (/players/hero/{player_id} 응답 + 수집 메타데이터)
실행: python crawler/collect_player_overview.py
"""

import base64
import json
import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def collect_player_overview(player_id, player_slug):
    """Overview 페이지 접속 후 CDP Network 로그에서 프로필 API 응답을 찾아 메타데이터와 함께 JSON 파일로 저장."""
    player_id = player_id.strip().lower()
    player_slug = player_slug.strip().lower()

    overview_url = (
        f"https://www.atptour.com/en/players/"
        f"{player_slug}/{player_id}/overview"
    )

    target_pattern = f"/players/hero/{player_id}"

    os.makedirs("data/raw", exist_ok=True)

    options = Options()

    # performance 로그 활성화 (Network 이벤트 기록)
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

        # 페이지 내 API 요청 완료 대기
        time.sleep(5)

        performance_logs = driver.get_log("performance")

        overview_data = None
        source_url = None
        response_status = None
        mime_type = None

        for log in performance_logs:
            message = json.loads(log["message"])["message"]

            # 응답 수신 이벤트만 처리
            if message["method"] != "Network.responseReceived":
                continue

            params = message["params"]
            response = params["response"]

            response_url = response.get("url", "")

            # 프로필 API 응답만 필터링
            if target_pattern not in response_url:
                continue

            print("\nOverview 데이터 응답 발견")
            print(f"Response URL: {response_url}")
            print(f"Status: {response.get('status')}")
            print(f"MIME Type: {response.get('mimeType')}")

            request_id = params["requestId"]

            try:
                # requestId로 응답 본문 조회
                body_result = driver.execute_cdp_cmd(
                    "Network.getResponseBody",
                    {"requestId": request_id}
                )

                body = body_result["body"]

                # base64 인코딩 응답은 디코딩 후 파싱
                if body_result.get("base64Encoded"):
                    body = base64.b64decode(body).decode("utf-8")

                response_json = json.loads(body)

                overview_data = response_json
                source_url = response_url
                response_status = response.get("status")
                mime_type = response.get("mimeType")

                break

            # 본문 조회 실패 시 다음 응답 확인
            except Exception as error:
                print(f"응답 Body 읽기 실패: {error}")

        if overview_data is None:
            raise RuntimeError(
                "Overview 데이터 응답을 찾지 못했습니다."
            )

        # ATP 응답 구조 확인
        # data 객체로 감싼 응답이면 내부 객체 사용
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

        # 원본 응답에 출처, 수집 시각, 수집 방식 메타데이터 추가
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


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID를 입력하세요: "
    ).strip().lower()

    player_slug = input(
        "ATP Player Slug를 입력하세요: "
    ).strip().lower()

    collect_player_overview(player_id, player_slug)