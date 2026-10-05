[SPORTORY 신규 ATP 선수 추가 순서]

준비
- ATP Player ID 확인
- ATP Player Slug 확인

1. Overview 수집
python crawler\collect_player_overview.py
입력: Player ID, Player Slug

2. Overview Raw DB 저장
python crawler\save_raw_to_db.py
입력: Player ID

3. 선수 기본정보 DB 저장
python crawler\save_player_to_db.py
입력: Player ID, Player Slug

4. Ranking History 수집
python crawler\collect_player_ranking_history.py
입력: Player ID

5. Ranking History Raw DB 저장
python crawler\save_ranking_history_raw_to_db.py
입력: Player ID

6. Ranking History DB 저장
python crawler\save_player_ranking_history_to_db.py
입력: Player ID

7. Activity 수집
python crawler\collect_player_activity.py
입력: Player ID, Player Slug

8. Activity Raw DB 저장
python crawler\save_activity_raw_to_db.py
입력: Player ID

9. 대회 DB 저장
python crawler\save_tournaments_to_db.py
입력: Player ID

10. 경기 DB 저장
python crawler\save_matches_to_db.py
입력: Player ID

11. Statistics 수집
python crawler\collect_player_stats.py
입력: Player ID

12. Statistics Raw DB 저장
python crawler\save_stats_raw_to_db.py
입력: Player ID

13. Statistics DB 저장
python crawler\save_player_stats_to_db.py
입력: Player ID

14. Bio 수집
python crawler\collect_player_bio.py
입력: Player ID, Player Slug

15. Bio Raw DB 저장
python crawler\save_bio_raw_to_db.py
입력: Player ID

16. Bio 한국어 번역
python crawler\translate_player_bio.py
입력: Player ID

17. Bio DB 저장
python crawler\save_player_bios_to_db.py
입력: Player ID

18. 선수 사진 수집
python crawler\collect_player_image.py
입력: Player ID, Player Slug

수집 결과:
data/player_images/{player_id}.png

19. 선수 사진 저장
python crawler\save_player_image_to_db.py
입력: Player ID

처리:
data/player_images/{player_id}.png
        ↓
Supabase Storage
        ↓
player-images/{player_id}.png
        ↓
Public URL
        ↓
player_images.image_path

20. API 최종 확인

GET /players
GET /players/{player_id}
GET /players/{player_id}/bio
GET /players/{player_id}/rankings
GET /players/{player_id}/stats
GET /players/{player_id}/matches

확인 항목:
- 선수 목록에 추가되었는지
- Profile
- Ranking
- Matches
- Statistics
- Bio EN / KO
- 선수 이미지

※ 이미지 API /images/{player_id}.png의 사용 여부는 현재 FastAPI 구현 확인 후 확정


21. Frontend 최종 확인

/tennis/players
/tennis/players/{player_id}

확인 항목:
- 선수 목록 노출
- ATP Ranking 순서
- 선수 이미지
- Profile
- Ranking
- Matches
- Statistics
- Bio EN / KO


[신규 선수 등록 이후]

최초 등록이 완료되면 이후에는 자동 수집 Runner가 관리한다.

주 2회 예정
- Ranking
- Matches
- Statistics

월 1회 예정
- Profile
- Bio
- Image

Bio는 변경 여부를 먼저 확인한다.

Bio 변경 없음
→ Gemini 번역 생략

Bio 변경 있음
→ Gemini 번역
→ DB 갱신


[전체 흐름]

ATP Player
→ Overview
→ players
→ Ranking History
→ Activity
→ Tournaments / Matches
→ Statistics
→ Bio
→ Gemini Korean Translation
→ Player Bio
→ Player Image
→ Supabase Storage
→ FastAPI
→ Frontend