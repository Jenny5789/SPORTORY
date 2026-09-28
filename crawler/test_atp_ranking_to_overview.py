from playwright.sync_api import sync_playwright


ranking_url = "https://www.atptour.com/en/rankings/singles"
base_url = "https://www.atptour.com"


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    print("ATP Rankings 페이지 접속 시작")

    page.goto(
        ranking_url,
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

    # 1위 선수 선택
    first_player = player_rows.nth(0)

    rank = first_player.locator("td.rank").inner_text()
    ranking_name = first_player.locator(
        "td.player li.name span"
    ).inner_text()
    points = first_player.locator("td.points").inner_text()

    # 1위 선수의 상세 페이지 주소 가져오기
    player_link = first_player.locator(
        "td.player li.name a"
    ).get_attribute("href")

    print("\n랭킹에서 찾은 선수:")
    print("순위:", rank.strip())
    print("이름:", ranking_name.strip())
    print("포인트:", points.strip())
    print("상세 페이지:", player_link)

    # ATP 기본 주소와 선수 상세 페이지 주소 연결
    overview_url = base_url + player_link

    # 다음 페이지 요청 전 대기
    print("\n다음 페이지 요청 전 5초 대기")
    page.wait_for_timeout(5000)

    print("\nOverview 페이지로 이동:")
    print(overview_url)

    # 랭킹에서 찾은 주소를 이용하여 선수 Overview 페이지로 이동
    page.goto(
        overview_url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    # 선수 이름 영역이 생성될 때까지 기다림
    page.wait_for_selector(
        ".player_name",
        state="attached",
        timeout=60000
    )

    # 선수 이름
    name = page.locator(".player_name").inner_text()

    # Country
    country_row = page.locator(".pd_right li").filter(has_text="Country")
    country = country_row.locator(".flag").inner_text()

    # Age
    age_row = page.locator(".pd_left li").filter(has_text="Age")
    age = age_row.locator("span").nth(1).inner_text()

    # Weight
    weight_row = page.locator(".pd_left li").filter(has_text="Weight")
    weight = weight_row.locator("span").nth(1).inner_text()

    # Height
    height_row = page.locator(".pd_left li").filter(has_text="Height")
    height = height_row.locator("span").nth(1).inner_text()

    # Turned pro
    pro_row = page.locator(".pd_left li").filter(has_text="Turned pro")
    pro_year = pro_row.locator("span").nth(1).inner_text()

    # Birthplace
    birthplace_row = page.locator(".pd_right li").filter(has_text="Birthplace")
    birthplace = birthplace_row.locator("span").nth(1).inner_text()

    # Plays
    plays_row = page.locator(".pd_right li").filter(has_text="Plays")
    plays = plays_row.locator("span").nth(1).inner_text()

    # Coach
    coach_row = page.locator(".pd_right li").filter(has_text="Coach")
    coach = coach_row.locator("span").nth(1).inner_text()

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

    browser.close()