"""requests로 ATP 단식 랭킹 페이지 요청 실험.

응답 상태 코드, Content-Type, HTML 앞 500자 확인.
"""

import requests

url = "https://www.atptour.com/en/rankings/singles"

response = requests.get(
    url,
    timeout=10
)

print("Status Code:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("HTML Length:", len(response.text))

print("\n--- Response 앞 500자 ---")
print(response.text[:500])