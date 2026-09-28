import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY를 찾을 수 없습니다.")

player_id = input("ATP Player ID: ").strip()

input_path = Path("data/raw") / f"{player_id}_bio.json"
output_path = Path("data/processed") / f"{player_id}_bio_translated.json"

if not input_path.exists():
    raise FileNotFoundError(
        f"Bio Raw 파일을 찾을 수 없습니다: {input_path}"
    )

with open(input_path, "r", encoding="utf-8") as file:
    raw_data = json.load(file)

if raw_data.get("player_id") != player_id:
    raise ValueError(
        f"입력한 player_id({player_id})와 "
        f"Raw Data의 player_id({raw_data.get('player_id')})가 다릅니다."
    )

client = genai.Client(api_key=api_key)


def translate_section(section_name, texts):
    items = []

    for index, text in enumerate(texts, start=1):
        items.append(
            {
                "item_order": index,
                "original_text": text
            }
        )

    prompt = f"""
다음은 ATP 테니스 선수 Bio의 {section_name} 항목입니다.

각 영어 원문을 한국어로 번역하세요.

규칙:
1. 원문의 의미와 사실을 변경하지 않습니다.
2. 원문에 없는 정보를 추가하지 않습니다.
3. 자연스러운 한국어로 번역합니다.
4. 선수명, 대회명 등 고유명사의 의미를 유지합니다.
5. 테니스 전문 용어의 의미를 정확하게 유지합니다.
6. item_order를 절대 변경하지 않습니다.
7. 모든 항목을 빠짐없이 번역합니다.

입력 데이터:
{json.dumps(items, ensure_ascii=False)}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
            response_schema={
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "item_order": {
                            "type": "INTEGER"
                        },
                        "translated_text": {
                            "type": "STRING"
                        }
                    },
                    "required": [
                        "item_order",
                        "translated_text"
                    ]
                }
            }
        )
    )

    translated_items = json.loads(response.text)

    if len(translated_items) != len(texts):
        raise ValueError(
            f"{section_name} 번역 개수가 일치하지 않습니다. "
            f"원문 {len(texts)}개 / 번역 {len(translated_items)}개"
        )

    result = []

    translated_by_order = {
        item["item_order"]: item["translated_text"]
        for item in translated_items
    }

    for index, original_text in enumerate(texts, start=1):
        translated_text = translated_by_order.get(index)

        if not translated_text:
            raise ValueError(
                f"{section_name} {index}번 번역 결과가 없습니다."
            )

        result.append(
            {
                "item_order": index,
                "original_text": original_text,
                "translated_text": translated_text
            }
        )

    return result


print("\nPersonal 19개 일괄 번역 시작")

personal = translate_section(
    "Personal",
    raw_data["data"]["personal"]
)

print("Personal 번역 완료:", len(personal), "개")


print("\nCareer 14개 일괄 번역 시작")

career = translate_section(
    "Career",
    raw_data["data"]["career"]
)

print("Career 번역 완료:", len(career), "개")


translated_data = {
    "source": raw_data["source"],
    "source_type": "player_bio_translation",
    "player_id": player_id,
    "source_url": raw_data["source_url"],
    "model": "gemini-3.1-flash-lite",
    "data": {
        "player_name": raw_data["data"]["player_name"],
        "personal": personal,
        "career": career
    }
}


output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    output_path,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        translated_data,
        file,
        ensure_ascii=False,
        indent=2
    )


print("\nBio 번역 완료")
print("선수:", translated_data["data"]["player_name"])
print("Personal:", len(personal), "개")
print("Career:", len(career), "개")
print("Gemini API 호출: 총 2회")
print("저장 위치:", output_path)