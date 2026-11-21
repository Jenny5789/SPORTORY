"""Python schedule 라이브러리 기반 수집 스케줄러 (현재 자동 실행은 Windows 작업 스케줄러 사용).

주간 수집(화, 금 13:00)과 월간 수집(매월 1일 13:30)을 프로세스 상시 실행 상태에서 예약 실행.
실행: python crawler/scheduler.py (종료: Ctrl + C)
"""

import time
from datetime import datetime

import schedule

from get_players_from_db import run_collection
from run_monthly_player_data import run_monthly_collection


def scheduled_collection():
    """주간 수집(Stats, Ranking History, Matches) 실행."""
    print()
    print("=" * 60)
    print("예약된 SPORTORY 주간 데이터 수집 시작")
    print("=" * 60)

    run_collection()


def scheduled_monthly_collection():
    """월간 수집(Profile, Bio, Image) 실행. 매일 호출되며 1일이 아니면 종료."""
    # 매월 1일에만 실행
    if datetime.now().day != 1:
        return

    print()
    print("=" * 60)
    print("예약된 SPORTORY 월간 데이터 수집 시작")
    print("=" * 60)

    run_monthly_collection()


# 주 2회
# Stats / Ranking / Matches
schedule.every().tuesday.at("13:00").do(scheduled_collection)
schedule.every().friday.at("13:00").do(scheduled_collection)


# 매월 1일 확인
# Profile / Bio / Image
schedule.every().day.at("13:30").do(scheduled_monthly_collection)


print("SPORTORY 데이터 수집 스케줄러 시작")
print("주간 수집: 매주 화요일 / 금요일 13:00")
print("월간 수집: 매월 1일 13:30")
print("종료: Ctrl + C")


# 30초 간격으로 실행 시각 도달 작업 확인
while True:
    schedule.run_pending()
    time.sleep(30)