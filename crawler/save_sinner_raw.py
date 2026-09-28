import json
from datetime import datetime

sinner_data = {
    "LastName": "Sinner",
    "FirstName": "Jannik",
    "BirthCity": "San Candido, Italy",
    "Coach": "Simone Vagnozzi, Darren Cahill",
    "BirthDate": "2001-08-16T00:00:00",
    "Age": 25,
    "NatlId": "ITA",
    "Nationality": "Italy",
    "HeightIn": 75,
    "HeightFt": "6'3\"",
    "HeightCm": 191,
    "WeightLb": 170,
    "WeightKg": 77,
    "PlayHand": {
        "Id": "R",
        "Description": "Right-Handed"
    },
    "BackHand": {
        "Id": "2",
        "Description": "Two-Handed"
    },
    "ProYear": 2018,
    "SglRank": 1,
    "SglHiRank": 1,
    "SglCareerWon": 365,
    "SglCareerLost": 89,
    "SglYtdWon": 44,
    "SglYtdLost": 3,
    "SglCareerTitles": 30,
    "SglYtdTitles": 6,
    "CareerPrizeFormatted": "$69,542,463",
    "SglHiRankDate": "2024-06-10T00:00:00"
}

raw_data = {
    "source": "ATP",
    "source_type": "player_overview",
    "player_id": "s0ag",
    "source_url": "https://www.atptour.com/en/-/www/players/hero/s0ag?v=1",
    "saved_at": datetime.now().astimezone().isoformat(),
    "collection_method": "manual_devtools_poc",
    "data": sinner_data
}

with open(
    "data/raw/sinner_overview.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        raw_data,
        file,
        ensure_ascii=False,
        indent=4
    )

print("저장 완료: data/raw/sinner_overview.json")