from playwright.sync_api import sync_playwright


url = "https://www.atptour.com/en/players/jannik-sinner/s0ag/bio"


with sync_playwright() as p:

    # 브라우저 실행
    browser = p.chromium.launch(headless=True)

    # ATP Bio 페이지 접속
    page = browser.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60000)

    # 페이지 HTML 가져오기
    html = page.content()

    print("페이지 제목:", page.title())
    print("HTML 길이:", len(html))
    print(
        "Career 문장 포함 여부:",
        "Unranked to begin 2018" in html
    )

    browser.close()