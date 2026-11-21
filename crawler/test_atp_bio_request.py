"""requests로 ATP 선수 Bio 페이지 요청 실험.

응답 상태 코드, HTML 길이, Career 문장 포함 여부 확인.
"""

import requests


url = "https://www.atptour.com/en/players/jannik-sinner/s0ag/bio"

response = requests.get(url, timeout=30)

print("상태 코드:", response.status_code)
print("HTML 길이:", len(response.text))
print("Career 문장 포함 여부:", "Unranked to begin 2018" in response.text)