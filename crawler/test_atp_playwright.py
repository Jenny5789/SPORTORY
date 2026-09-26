from playwright.sync_api import sync_playwright


url = "https://www.atptour.com/en/rankings/singles"


with sync_playwright() as p:

    # Chromium 브라우저 실행
    browser = p.chromium.launch(
        headless=False
    )

    # 새 페이지 생성
    page = browser.new_page()

    print("ATP 페이지 접속 시작")

    # ATP Rankings 페이지 접속
    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    # 선수 데이터가 HTML에 생성될 때까지 기다림
    page.wait_for_selector(
        "tr td.player",
        state="attached",
        timeout=60000
    )

    # 선수 정보가 들어 있는 모든 행 찾기
    player_rows = page.locator("tr:has(td.player)")

    print("\n--- ATP Ranking Top 50 ---")


    # 1위 선수의 상세 페이지 주소 확인
    first_player = player_rows.nth(0)

    player_link = first_player.locator(
        "td.player li.name a"
    ).get_attribute("href")

    print("\n--- 1위 선수 상세 페이지 ---")
    print(player_link)
    
    
    # 앞에서부터 50개의 행만 반복
    for i in range(50):

        row = player_rows.nth(i)

        rank = row.locator("td.rank").inner_text()
        name = row.locator("td.player li.name span").inner_text()
        points = row.locator("td.points").inner_text()

        print(
            rank.strip(),
            "|",
            name.strip(),
            "|",
            points.strip()
        )

    input("\n결과를 확인한 후 Enter를 누르세요...")

    browser.close()