import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import Header from '../../components/Header/Header'
import PlayerProfile from './components/PlayerProfile'
import PlayerRanking from './components/PlayerRanking'
import PlayerStatistics from './components/PlayerStatistics'
import PlayerMatches from './components/PlayerMatches'
import PlayerBio from './components/PlayerBio'

import './PlayerDetail.css'

const API_BASE_URL = 'http://127.0.0.1:8000'

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

function PlayerDetail() {
  const { playerId } = useParams()

  const [player, setPlayer] = useState(null)
  const [rankings, setRankings] = useState([])
  const [matches, setMatches] = useState([])
  const [stats, setStats] = useState([])
  const [bio, setBio] = useState(null)
  const [activeSection, setActiveSection] =
    useState('profile')

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