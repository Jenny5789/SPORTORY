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