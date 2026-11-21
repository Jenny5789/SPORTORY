"""ATP 선수 헤드샷 이미지 수집.

입력: player_id, player_slug → 출력: data/player_images/{player_id}.png, data/raw/{player_id}_image_metadata.json
실행: python crawler/collect_player_image.py
"""

import base64
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from selenium import webdriver


def collect_player_image(player_id, player_slug):
    """Overview 페이지의 CDP Network 로그에서 헤드샷 이미지 응답을 찾아 PNG 파일과 메타데이터 JSON으로 저장."""
    player_id = player_id.strip().lower()
    player_slug = player_slug.strip().lower()

    page_url = (
        f"https://www.atptour.com/en/players/"
        f"{player_slug}/{player_id}/overview"
    )

    target_text = f"player-gladiator-headshot/{player_id}"

    image_path = Path("data/player_images") / f"{player_id}.png"
    metadata_path = (
        Path("data/raw")
        / f"{player_id}_image_metadata.json"
    )

    image_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    options = webdriver.ChromeOptions()

    # performance 로그 활성화 (Network 이벤트 기록)
    options.set_capability(
        "goog:loggingPrefs",
        {
            "performance": "ALL"
        }
    )

    driver = webdriver.Chrome(options=options)

    try:
        driver.execute_cdp_cmd(
            "Network.enable",
            {}
        )

        driver.get(page_url)

        logs = driver.get_log("performance")

        image_request_id = None
        image_url = None
        image_status = None
        mime_type = None

        for entry in logs:
            message = json.loads(entry["message"])["message"]

            if message["method"] != "Network.responseReceived":
                continue

            params = message["params"]
            response = params["response"]
            url = response["url"]

            # 헤드샷 이미지 응답만 필터링
            if target_text in url:
                image_request_id = params["requestId"]
                image_url = url
                image_status = response["status"]
                mime_type = response["mimeType"]

                print("\n선수 이미지 응답 발견")
                print("Image URL:", image_url)
                print("Status:", image_status)
                print("MIME Type:", mime_type)

                break

        if image_request_id is None:
            raise RuntimeError(
                "Network 로그에서 선수 이미지 응답을 찾지 못했습니다."
            )

        # 상태 코드 200, image/* MIME 타입만 허용
        if image_status != 200:
            raise RuntimeError(
                f"이미지 응답 상태가 정상적이지 않습니다: "
                f"{image_status}"
            )

        if not mime_type.startswith("image/"):
            raise RuntimeError(
                f"이미지 응답이 아닙니다: {mime_type}"
            )

        # requestId로 이미지 응답 본문 조회
        body = driver.execute_cdp_cmd(
            "Network.getResponseBody",
            {
                "requestId": image_request_id
            }
        )

        # 바이너리 응답은 base64로 전달, 디코딩 후 bytes로 저장
        if body["base64Encoded"]:
            image_bytes = base64.b64decode(body["body"])
        else:
            image_bytes = body["body"].encode("latin1")

        with open(image_path, "wb") as file:
            file.write(image_bytes)

        collected_at = datetime.now(
            ZoneInfo("Asia/Seoul")
        ).isoformat()

        metadata = {
            "source": "ATP",
            "source_type": "player_image",
            "player_id": player_id,
            "source_page_url": page_url,
            "source_image_url": image_url,
            "collected_at": collected_at,
            "collection_method": "selenium_cdp",
            "mime_type": mime_type,
            "file_path": str(image_path),
            "file_size_bytes": len(image_bytes)
        }

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                metadata,
                file,
                ensure_ascii=False,
                indent=2
            )

        print("\n선수 이미지 수집 완료")
        print("Player ID:", player_id)
        print("이미지:", image_path)
        print("파일 크기:", len(image_bytes), "bytes")
        print("Metadata:", metadata_path)

    finally:
        driver.quit()


if __name__ == "__main__":
    player_id = input(
        "ATP Player ID: "
    ).strip().lower()

    player_slug = input(
        "ATP Player Slug: "
    ).strip().lower()

    collect_player_image(
        player_id,
        player_slug
    )