# SPORTORY 데이터 수집 자동화

## 자동 수집

Python `schedule` 라이브러리를 사용해 선수 데이터 수집을 주기적으로 실행한다.

### 주 2회
- 화요일 / 금요일 13:00
- Statistics
- Ranking History
- Matches

### 월 1회
- 매월 1일 13:30
- Profile
- Bio
- Image
- Bio 변경 시에만 Gemini 번역 실행

## 실행 구조

scheduler.py
→ DB에서 선수 목록 조회
→ 선수별 데이터 수집
→ Raw Data 저장
→ 가공 데이터 저장
→ Supabase PostgreSQL 업데이트

한 선수 또는 데이터 수집에서 오류가 발생해도 다음 수집을 계속 진행한다.

## 실행

```bash
conda activate SPORTORY
python crawler/scheduler.py
```