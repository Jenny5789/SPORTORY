/*
 * 선수 상세 화면 (/tennis/players/:playerId)
 * - 섹션: Profile, Ranking, Statistics, Matches, Biography
 * - 상단 내비게이션: 섹션 이동, 스크롤 위치 기준 현재 섹션 표시
 * - API: GET /players/{player_id}, /players/{player_id}/rankings,
 *   /players/{player_id}/matches, /players/{player_id}/stats, /players/{player_id}/bio
 */
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import Header from '../../components/Header/Header'
import PlayerProfile from './components/PlayerProfile'
import PlayerRanking from './components/PlayerRanking'
import PlayerStatistics from './components/PlayerStatistics'
import PlayerMatches from './components/PlayerMatches'
import PlayerBio from './components/PlayerBio'

import './PlayerDetail.css'

// 배포 환경은 VITE_API_BASE_URL 사용, 미설정 시 로컬 FastAPI 서버
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

// 상단 내비게이션 항목, id는 섹션 래퍼 div의 DOM id와 동일
const DETAIL_SECTIONS = [
  {
    id: 'profile',
    number: '01',
    label: 'PROFILE',
  },
  {
    id: 'ranking',
    number: '02',
    label: 'RANKING',
  },
  {
    id: 'statistics',
    number: '03',
    label: 'STATISTICS',
  },
  {
    id: 'matches',
    number: '04',
    label: 'MATCHES',
  },
  {
    id: 'bio',
    number: '05',
    label: 'BIOGRAPHY',
  },
]

// URL 파라미터 playerId 기준 선수 상세 데이터 조회, 섹션 컴포넌트에 전달
function PlayerDetail() {
  const { playerId } = useParams()

  const [player, setPlayer] = useState(null)
  const [rankings, setRankings] = useState([])
  const [matches, setMatches] = useState([])
  const [stats, setStats] = useState([])
  const [bio, setBio] = useState(null)
  const [activeSection, setActiveSection] =
    useState('profile')

  // playerId 변경 시 5개 API 동시 요청
  // 요청별 개별 then, catch로 한 요청의 네트워크 오류가 다른 섹션 데이터에 영향 없음
  useEffect(() => {
    fetch(`${API_BASE_URL}/players/${playerId}`)
      .then((response) => response.json())
      .then((data) => setPlayer(data))
      .catch((error) =>
        console.error('Failed to load player:', error),
      )

    fetch(
      `${API_BASE_URL}/players/${playerId}/rankings`,
    )
      .then((response) => response.json())
      .then((data) => setRankings(data))
      .catch((error) =>
        console.error('Failed to load rankings:', error),
      )

    fetch(
      `${API_BASE_URL}/players/${playerId}/matches`,
    )
      .then((response) => response.json())
      .then((data) => setMatches(data))
      .catch((error) =>
        console.error('Failed to load matches:', error),
      )

    fetch(
      `${API_BASE_URL}/players/${playerId}/stats`,
    )
      .then((response) => response.json())
      .then((data) => setStats(data))
      .catch((error) =>
        console.error('Failed to load stats:', error),
      )

    fetch(
      `${API_BASE_URL}/players/${playerId}/bio`,
    )
      .then((response) => response.json())
      .then((data) => setBio(data))
      .catch((error) =>
        console.error('Failed to load bio:', error),
      )
  }, [playerId])

  // 스크롤 위치에 따라 내비게이션 활성 섹션 갱신 (IntersectionObserver)
  // 섹션 DOM은 player 수신 후 렌더링되므로 player를 의존성으로 지정
  useEffect(() => {
    const sectionElements = DETAIL_SECTIONS
      .map((section) =>
        document.getElementById(section.id),
      )
      .filter(Boolean)

    if (!sectionElements.length) {
      return
    }

    const observer = new IntersectionObserver(
      (entries) => {
        // 판정 영역에 들어온 섹션 중 노출 비율이 가장 큰 섹션 선택
        const visibleEntries = entries
          .filter((entry) => entry.isIntersecting)
          .sort(
            (a, b) =>
              b.intersectionRatio -
              a.intersectionRatio,
          )

        if (visibleEntries.length > 0) {
          setActiveSection(
            visibleEntries[0].target.id,
          )
        }
      },
      {
        root: null,
        // 뷰포트 상단 150px, 하단 55%를 제외한 영역 기준 판정
        rootMargin: '-150px 0px -55% 0px',
        threshold: [0, 0.1, 0.25, 0.5],
      },
    )

    sectionElements.forEach((element) => {
      observer.observe(element)
    })

    return () => {
      observer.disconnect()
    }
  }, [player])

  // 내비게이션 클릭 시 활성 표시 즉시 변경 후 해당 섹션으로 스크롤
  const scrollToSection = (sectionId) => {
    const section =
      document.getElementById(sectionId)

    if (!section) {
      return
    }

    setActiveSection(sectionId)

    section.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    })
  }

  // 기본 정보(player) 수신 전 로딩 문구, 나머지 데이터는 각 섹션 컴포넌트에서 빈 값 처리
  if (!player) {
    return (
      <>
        <Header />

        <main className="player-detail-page">
          <p className="player-detail-loading">
            Loading player...
          </p>
        </main>
      </>
    )
  }

  return (
    <>
      <Header />

      <nav
        className="player-detail-nav"
        aria-label="Player detail navigation"
      >
        <div className="player-detail-nav-inner">
          <Link
            to="/tennis/players"
            className="player-detail-nav-back"
          >
            <span>←</span>
            ALL PLAYERS
          </Link>

          <div className="player-detail-nav-divider" />

          <div className="player-detail-nav-sections">
            {DETAIL_SECTIONS.map((section) => (
              <button
                type="button"
                key={section.id}
                className={
                  activeSection === section.id
                    ? 'is-active'
                    : ''
                }
                onClick={() =>
                  scrollToSection(section.id)
                }
              >
                <span>{section.number}</span>
                {section.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <main className="player-detail-page">
        <div
          id="profile"
          className="player-detail-section-anchor"
        >
          <PlayerProfile player={player} />
        </div>

        <div
          id="ranking"
          className="player-detail-section-anchor"
        >
          <PlayerRanking rankings={rankings} />
        </div>

        <div
          id="statistics"
          className="player-detail-section-anchor"
        >
          <PlayerStatistics stats={stats} />
        </div>

        <div
          id="matches"
          className="player-detail-section-anchor"
        >
          <PlayerMatches matches={matches} />
        </div>

        <div
          id="bio"
          className="player-detail-section-anchor"
        >
          <PlayerBio bio={bio} />
        </div>
      </main>
    </>
  )
}

export default PlayerDetail