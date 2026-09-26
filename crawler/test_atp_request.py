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