"""requests로 선수 프로필 데이터 경로(/players/hero) 직접 요청 실험.

응답 상태 코드, Content-Type, 응답 앞 500자 확인.
"""

import requests


player_id = "s0ag"

url = (
    f"https://www.atptour.com/en/-/www/players/hero/"
    f"{player_id}?v=1"
)

response = requests.get(
    url,
    timeout=30
)

print("상태 코드:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("응답 길이:", len(response.content))

print("\n응답 앞부분:")
print(response.text[:500])