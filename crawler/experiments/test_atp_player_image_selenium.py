"""Selenium, CDP Network 로그로 선수 이미지 응답 추출 실험.

Overview 페이지 로드 중 수신한 player-gladiator-headshot 응답을 requestId로 조회, data/player_images에 PNG 저장.
"""

import base64
import json
from pathlib import Path

from selenium import webdriver


player_id = "s0ag"
player_slug = "jannik-sinner"

page_url = (
    f"https://www.atptour.com/en/players/"
    f"{player_slug}/{player_id}/overview"
)

target_text = f"player-gladiator-headshot/{player_id}"

output_path = Path("data/player_images") / f"{player_id}.png"
output_path.parent.mkdir(parents=True, exist_ok=True)

options = webdriver.ChromeOptions()

# performance 로그 활성화: get_log("performance")로 Network 이벤트 조회
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

    for entry in logs:
        message = json.loads(entry["message"])["message"]

        if message["method"] != "Network.responseReceived":
            continue

        params = message["params"]
        response = params["response"]
        url = response["url"]

        if target_text in url:
            image_request_id = params["requestId"]
            image_url = url

            print("선수 이미지 응답 발견")
            print("Image URL:", image_url)
            print("Status:", response["status"])
            print("MIME Type:", response["mimeType"])

            break

    if image_request_id is None:
        raise RuntimeError(
            "Network 로그에서 선수 이미지 응답을 찾지 못했습니다."
        )

    body = driver.execute_cdp_cmd(
        "Network.getResponseBody",
        {
            "requestId": image_request_id
        }
    )

    # 이미지 등 바이너리 본문은 base64 문자열로 전달
    if body["base64Encoded"]:
        image_bytes = base64.b64decode(body["body"])
    else:
        image_bytes = body["body"].encode("latin1")

    with open(output_path, "wb") as file:
        file.write(image_bytes)

    print("이미지 저장 완료:", output_path)
    print("파일 크기:", len(image_bytes), "bytes")

finally:
    driver.quit()