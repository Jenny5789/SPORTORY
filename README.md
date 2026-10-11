# SPORTORY

> 선수 기록과 Biography를 연결해 선수의 이야기를 제공하는 개인 프로젝트

SPORTORY = SPORT + STORY

스포츠 데이터를 단순히 나열하는 대신, 선수의 기록과 정보를 한곳에 연결해 보여주는 스포츠 정보 서비스입니다.

첫 번째 종목으로 테니스를 선택했습니다. ATP 선수 데이터를 수집하고, 원본 데이터를 보존한 뒤 서비스에 필요한 형태로 정제·저장합니다. 이후 FastAPI와 React를 통해 선수 목록과 상세 정보를 제공합니다.

## Links

- [SPORTORY 바로가기](https://sportory.vercel.app/)
- [GitHub 저장소](https://github.com/Jenny5789/SPORTORY)

## Screenshots

### Home

SPORTORY의 전체 방향과 현재 제공하는 테니스 서비스를 소개합니다.

<img src="docs/images/home.png" width="80%" alt="SPORTORY Home" />

### Players

수집된 선수 목록과 현재 순위를 확인할 수 있습니다.

<img src="docs/images/players.png" width="80%" alt="SPORTORY Players" />

### Player Profile and Story

선수 카드의 앞면에서는 프로필과 주요 기록을 확인하고, 카드를 뒤집으면 Biography Story를 확인할 수 있습니다.

<img src="docs/images/profile.png" width="80%" alt="SPORTORY Player Profile" />

### Random Biography Story

선수 카드를 클릭하면 Personal · Career Biography 항목 중 3개를 랜덤하게 보여줍니다.

<table>
  <tr>
    <td><img src="docs/images/story-1.png" width="100%" alt="Random Biography Story 1" /></td>
    <td><img src="docs/images/story-2.png" width="100%" alt="Random Biography Story 2" /></td>
  </tr>
</table>

### Ranking

선수의 현재 순위와 순위 이력을 확인할 수 있습니다.

<img src="docs/images/ranking.png" width="80%" alt="SPORTORY Ranking" />

## Project Overview

SPORTORY가 제공하는 핵심 정보는 다음과 같습니다.

- 선수 기본 정보와 이미지
- ATP 단식 순위와 순위 이력
- 선수 경기와 대회 정보
- 선수 통계
- 선수 Biography 원문
- Biography 한국어 번역

서비스의 기본 사용자 흐름은 다음과 같습니다.

```text
Home → Tennis → Players → Player Detail
```

선수 상세 화면에서는 Profile, Ranking, Matches, Statistics, Biography를 함께 확인할 수 있습니다.

## Why SPORTORY

기존 스포츠 서비스는 기록과 순위 중심으로 제공되는 경우가 많습니다. SPORTORY는 선수의 기록에 Biography와 주요 경력을 연결해, 숫자만으로는 알기 어려운 선수의 배경과 이야기를 함께 보여주는 것을 목표로 합니다.

## Data Pipeline

```text
ATP Web Source
      ↓
Data Collection
      ↓
Raw Data Storage
      ↓
Data Processing
      ↓
Biography Translation
      ↓
PostgreSQL
      ↓
FastAPI
      ↓
React Frontend
```

### 1. Data Collection

ATP 페이지의 동적 데이터를 브라우저 환경에서 확인하고, 데이터가 제공되는 형태에 따라 수집 방식을 나눴습니다.

- Profile, Ranking, Matches, Statistics, Image: Network Response 기반 수집
- Biography: HTML에 렌더링된 Personal·Career 영역 수집
- Selenium: 브라우저 실행, 페이지 이동, 렌더링 대기
- CDP: Network 이벤트 확인과 Response Body 접근

ATP에 직접 요청했을 때 `403`이 발생하는 문제가 있었기 때문에, 실제 브라우저 환경에서 데이터를 확인하는 방식으로 수집 구조를 변경했습니다.

### 2. Raw Data Storage

수집한 원본 응답과 함께 다음 메타데이터를 보존합니다.

- Source
- Source URL
- Source Player ID
- Collection Time
- Collection Method
- Original JSON 또는 Content

원본 데이터를 별도로 보존하면 가공 결과에 문제가 생겼을 때 수집을 다시 실행하지 않고 원인을 확인하거나 재처리할 수 있습니다.

### 3. Data Processing

외부 데이터의 필드와 서비스에서 사용하는 필드를 매핑하고, 날짜·국가·플레이 스타일 등의 값을 서비스 스키마에 맞게 정제합니다.

```text
Raw Data → Field Mapping → Data Cleaning → Service Schema → PostgreSQL
```

### 4. Biography Translation

AI는 선수 정보를 생성하는 용도가 아니라, SPORTORY가 수집한 Biography 영문 원문을 한국어로 번역하는 단계에만 사용합니다.

- Gemini 3.1 Flash-Lite 사용
- Personal·Career 섹션을 기준으로 번역
- 기존 Biography가 변경된 경우에만 재번역
- `item_order`, 번역 결과 개수, 누락 여부를 검증한 뒤 저장

Ranking, Match, Statistics처럼 구조화된 데이터는 일반 코드로 처리하고, 문장 형태의 Biography에만 AI 번역을 적용했습니다.

### 5. Database and API

정제된 데이터를 PostgreSQL에 저장하고, FastAPI REST API를 통해 프론트엔드에 제공합니다.

```text
PostgreSQL → FastAPI Response → React Frontend
```

동일한 레코드를 다시 수집할 때는 키를 기준으로 `INSERT` 또는 `UPDATE`하는 UPSERT 방식으로 중복 저장을 줄입니다.

## Main Features

### Player

- Profile
- Player Image
- Nationality
- Birth Date
- Height
- Playing Hand

### Ranking

- ATP Singles Ranking
- Ranking Points
- Ranking History

### Matches

- Player Matches
- Match Information
- Tournament Information

### Statistics

- Player Statistics

### Biography

- Personal Information
- Career Information
- Original English Text
- Korean Translation

## Tech Stack

| Area | Technologies |
| --- | --- |
| Data Collection | Python, Selenium, Chrome DevTools Protocol, Network Response Parsing |
| Data Processing | Python |
| Backend | FastAPI, Uvicorn |
| Database | PostgreSQL, Supabase |
| Frontend | React, Vite, JavaScript, CSS |
| AI Translation | Gemini 3.1 Flash-Lite |
| Deployment | Vercel, Render, Supabase |
| Automation | Windows Task Scheduler |

## Architecture

```text
ATP Web Source
      ↓ Selenium · CDP
Crawler: Collection / Raw Data
      ↓ Python Processing
PostgreSQL / Supabase
      ↓ REST API
FastAPI Backend
      ↓ HTTP Request
React Frontend / Vercel
```

## Repository Structure

```text
SPORTORY/
├── backend/
│   ├── main.py
│   ├── database.py
│   └── routers/
├── crawler/
│   ├── data collection scripts
│   └── translate_player_bio.py
├── data/
│   └── player_images/
├── frontend/
│   └── src/
│       ├── components/
│       └── pages/
├── docs/
├── requirements.txt
└── README.md
```

## API

```http
GET /players
GET /players/{player_id}
GET /players/{player_id}/bio
GET /players/{player_id}/rankings
GET /players/{player_id}/stats
GET /players/{player_id}/matches
GET /images/{player_image}
```

## Deployment

```text
GitHub
├── Frontend → Vercel
└── Backend  → Render → Supabase PostgreSQL
```

- Frontend: Vercel
- Backend: Render
- Database: Supabase PostgreSQL
- Collection Automation: Windows Task Scheduler

## Current Scope

현재 서비스는 테니스 종목의 Player, Ranking, Matches, Statistics, Biography를 제공하며, Biography는 한국어로도 확인할 수 있습니다.

## Project Goal

```text
Sports Data → Story
```

스포츠 데이터를 수집하고, 원본을 보존하며, 서비스에 필요한 형태로 가공하고, API와 웹 화면을 통해 선수의 기록과 이야기를 함께 전달하는 것이 SPORTORY의 목표입니다.
