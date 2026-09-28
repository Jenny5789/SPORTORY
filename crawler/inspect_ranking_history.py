import json


with open(
    "data/raw/sinner_ranking_history_response.json",
    "r",
    encoding="utf-8"
) as file:
    ranking_data = json.load(file)


print("최상위 Key:")
print(ranking_data.keys())

print("\nFirstRankYear:")
print(ranking_data.get("FirstRankYear"))

print("\nLastRankYear:")
print(ranking_data.get("LastRankYear"))

print("\nHistory 개수:")
print(len(ranking_data.get("History", [])))

print("\n첫 번째 History:")
print(ranking_data["History"][0])