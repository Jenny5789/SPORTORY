# SPORTORY 데이터 수집 자동화

## 자동 수집

Windows 작업 스케줄러가 수집 스크립트를 주기적으로 실행한다.

### 주 2회
- 화요일 / 금요일 13:00
- Statistics
- Ranking History
- Matches
- 실행 파일: `crawler/get_players_from_db.py`

### 월 1회
- 매월 1일 13:30
- Profile
- Bio
- Image
- Bio 변경 시에만 Gemini 번역 실행
- 실행 파일: `crawler/run_monthly_player_data.py`

## 실행 구조

get_players_from_db.py / run_monthly_player_data.py
→ DB에서 선수 목록 조회
→ 선수별 데이터 수집
→ Raw Data 저장
→ 가공 데이터 저장
→ Supabase PostgreSQL 업데이트

한 선수 또는 데이터 수집에서 오류가 발생해도 다음 수집을 계속 진행한다.

## 작업 스케줄러 등록

- 프로그램: 사용하는 Python 실행 파일(conda 환경의 `python.exe`)
- 인수: 위 실행 파일 경로 (예: `crawler/get_players_from_db.py`)
- 시작 위치: 저장소 루트 폴더 (`data/raw`, `logs/` 등 상대 경로를 사용하므로 반드시 루트에서 실행)

## 실행

```bash
conda activate SPORTORY
python crawler/get_players_from_db.py      # 주 2회
python crawler/run_monthly_player_data.py  # 월 1회
```
