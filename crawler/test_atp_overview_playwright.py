from playwright.sync_api import sync_playwright


url = "https://www.atptour.com/en/players/jannik-sinner/s0ag/overview"


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    print("ATP 선수 Overview 페이지 접속 시작")

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    # 선수 이름 영역이 생성될 때까지 기다림
    page.wait_for_selector(
        ".player_name",
        state="attached",
        timeout=60000
    )

    # 선수 이름 가져오기
    name = page.locator(".player_name").inner_text()

    print("\n선수 이름:")
    print(name)


    # Country가 적혀 있는 한 줄 찾기
    country_row = page.locator(".pd_right li").filter(has_text="Country")

    # 그 줄 안에서 실제 국가 값 가져오기
    country = country_row.locator(".flag").inner_text()

    print("\n국적:")
    print(country)


    # Age가 적혀 있는 한 줄 찾기
    age_row = page.locator(".pd_left li").filter(has_text="Age")

    # 두 번째 span의 값 가져오기
    age = age_row.locator("span").nth(1).inner_text()

    print("\n나이 / 생년월일:")
    print(age)


    # Weight가 적혀 있는 한 줄 찾기
    weight_row = page.locator(".pd_left li").filter(has_text="Weight")

    # 두 번째 span의 값 가져오기
    weight = weight_row.locator("span").nth(1).inner_text()

    print("\n몸무게:")
    print(weight)


    # Height가 적혀 있는 한 줄 찾기
    height_row = page.locator(".pd_left li").filter(has_text="Height")

    # 두 번째 span의 값 가져오기
    height = height_row.locator("span").nth(1).inner_text()

    print("\n키:")
    print(height)


    # Turned pro가 적혀 있는 한 줄 찾기
    pro_row = page.locator(".pd_left li").filter(has_text="Turned pro")

    # 두 번째 span의 값 가져오기
    pro_year = pro_row.locator("span").nth(1).inner_text()

    print("\n프로 전향 연도:")
    print(pro_year)


    # Birthplace가 적혀 있는 한 줄 찾기
    birthplace_row = page.locator(".pd_right li").filter(has_text="Birthplace")

    # 두 번째 span의 값 가져오기
    birthplace = birthplace_row.locator("span").nth(1).inner_text()

    print("\n출생지:")
    print(birthplace)


    # Plays가 적혀 있는 한 줄 찾기
    plays_row = page.locator(".pd_right li").filter(has_text="Plays")

    # 두 번째 span의 값 가져오기
    plays = plays_row.locator("span").nth(1).inner_text()

    print("\n플레이:")
    print(plays)


    # Coach가 적혀 있는 한 줄 찾기
    coach_row = page.locator(".pd_right li").filter(has_text="Coach")

    # 두 번째 span의 값 가져오기
    coach = coach_row.locator("span").nth(1).inner_text()

    print("\n코치:")
    print(coach)


    print("\n현재 페이지 제목:")
    print(page.title())

    print("\n현재 URL:")
    print(page.url)

    input("\n브라우저 화면을 확인한 후 Enter를 누르세요...")

    browser.close()