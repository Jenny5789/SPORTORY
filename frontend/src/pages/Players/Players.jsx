import { useEffect, useMemo, useState } from 'react'

import Header from '../../components/Header/Header'
import PlayerQuickProfile from './components/PlayerQuickProfile/PlayerQuickProfile'

import './Players.css'

const API_BASE_URL = 'http://127.0.0.1:8000'
const SHOWCASE_INTERVAL = 3000

function ArrowIcon({ direction = 'right' }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      aria-hidden="true"
      style={
        direction === 'left'
          ? { transform: 'rotate(180deg)' }
          : undefined
      }
    >
      <path d="M5 12h14M13 6l6 6-6 6" />
    </svg>
  )
}

function Players() {
  const [players, setPlayers] = useState([])
  const [rankings, setRankings] = useState({})
  const [activeIndex, setActiveIndex] = useState(0)
  const [selectedPlayer, setSelectedPlayer] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isShowcasePaused, setIsShowcasePaused] = useState(false)

  useEffect(() => {
    async function loadPlayers() {
      try {
        const response = await fetch(`${API_BASE_URL}/players`)

        if (!response.ok) {
          throw new Error('Failed to load players')
        }

        const playerData = await response.json()

        const rankingResults = await Promise.all(
          playerData.map(async (player) => {
            try {
              const rankingResponse = await fetch(
                `${API_BASE_URL}/players/${player.player_id}/rankings?limit=1`,
              )

              if (!rankingResponse.ok) {
                return [player.player_id, null]
              }

              const rankingData = await rankingResponse.json()

              return [
                player.player_id,
                rankingData[0] || null,
              ]
            } catch {
              return [player.player_id, null]
            }
          }),
        )

        setPlayers(playerData)
        setRankings(Object.fromEntries(rankingResults))
      } catch (error) {
        console.error('Failed to load players:', error)
      } finally {
        setLoading(false)
      }
    }

    loadPlayers()
  }, [])

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

  // 등록된 선수 전체를 Showcase에 사용
  const featuredPlayers = rankedPlayers

  const activePlayer = featuredPlayers[activeIndex]

  const activeRanking = activePlayer
    ? rankings[activePlayer.player_id]
    : null

  // 선수 목록이 변경됐을 때 index 범위 보호
  useEffect(() => {
    if (
      featuredPlayers.length > 0 &&
      activeIndex >= featuredPlayers.length
    ) {
      setActiveIndex(0)
    }
  }, [activeIndex, featuredPlayers.length])

  // Showcase 자동 순환
  useEffect(() => {
    if (
      featuredPlayers.length <= 1 ||
      isShowcasePaused ||
      selectedPlayer
    ) {
      return
    }

    const intervalId = setInterval(() => {
      setActiveIndex((current) =>
        current === featuredPlayers.length - 1
          ? 0
          : current + 1,
      )
    }, SHOWCASE_INTERVAL)

    return () => clearInterval(intervalId)
  }, [
    featuredPlayers.length,
    isShowcasePaused,
    selectedPlayer,
  ])

  const showPrevious = () => {
    setActiveIndex((current) =>
      current === 0
        ? featuredPlayers.length - 1
        : current - 1,
    )
  }

  const showNext = () => {
    setActiveIndex((current) =>
      current === featuredPlayers.length - 1
        ? 0
        : current + 1,
    )
  }

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

  return (
    <>
      <Header />

      <main className="players-page">
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

        {activePlayer && (
          <section
            className="players-showcase"
            onMouseEnter={() => setIsShowcasePaused(true)}
            onMouseLeave={() => setIsShowcasePaused(false)}
          >
            <button
              type="button"
              className="showcase-player"
              onClick={() =>
                setSelectedPlayer(activePlayer)
              }
            >
              <div className="showcase-copy">
                <div className="showcase-ranking">
                  <span>ATP RANKING</span>

                  <strong>
                    {activeRanking?.singles_rank
                      ? `#${String(
                          activeRanking.singles_rank,
                        ).padStart(2, '0')}`
                      : '—'}
                  </strong>
                </div>

                <div className="showcase-identity">
                  <span>
                    {activePlayer.nationality}
                  </span>

                  <h2>
                    {activePlayer.first_name}
                    <br />
                    {activePlayer.last_name}
                  </h2>

                  <div className="showcase-explore">
                    EXPLORE PLAYER
                    <ArrowIcon />
                  </div>
                </div>
              </div>

              <div className="showcase-visual">
                <span className="showcase-background-rank">
                  {activeRanking?.singles_rank
                    ? String(
                        activeRanking.singles_rank,
                      ).padStart(2, '0')
                    : ''}
                </span>

                <img
                  src={`${API_BASE_URL}${activePlayer.image_url}`}
                  alt={`${activePlayer.first_name} ${activePlayer.last_name}`}
                />
              </div>
            </button>

            {featuredPlayers.length > 1 && (
              <div className="showcase-controls">
                <span>
                  {String(activeIndex + 1).padStart(
                    2,
                    '0',
                  )}
                  {' / '}
                  {String(
                    featuredPlayers.length,
                  ).padStart(2, '0')}
                </span>

                <div>
                  <button
                    type="button"
                    onClick={showPrevious}
                    aria-label="Previous player"
                  >
                    <ArrowIcon direction="left" />
                  </button>

                  <button
                    type="button"
                    onClick={showNext}
                    aria-label="Next player"
                  >
                    <ArrowIcon />
                  </button>
                </div>
              </div>
            )}
          </section>
        )}

        <section className="all-players">
          <div className="all-players-heading">
            <p>ALL PLAYERS</p>

            <span>
              {String(rankedPlayers.length).padStart(
                2,
                '0',
              )}{' '}
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
                      src={`${API_BASE_URL}${player.image_url}`}
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

                      <p>{player.nationality}</p>
                    </div>

                    <ArrowIcon />
                  </div>
                </button>
              )
            })}
          </div>
        </section>
      </main>

      {selectedPlayer && (
        <PlayerQuickProfile
          player={selectedPlayer}
          ranking={
            rankings[selectedPlayer.player_id]
          }
          onClose={() => setSelectedPlayer(null)}
        />
      )}
    </>
  )
}

export default Players