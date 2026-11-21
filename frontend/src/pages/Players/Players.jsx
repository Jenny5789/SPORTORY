/*
 * 테니스 선수 목록 화면 (/tennis/players)
 * - API: GET /players (선수 정보와 최신 단식 순위, 포인트 포함)
 * - 카드 클릭 시 PlayerQuickProfile 팝업
 */
import { useEffect, useMemo, useState } from 'react'

import Header from '../../components/Header/Header'
import PlayerQuickProfile from './components/PlayerQuickProfile/PlayerQuickProfile'

import './Players.css'

// 배포 환경은 VITE_API_BASE_URL 사용, 미설정 시 로컬 FastAPI 서버
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

// 선수 카드 우측 화살표 아이콘
function ArrowIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      aria-hidden="true"
    >
      <path d="M5 12h14M13 6l6 6-6 6" />
    </svg>
  )
}

// 선수 카드 목록, ATP 단식 순위 오름차순
function Players() {
  const [players, setPlayers] = useState([])
  // player_id → { singles_rank, singles_points }
  const [rankings, setRankings] = useState({})
  const [selectedPlayer, setSelectedPlayer] = useState(null)
  const [loading, setLoading] = useState(true)

  /* LOAD PLAYERS + LATEST RANKING */

  useEffect(() => {
    async function loadPlayers() {
      try {
        const response = await fetch(
          `${API_BASE_URL}/players`,
        )

        if (!response.ok) {
          throw new Error('Failed to load players')
        }

        const playerData = await response.json()

        // /players 응답의 최신 순위, 포인트로 순위 맵 생성 (선수별 /rankings 추가 요청 없음)
        const rankingResults = playerData.map((player) => [
          player.player_id,
          {
            singles_rank: player.singles_rank,
            singles_points: player.singles_points,
          },
        ])

        setPlayers(playerData)
        setRankings(
          Object.fromEntries(rankingResults),
        )
      } catch (error) {
        // 실패 시 콘솔 기록, 빈 목록 표시
        console.error(
          'Failed to load players:',
          error,
        )
      } finally {
        setLoading(false)
      }
    }

    loadPlayers()
  }, [])

  /* SORT BY ATP RANKING */

  // 순위 없는 선수는 MAX_SAFE_INTEGER로 처리해 맨 뒤 배치
  const rankedPlayers = useMemo(() => {
    return [...players].sort((a, b) => {
      const rankA =
        rankings[a.player_id]?.singles_rank ??
        Number.MAX_SAFE_INTEGER

      const rankB =
        rankings[b.player_id]?.singles_rank ??
        Number.MAX_SAFE_INTEGER

      return rankA - rankB
    })
  }, [players, rankings])

  /* LOADING */

  if (loading) {
    return (
      <>
        <Header />

        <main className="players-page">
          <p className="players-loading">
            Loading players...
          </p>
        </main>
      </>
    )
  }

  /* PAGE */

  return (
    <>
      <Header />

      <main className="players-page">

        {/* INTRO */}

        <section className="players-heading">
          <p className="players-kicker">
            TENNIS
          </p>

          <div className="players-heading-row">
            <h1>
              MEET THE
              <br />
              PLAYERS
            </h1>

            <p>
              Different players, different stories.
              <br />
              That makes tennis special.
            </p>
          </div>
        </section>

        {/* ALL PLAYERS */}

        <section className="all-players">
          <div className="all-players-heading">
            <p>ALL PLAYERS</p>

            <span>
              {String(
                rankedPlayers.length,
              ).padStart(2, '0')}{' '}
              PLAYERS
            </span>
          </div>

          <div className="all-players-grid">
            {rankedPlayers.map((player) => {
              const ranking =
                rankings[player.player_id]

              return (
                <button
                  type="button"
                  key={player.player_id}
                  className="all-player"
                  onClick={() =>
                    setSelectedPlayer(player)
                  }
                  aria-label={`Open ${player.first_name} ${player.last_name} quick profile`}
                >
                  <div className="all-player-image">
                    <span className="all-player-rank">
                      {ranking?.singles_rank
                        ? `#${String(
                            ranking.singles_rank,
                          ).padStart(2, '0')}`
                        : '—'}
                    </span>

                    <img
                      src={player.image_url}
                      alt={`${player.first_name} ${player.last_name}`}
                    />
                  </div>

                  <div className="all-player-copy">
                    <div>
                      <h3>
                        <span>
                          {player.first_name}
                        </span>

                        <strong>
                          {player.last_name}
                        </strong>
                      </h3>

                      <p>
                        {player.nationality}
                      </p>
                    </div>

                    <ArrowIcon />
                  </div>
                </button>
              )
            })}
          </div>
        </section>
      </main>

      {/* QUICK PROFILE */}

      {selectedPlayer && (
        <PlayerQuickProfile
          player={selectedPlayer}
          ranking={
            rankings[selectedPlayer.player_id]
          }
          onClose={() =>
            setSelectedPlayer(null)
          }
        />
      )}
    </>
  )
}

export default Players