# SPORTORY

**SPORTORY = SPORTS + STORY**

스포츠의 선수, 경기, 기록과 그 안의 이야기를 데이터 기반으로 제공하는 스포츠 정보 서비스입니다.

현재는 첫 번째 구현 대상으로 **Tennis**를 개발하고 있으며,
ATP 선수 데이터를 수집·가공·저장하고 이를 웹 서비스에서 제공하는 전체 데이터 파이프라인을 구축했습니다.

---

## 1. Project

SPORTORY는 스포츠 데이터를 단순히 나열하는 것이 아니라,
선수의 기록과 정보를 연결하여 스포츠와 선수를 이해할 수 있도록 하는 것을 목표로 합니다.

현재 Tennis를 중심으로 다음 데이터를 제공합니다.

- 선수 기본 정보
- 선수 이미지
- ATP Ranking History
- Match
- Statistics
- Biography
- Biography Korean Translation

현재 검증된 주요 선수 외에도 동일한 데이터 수집 구조를 이용하여 선수를 추가할 수 있도록 구성했습니다.

---

## 2. Service

### Home

SPORTORY의 전체 방향을 소개하고 현재 이용 가능한 스포츠인 Tennis로 진입할 수 있습니다.

### Tennis Players

수집된 선수 목록과 현재 랭킹 정보를 확인할 수 있습니다.

### Player Detail

선수별 상세 정보를 제공합니다.

- Profile
- Ranking
- Matches
- Statistics
- Biography
- Korean Translation

### Player Story

선수의 Biography 데이터를 활용하여 기록 이외의 선수 정보를 Story 형태로 제공합니다.

---

## 3. Data Pipeline

SPORTORY는 외부 데이터를 실시간으로 사용자에게 직접 요청하는 방식이 아니라,
데이터를 먼저 수집하고 저장한 뒤 Backend API를 통해 제공합니다.

```text
ATP Web Source
      ↓
Data Collection
      ↓
Raw Data
      ↓
Data Processing
      ↓
AI Translation
      ↓
PostgreSQL
      ↓
FastAPI
      ↓
Frontend
      ↓
User
```

### Collection

ATP Web Source에서 선수 및 관련 데이터를 수집합니다.

웹 페이지의 동적 데이터 처리를 위해 Browser Automation을 사용했습니다.

### Raw Data

수집한 원본 데이터를 별도로 보존하여
가공 과정에서 문제가 발생했을 때 원본을 다시 확인할 수 있도록 구성했습니다.

### Processing

서비스에서 사용할 수 있도록 수집 데이터를 정제하고 구조화합니다.

### AI

선수 Biography의 영어 원문을 기반으로 한국어 번역을 수행합니다.

AI는 인터넷에서 임의로 선수 정보를 생성하는 방식이 아니라,
SPORTORY가 수집한 데이터를 기반으로 필요한 가공에 사용합니다.

### Database

가공된 데이터를 PostgreSQL에 저장합니다.

### Backend

FastAPI를 사용하여 데이터 조회 API를 제공합니다.

### Frontend

Frontend에서 Backend API를 호출하여
실제 DB 데이터를 사용자에게 제공합니다.

---

## 4. Key Features

### Player

- Player Profile
- Player Image
- Nationality
- Birth Date
- Height
- Playing Hand

### Ranking

- ATP Singles Ranking
- Ranking Points
- Ranking History

### Match

- Player Matches
- Match Information

### Statistics

- Player Statistics

### Biography

- Personal Information
- Career Information
- Original English Text
- Korean Translation

---

## 5. Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Uvicorn

### Data Collection

- Python
- Browser Automation
- HTML / Network Response Parsing

### Database

- PostgreSQL
- Supabase

### AI

- Gemini
- Biography Korean Translation

### Deployment

- Vercel — Frontend
- Render — Backend
- Supabase — Database

---

## 6. Project Structure

```text
SPORTORY/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   └── routers/
│
├── crawler/
│   ├── ...
│   └── translate_player_bio.py
│
├── data/
│   └── player_images/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── pages/
│   └── ...
│
├── docs/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 7. Database

SPORTORY는 PostgreSQL을 사용합니다.

주요 데이터 영역은 다음과 같습니다.

- Players
- Player Ranking History
- Matches
- Tournaments
- Player Statistics
- Player Bios
- Player Images
- Raw Data

외부에서 수집한 원본 데이터와 서비스에서 사용하는 가공 데이터를 구분하여 관리합니다.

---

## 8. Backend API

FastAPI를 기반으로 REST API를 제공합니다.

주요 API:

```text
GET /players
GET /players/{player_id}
GET /players/{player_id}/bio
GET /players/{player_id}/rankings
GET /players/{player_id}/stats
GET /players/{player_id}/matches
```

선수 이미지는 Static Resource로 제공합니다.

```text
/images/{player_image}
```

---

## 9. Frontend

Frontend는 Backend API를 통해 SPORTORY DB의 데이터를 조회합니다.

주요 페이지:

```text
Home
  ↓
Tennis
  ↓
Players
  ↓
Player Detail
```

Player Detail에서는 선수의 Profile, Ranking, Matches, Statistics, Biography를 확인할 수 있습니다.

---

## 10. Deployment

현재 서비스는 다음과 같이 배포되어 있습니다.

```text
GitHub
   │
   ├── Frontend
   │       ↓
   │    Vercel
   │
   └── Backend
           ↓
        Render
           ↓
       Supabase
```

### Frontend

Vercel을 통해 React/Vite Frontend를 배포합니다.

### Backend

Render를 통해 FastAPI Backend를 배포합니다.

### Database

Supabase PostgreSQL을 사용합니다.

---

## 11. Current Status

### Implemented

- ATP 선수 데이터 수집
- Raw Data 저장
- 데이터 정제 및 구조화
- Biography 데이터 처리
- Biography 한국어 번역
- PostgreSQL 저장
- FastAPI API
- React Frontend
- Frontend / Backend 연결
- Vercel Frontend 배포
- Render Backend 배포
- Supabase PostgreSQL 연결

### Currently Available

- Tennis
- Player
- Ranking
- Matches
- Statistics
- Biography
- Korean Translation

---

## 12. Future Work

SPORTORY는 Tennis를 첫 번째 스포츠로 구현하고 있으며,
향후 다른 스포츠로 확장할 수 있는 방향을 고려하고 있습니다.

향후 후보 기능:

- Additional Sports
- More Player Data
- News / Interview
- AI-based Player Analysis
- Additional User Features

현재 구현되지 않은 기능은 서비스에서 제공되는 기능으로 간주하지 않습니다.

---

## 13. Project Goal

SPORTORY의 핵심 목표는

> **Sports Data → Story**

입니다.

외부 스포츠 데이터를 수집하고,
원본을 보존하며,
필요한 데이터를 가공하고,
AI를 필요한 부분에 활용한 뒤,
Database와 API를 통해 사용자에게 전달합니다.

단순한 스포츠 데이터 조회를 넘어
선수의 기록과 정보를 연결하여
스포츠와 선수에 대한 이야기를 전달하는 서비스를 지향합니다.
