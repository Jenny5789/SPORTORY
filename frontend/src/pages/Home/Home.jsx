/*
 * Home 화면 (/home)
 * - 히어로: 서비스 소개, 단식 순위 순 선수 슬라이더 (5초 자동 전환)
 * - Explore Sports: 종목 타일 목록 (Tennis만 선수 목록으로 이동)
 * - 선수 클릭 시 PlayerQuickProfile 팝업
 * - API: GET /players
 */
import { useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import Header from '../../components/Header/Header'
import PlayerQuickProfile from '../Players/components/PlayerQuickProfile/PlayerQuickProfile'
import './Home.css'

import homeHero from '../../assets/home/home_hero.png'
import tennisImg from '../../assets/home/sport_tennis.png'
import footballImg from '../../assets/home/sport_football.png'
import basketballImg from '../../assets/home/sport_basketball.png'
import baseballImg from '../../assets/home/sport_baseball.png'
import cyclingImg from '../../assets/home/sport_cycling.png'
import runningImg from '../../assets/home/sport_running.png'

// 배포 환경은 VITE_API_BASE_URL 사용, 미설정 시 로컬 FastAPI 서버
const API_BASE =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
// 선수 슬라이더 자동 전환 간격 (ms)
const PLAYER_INTERVAL = 5000

function Home() {
  const railRef = useRef(null)

  const [players, setPlayers] = useState([])
  const [playerIndex, setPlayerIndex] = useState(0)
  const [selectedPlayer, setSelectedPlayer] = useState(null)

  // 종목 타일 데이터, available: false 종목은 링크 없이 Planned 표시
  const sports = [
    {
      name: 'Tennis',
      status: 'Available',
      image: tennisImg,
      available: true,
    },
    {
      name: 'Football',
      status: 'Planned',
      image: footballImg,
      available: false,
    },
    {
      name: 'Basketball',
      status: 'Planned',
      image: basketballImg,
      available: false,
    },
    {
      name: 'Baseball',
      status: 'Planned',
      image: baseballImg,
      available: false,
    },
    {
      name: 'Cycling',
      status: 'Planned',
      image: cyclingImg,
      available: false,
    },
    {
      name: 'Running',
      status: 'Planned',
      image: runningImg,
      available: false,
    },
  ]

  /* PLAYER DATA */

  // 마운트 시 1회 선수 목록 조회
  useEffect(() => {
    const loadPlayers = async () => {
      try {
        const response = await fetch(`${API_BASE}/players`)

        if (!response.ok) {
          throw new Error('Failed to load players')
        }

        const playerList = await response.json()

        // PlayerQuickProfile의 ranking prop 형태({ singles_rank, singles_points })로 변환
        const playersWithRanking = playerList.map((player) => ({
          ...player,
          ranking: {
            singles_rank: player.singles_rank,
            singles_points: player.singles_points,
          },
        }))

        setPlayers(playersWithRanking)
      } catch (error) {
        // 실패 시 콘솔 기록, 히어로 영역은 LOADING TENNIS 문구 유지
        console.error('Failed to load players:', error)
      }
    }

    loadPlayers()
  }, [])

  // 단식 순위 있는 선수만 순위 오름차순 정렬 (슬라이더 순서)
  const rankedPlayers = useMemo(() => {
    return [...players]
      .filter((player) => player.ranking?.singles_rank)
      .sort(
        (a, b) =>
          a.ranking.singles_rank - b.ranking.singles_rank,
      )
  }, [players])

  const activePlayer = rankedPlayers[playerIndex]

  /* PLAYER SLIDER */

  // 선수 2명 이상, 팝업 닫힌 상태에서만 자동 전환 (팝업 열림 시 정지)
  useEffect(() => {
      if (
      rankedPlayers.length <= 1 ||
      selectedPlayer
    ) {
      return undefined
    }

    const timer = window.setInterval(() => {
      setPlayerIndex(
        (current) => (current + 1) % rankedPlayers.length,
      )
    }, PLAYER_INTERVAL)

    // 의존 값 변경, 언마운트 시 타이머 해제
    return () => window.clearInterval(timer)
  }, [rankedPlayers.length, selectedPlayer])
    
  // 이전, 다음 버튼: 첫 선수와 마지막 선수 사이 순환
  const showPreviousPlayer = () => {
    if (!rankedPlayers.length) return

    setPlayerIndex((current) =>
      current === 0
        ? rankedPlayers.length - 1
        : current - 1,
    )
  }

  const showNextPlayer = () => {
    if (!rankedPlayers.length) return

    setPlayerIndex(
      (current) => (current + 1) % rankedPlayers.length,
    )
  }

  /* HOME CONTROLS */

  // 종목 타일 레일 가로 스크롤 (direction: -1 왼쪽, 1 오른쪽)
  const scrollRail = (direction) => {
    railRef.current?.scrollBy({
      left: direction * 380,
      behavior: 'smooth',
    })
  }

  // EXPLORE SPORTS 버튼 클릭 시 종목 섹션으로 이동
  const scrollToSports = () => {
    document
      .getElementById('explore-sports')
      ?.scrollIntoView({
        behavior: 'smooth',
      })
  }

  return (
    <div className="home-page">
      <Header variant="overlay" />

      {/* HERO */}

      <section className="hero">

        {/* LEFT: SPORTORY */}

        <div className="hero-brand">
          <img
            src={homeHero}
            alt="People participating in several different sports"
            className="hero-brand-image"
          />

          <div className="hero-brand-scrim" />

          <div className="hero-copy">
            <p className="eyebrow">
              SPORTS + STORY
            </p>

            <h1 className="display">
              SPORTS CREATE
              <br />
              <em>MORE STORIES</em>
            </h1>

            <p className="hero-description">
              스포츠는 경기 그 이상입니다.
              <br />
              사람, 기록, 그리고 이야기가 모이는 곳,
              <br />
              SPORTORY.
            </p>

            <button
              className="cta"
              type="button"
              onClick={scrollToSports}
            >
              EXPLORE SPORTS

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
              >
                <path d="M12 4v16M6 14l6 6 6-6" />
              </svg>
            </button>
          </div>
        </div>

        {/* RIGHT: CURRENTLY AVAILABLE SPORT */}

        <div className="hero-available">
          {activePlayer ? (
            <>
              <div
                className="available-rank-bg"
                aria-hidden="true"
              >
                {String(
                  activePlayer.ranking?.singles_rank ?? '',
                ).padStart(2, '0')}
              </div>

              {/* 모든 텍스트를 하나의 흐름 안에 배치 */}

              <div className="available-content">

                <div className="available-intro">
                  <span className="available-label">
                    NOW AVAILABLE
                  </span>

                  <strong className="available-sport">
                    TENNIS
                  </strong>
                </div>

                <button
                  type="button"
                  className="available-player available-player-button"
                  onClick={() => setSelectedPlayer(activePlayer)}
                  aria-label={`Open ${activePlayer.first_name} ${activePlayer.last_name} quick profile`}
                >
                  <p className="available-country">
                    {activePlayer.nationality}
                  </p>

                  <h2 className="available-name">
                    <span>
                      {activePlayer.first_name}
                    </span>

                    <strong>
                      {activePlayer.last_name}
                    </strong>
                  </h2>
                </button>

                <div className="available-ranking">
                  <div className="available-ranking-item">
                    <span>WORLD RANKING</span>

                    <strong className="ranking-number">
                      #
                      {String(
                        activePlayer.ranking?.singles_rank ?? '—',
                      ).padStart(2, '0')}
                    </strong>
                  </div>

                  <div className="available-ranking-item">
                    <span>POINTS</span>

                    <strong>
                      {activePlayer.ranking?.singles_points
                        ? Number(
                            activePlayer.ranking.singles_points,
                          ).toLocaleString()
                        : '—'}
                    </strong>
                  </div>
                </div>

                <div className="available-data">
                  <span>PROFILE</span>
                  <span>RANKING</span>
                  <span>MATCHES</span>
                  <span>STATISTICS</span>
                  <span>BIOGRAPHY</span>
                </div>

                <button
                  type="button"
                  className="available-link available-link-button"
                  onClick={() => setSelectedPlayer(activePlayer)}
                >
                  EXPLORE PLAYER
                  <span>→</span>
                </button>

              </div>
             
              {/* PLAYER IMAGE */}

              <button
                type="button"
                className="available-visual available-visual-button"
                onClick={() => setSelectedPlayer(activePlayer)}
                aria-label={`Open ${activePlayer.first_name} ${activePlayer.last_name} quick profile`}
              >
                <img
                  key={activePlayer.player_id}
                  src={activePlayer.image_url}
                  alt={`${activePlayer.first_name} ${activePlayer.last_name}`}
                />
              </button>

              {/* SLIDER NAVIGATION */}

              <div className="available-navigation">
                <div className="available-counter">
                  <strong>
                    {String(playerIndex + 1).padStart(2, '0')}
                  </strong>

                  <span>/</span>

                  <span>
                    {String(rankedPlayers.length).padStart(2, '0')}
                  </span>
                </div>

                <div className="available-buttons">
                  <button
                    type="button"
                    onClick={showPreviousPlayer}
                    aria-label="Previous player"
                  >
                    ←
                  </button>

                  <button
                    type="button"
                    onClick={showNextPlayer}
                    aria-label="Next player"
                  >
                    →
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="available-loading">
              LOADING TENNIS
            </div>
          )}
        </div>
      </section>

      {/* EXPLORE SPORTS */}

      <section
        className="explore"
        id="explore-sports"
      >
        <div className="explore-head">
          <div>
            <h2>EXPLORE SPORTS</h2>

            <p>
              다양한 스포츠의 선수, 기록, 이야기를 만나보세요.
            </p>
          </div>

          <div className="rail-nav">
            <button
              type="button"
              aria-label="Scroll left"
              onClick={() => scrollRail(-1)}
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
              >
                <path d="M15 5l-7 7 7 7" />
              </svg>
            </button>

            <button
              type="button"
              aria-label="Scroll right"
              onClick={() => scrollRail(1)}
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
              >
                <path d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

        <div
          className="rail"
          ref={railRef}
        >
          {sports.map((sport) => {
            const tile = (
              <>
                <img
                  src={sport.image}
                  alt={sport.name}
                />

                <div className="tile-scrim" />

                <div className="tile-copy">
                  <div className="name">
                    {sport.name}

                    {sport.available && (
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                      >
                        <path d="M5 12h14M13 6l6 6-6 6" />
                      </svg>
                    )}
                  </div>

                  <span className="status">
                    {sport.status}
                  </span>
                </div>
              </>
            )

            // available 종목만 선수 목록 링크, 나머지는 클릭 불가 타일
            if (sport.available) {
              return (
                <Link
                  to="/tennis/players"
                  className="tile available"
                  key={sport.name}
                >
                  {tile}
                </Link>
              )
            }

            return (
              <div
                className="tile"
                key={sport.name}
              >
                {tile}
              </div>
            )
          })}
        </div>
      </section>

      {/* PLAYER QUICK PROFILE POPUP */}
      {selectedPlayer && (
        <PlayerQuickProfile
          player={selectedPlayer}
          ranking={selectedPlayer.ranking}
          onClose={() => setSelectedPlayer(null)}
        />
      )}
    </div>
  )
}

export default Home