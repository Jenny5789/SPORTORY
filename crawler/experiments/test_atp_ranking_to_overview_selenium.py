import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ranking_url = "https://www.atptour.com/en/rankings/singles"
base_url = "https://www.atptour.com"

driver = webdriver.Chrome()

print("ATP Rankings 페이지 접속 시작")

driver.get(ranking_url)

# 선수 데이터가 HTML에 생성될 때까지 기다림
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "tr td.player")
    )
)

# 선수 정보가 들어 있는 모든 행 찾기
player_rows = driver.find_elements(
    By.CSS_SELECTOR,
    "tr:has(td.player)"
)

# 1위 선수 선택
first_player = player_rows[0]

rank = first_player.find_element(
    By.CSS_SELECTOR,
    "td.rank"
).text

ranking_name = first_player.find_element(
    By.CSS_SELECTOR,
    "td.player li.name span"
).text

points = first_player.find_element(
    By.CSS_SELECTOR,
    "td.points"
).text

# 1위 선수의 상세 페이지 주소 가져오기
player_link = first_player.find_element(
    By.CSS_SELECTOR,
    "td.player li.name a"
).get_attribute("href")

print("\n랭킹에서 찾은 선수:")
print("순위:", rank)
print("이름:", ranking_name)
print("포인트:", points)
print("상세 페이지:", player_link)

# 다음 페이지 요청 전 대기
print("\n다음 페이지 요청 전 5초 대기")
time.sleep(5)

# Selenium의 get_attribute("href")는 전체 URL을 반환할 수 있음
if player_link.startswith("http"):
    overview_url = player_link
else:
    overview_url = base_url + player_link

print("\nOverview 페이지로 이동:")
print(overview_url)

driver.get(overview_url)

# 선수 이름 영역이 생성될 때까지 기다림
player_name = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".player_name")
    )
)

print("\nOverview 접근 결과:")
print("페이지 제목:", driver.title)
print("선수 이름:", player_name.text)

input("\n결과를 확인한 후 Enter를 누르세요...")

driver.quit()