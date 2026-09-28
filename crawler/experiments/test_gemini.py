import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY를 찾을 수 없습니다.")

client = genai.Client(api_key=api_key)

text = "From Sesto in the German-speaking region of Italy."

prompt = f"""
다음은 ATP 테니스 선수 Bio의 영어 원문입니다.

원문의 의미와 사실을 변경하거나 추가하지 말고
자연스러운 한국어로 번역해주세요.

테니스 관련 고유명사와 전문 용어의 의미를 정확하게 유지해주세요.

영어 원문:
{text}
"""

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt
)

print("영어 원문:")
print(text)

print("\n한국어 번역:")
print(response.text)