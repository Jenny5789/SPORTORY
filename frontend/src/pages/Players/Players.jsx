import { useEffect, useMemo, useState } from 'react'

import Header from '../../components/Header/Header'
import PlayerQuickProfile from './components/PlayerQuickProfile/PlayerQuickProfile'

import './Players.css'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

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

function Players() {
  const [players, setPlayers] = useState([])
  const [rankings, setRankings] = useState({})
  const [selectedPlayer, setSelectedPlayer] = useState(null)
  const [loading, setLoading] = useState(true)

  /* =========================================================
     LOAD PLAYERS + LATEST RANKING
  ========================================================= */

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

        const rankingResults = await Promise.all(
          playerData.map(async (player) => {
            try {
              const rankingResponse = await fetch(
                `${API_BASE_URL}/players/${player.player_id}/rankings?limit=1`,
              )

              if (!rankingResponse.ok) {
                return [player.player_id, null]
              }

              const rankingData =
                await rankingResponse.json()

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
        setRankings(
          Object.fromEntries(rankingResults),
        )
      } catch (error) {
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

  /* =========================================================
     SORT BY ATP RANKING
  ========================================================= */

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

  /* =========================================================
     LOADING
  ========================================================= */

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

  /* =========================================================
     PAGE
  ========================================================= */

  return (
    <>
      <Header />

      <main className="players-page">

        {/* ===================================================
            INTRO
        =================================================== */}

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

        {/* ===================================================
            ALL PLAYERS
        =================================================== */}

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

      {/* =====================================================
          QUICK PROFILE
      ===================================================== */}

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