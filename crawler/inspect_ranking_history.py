"""Sinner 순위 이력 원본 JSON의 구조 확인용 스크립트.

입력: data/raw/sinner_ranking_history_response.json → 출력: 최상위 Key, History 개수, 첫 번째 History 콘솔 출력
실행: python crawler/inspect_ranking_history.py
"""

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