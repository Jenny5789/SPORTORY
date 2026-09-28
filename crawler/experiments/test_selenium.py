from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://www.atptour.com/en/players/jannik-sinner/s0ag/overview"

driver = webdriver.Chrome()

print("ATP Overview 페이지 접속 시작")

driver.get(url)

print("페이지 제목:", driver.title)
print("현재 URL:", driver.current_url)

# 선수 이름 영역이 생성될 때까지 기다림
player_name = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".player_name")
    )
)

# 선수 이름
name = player_name.text

# 왼쪽 정보 목록
left_rows = driver.find_elements(
    By.CSS_SELECTOR,
    ".pd_left li"
)

# 오른쪽 정보 목록
right_rows = driver.find_elements(
    By.CSS_SELECTOR,
    ".pd_right li"
)

# Age / Weight / Height / Turned pro
for row in left_rows:

    if "Age" in row.text:
        age = row.find_elements(
            By.TAG_NAME,
            "span"
        )[1].text

    elif "Weight" in row.text:
        weight = row.find_elements(
            By.TAG_NAME,
            "span"
        )[1].text

    elif "Height" in row.text:
        height = row.find_elements(
            By.TAG_NAME,
            "span"
        )[1].text

    elif "Turned pro" in row.text:
        pro_year = row.find_elements(
            By.TAG_NAME,
            "span"
        )[1].text


# Country / Birthplace / Plays / Coach
for row in right_rows:

    if "Country" in row.text:
        country = row.find_element(
            By.CSS_SELECTOR,
            ".flag"
        ).text

    elif "Birthplace" in row.text:
        birthplace = row.find_elements(
            By.TAG_NAME,
            "span"
        )[1].text

    elif "Plays" in row.text:
        plays = row.find_elements(
            By.TAG_NAME,
            "span"
        )[1].text

    elif "Coach" in row.text:
        coach = row.find_elements(
            By.TAG_NAME,
            "span"
        )[1].text


print("\nOverview에서 수집한 정보:")
print("선수 이름:", name)
print("국적:", country)
print("나이 / 생년월일:", age)
print("몸무게:", weight)
print("키:", height)
print("프로 전향 연도:", pro_year)
print("출생지:", birthplace)
print("플레이:", plays)
print("코치:", coach)

input("\n결과를 확인한 후 Enter를 누르세요...")

driver.quit()