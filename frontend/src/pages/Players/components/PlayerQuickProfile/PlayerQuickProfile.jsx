import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import './PlayerQuickProfile.css'

const API_BASE_URL = 'http://127.0.0.1:8000'

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

function FlipIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      aria-hidden="true"
    >
      <path d="M20 7v5h-5" />
      <path d="M4 17v-5h5" />
      <path d="M6.1 9A7 7 0 0 1 18 6.5L20 9" />
      <path d="M17.9 15A7 7 0 0 1 6 17.5L4 15" />
    </svg>
  )
}

function PlayerQuickProfile({ player, ranking, onClose }) {
  const [isFlipped, setIsFlipped] = useState(false)
  const [bio, setBio] = useState(null)
  const [bioLoading, setBioLoading] = useState(true)

  /* =========================================================
     KEYBOARD / BODY
  ========================================================= */

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    document.body.style.overflow = 'hidden'

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      document.body.style.overflow = ''
    }
  }, [onClose])

  /* =========================================================
     BIOGRAPHY
  ========================================================= */

  useEffect(() => {
    let cancelled = false

    async function loadBio() {
      setBioLoading(true)

      try {
        const response = await fetch(
          `${API_BASE_URL}/players/${player.player_id}/bio`,
        )

        if (!response.ok) {
          throw new Error('Failed to load bio')
        }

        const data = await response.json()

        if (!cancelled) {
          setBio(data)
        }
      } catch (error) {
        console.error('Failed to load player bio:', error)

        if (!cancelled) {
          setBio(null)
        }
      } finally {
        if (!cancelled) {
          setBioLoading(false)
        }
      }
    }

    loadBio()

    return () => {
      cancelled = true
    }
  }, [player.player_id])

  /* =========================================================
     STORY DATA
  ========================================================= */

  const allStoryItems = useMemo(() => {
    if (!bio) return []

    const personal = Array.isArray(bio.personal)
      ? bio.personal.map((item) => ({
          ...item,
          storyCategory: 'PERSONAL',
        }))
      : []

    const career = Array.isArray(bio.career)
      ? bio.career.map((item) => ({
          ...item,
          storyCategory: 'CAREER',
        }))
      : []

    return [...personal, ...career]
      .filter((item) => item.translated_text)
  }, [bio])

  const [storyItems, setStoryItems] = useState([])

  const pickRandomStories = () => {
    const shuffledStories = [...allStoryItems]

    for (
      let i = shuffledStories.length - 1;
      i > 0;
      i -= 1
    ) {
      const randomIndex = Math.floor(
        Math.random() * (i + 1),
      )

      ;[
        shuffledStories[i],
        shuffledStories[randomIndex],
      ] = [
        shuffledStories[randomIndex],
        shuffledStories[i],
      ]
    }

    setStoryItems(shuffledStories.slice(0, 3))
  }

  /* =========================================================
     CARD ACTIONS
  ========================================================= */

  const handleCardClick = () => {
    // SPORT → STORY로 뒤집을 때마다
    // 새로운 Biography 3개 선택
    if (!isFlipped) {
      pickRandomStories()
    }

    setIsFlipped((current) => !current)
  }

  const handleCardKeyDown = (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault()

      if (!isFlipped) {
        pickRandomStories()
      }

      setIsFlipped((current) => !current)
    }
  }

  const stopCardAction = (event) => {
    event.stopPropagation()
  }

  /* =========================================================
     RENDER
  ========================================================= */

  return (
    <div
      className="quick-profile-overlay"
      role="dialog"
      aria-modal="true"
      aria-label={`${player.first_name} ${player.last_name} quick profile`}
      onMouseDown={onClose}
    >
      <div
        className={`quick-profile-flip ${
          isFlipped ? 'is-flipped' : ''
        }`}
        onMouseDown={stopCardAction}
        onClick={handleCardClick}
        onKeyDown={handleCardKeyDown}
        role="button"
        tabIndex={0}
        aria-label={
          isFlipped
            ? 'Flip back to player profile'
            : 'Flip to player story'
        }
      >
        <div className="quick-profile-inner">

          {/* =================================================
              FRONT — SPORT
          ================================================= */}

          <article className="quick-profile-face quick-profile-front">
            <button
              type="button"
              className="quick-profile-close"
              onClick={(event) => {
                event.stopPropagation()
                onClose()
              }}
              aria-label="Close player profile"
            >
              ×
            </button>

            <div className="quick-profile-front-copy">
              <div className="quick-profile-top">
                <p className="quick-profile-eyebrow">
                  SPORT / PLAYER PROFILE
                </p>

                <div className="quick-profile-flip-guide">
                  <FlipIcon />
                  <span>FLIP TO STORY</span>
                </div>
              </div>

              <div className="quick-profile-name">
                <p>{player.nationality}</p>

                <h2>
                  <span>{player.first_name}</span>
                  <span>{player.last_name}</span>
                </h2>
              </div>

              <div>
                <div className="quick-profile-facts">
                  <div>
                    <span>ATP RANKING</span>

                    <strong>
                      {ranking?.singles_rank
                        ? `#${String(
                            ranking.singles_rank,
                          ).padStart(2, '0')}`
                        : '—'}
                    </strong>
                  </div>

                  <div>
                    <span>POINTS</span>

                    <strong>
                      {ranking?.singles_points != null
                        ? Number(
                            ranking.singles_points,
                          ).toLocaleString()
                        : '—'}
                    </strong>
                  </div>

                  <div>
                    <span>PLAYS</span>

                    <strong>
                      {player.play_hand || '—'}
                    </strong>
                  </div>
                </div>

                <Link
                  to={`/tennis/players/${player.player_id}`}
                  className="quick-profile-detail-link"
                  onClick={stopCardAction}
                >
                  <span>VIEW FULL PROFILE</span>
                  <ArrowIcon />
                </Link>
              </div>
            </div>

            <div className="quick-profile-front-visual">
              <span className="quick-profile-rank-bg">
                {ranking?.singles_rank
                  ? String(
                      ranking.singles_rank,
                    ).padStart(2, '0')
                  : ''}
              </span>

              <img
                src={`${API_BASE_URL}${player.image_url}`}
                alt={`${player.first_name} ${player.last_name}`}
              />
            </div>
          </article>

          {/* =================================================
              BACK — STORY
          ================================================= */}

          <article className="quick-profile-face quick-profile-back">
            <button
              type="button"
              className="quick-profile-close"
              onClick={(event) => {
                event.stopPropagation()
                onClose()
              }}
              aria-label="Close player story"
            >
              ×
            </button>

            <div className="quick-story">
              <div className="quick-story-header">
                <div>
                  <p className="quick-profile-eyebrow">
                    STORY / BIOGRAPHY
                  </p>

                  <h2>
                    {player.first_name}
                    <br />
                    {player.last_name}
                  </h2>
                </div>

                <div className="quick-profile-flip-guide">
                  <FlipIcon />
                  <span>BACK TO SPORT</span>
                </div>
              </div>

              <div className="quick-story-divider" />

              <div className="quick-story-body">
                <div className="quick-story-intro">
                  <span>BEYOND THE NUMBERS</span>

                  <p>
                    기록 너머의 선수 이야기를
                    SPORTORY가 수집한 Biography를 통해
                    살펴봅니다.
                  </p>
                </div>

                <div
                  className="quick-story-list"
                  onClick={stopCardAction}
                  onMouseDown={stopCardAction}
                >
                  {bioLoading && (
                    <p className="quick-story-status">
                      Loading story...
                    </p>
                  )}

                  {!bioLoading &&
                    storyItems.length === 0 && (
                      <p className="quick-story-status">
                        Story information is not available.
                      </p>
                    )}

                  {!bioLoading &&
                    storyItems.map((item, index) => (
                      <article
                        className="quick-story-item"
                        key={`${item.storyCategory}-${
                          item.item_order ?? index
                        }`}
                      >
                        <div className="quick-story-meta">
                          <span>
                            {String(index + 1).padStart(
                              2,
                              '0',
                            )}
                          </span>

                          <strong>
                            {item.storyCategory}
                          </strong>
                        </div>

                        <p>{item.translated_text}</p>
                      </article>
                    ))}
                </div>
              </div>

              <Link
                to={`/tennis/players/${player.player_id}`}
                className="quick-profile-detail-link quick-story-detail-link"
                onClick={stopCardAction}
              >
                <span>CONTINUE TO FULL PROFILE</span>
                <ArrowIcon />
              </Link>
            </div>
          </article>

        </div>
      </div>
    </div>
  )
}

export default PlayerQuickProfile