"""requests로 ATP 선수 이미지(player-gladiator-headshot) 직접 요청 실험.

200 응답, image Content-Type 확인 후 data/player_images에 PNG 저장, 그 외 응답은 앞 500자 출력.
"""

from pathlib import Path

import requests


player_id = "s0ag"

image_url = (
    "https://www.atptour.com"
    f"/-/media/alias/player-gladiator-headshot/{player_id}"
)

response = requests.get(
    image_url,
    timeout=30
)

print("Status Code:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("Content-Length:", len(response.content))

if response.status_code == 200:
    content_type = response.headers.get("Content-Type", "")

    if "image" not in content_type:
        raise ValueError(
            f"이미지 응답이 아닙니다. Content-Type: {content_type}"
        )

    output_path = Path("data/player_images") / f"{player_id}.png"

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_path, "wb") as file:
        file.write(response.content)

    print("이미지 저장 완료:", output_path)

else:
    print("이미지 요청 실패")
    print(response.text[:500])