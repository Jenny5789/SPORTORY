from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://www.atptour.com/en/players/jannik-sinner/s0ag/bio"

driver = webdriver.Chrome()

print("ATP Bio 페이지 접속 시작")

driver.get(url)

print("페이지 제목:", driver.title)
print("현재 URL:", driver.current_url)

WebDriverWait(driver, 60).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".player_name")
    )
)

player_name = driver.find_element(
    By.CSS_SELECTOR,
    ".player_name"
)

print("선수 이름:", player_name.text)

bio_tabs = driver.find_elements(
    By.CSS_SELECTOR,
    ".atp_player-bio .tabs"
)

print("Bio 탭 개수:", len(bio_tabs))

if len(bio_tabs) >= 1:
    personal_items = bio_tabs[0].find_elements(
        By.CSS_SELECTOR,
        ".basic-content li"
    )

    print("\nPersonal:")

    for item in personal_items:
        text = item.get_attribute("textContent").strip()

        if text:
            print("-", text)

if len(bio_tabs) >= 2:
    career_items = bio_tabs[1].find_elements(
        By.CSS_SELECTOR,
        ".basic-content li"
    )

    print("\nCareer:")

    for item in career_items:
        text = item.get_attribute("textContent").strip()

        if text:
            print("-", text)

input("\n결과를 확인한 후 Enter를 누르세요...")

driver.quit()