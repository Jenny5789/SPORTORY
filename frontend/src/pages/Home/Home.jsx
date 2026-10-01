import { useRef } from 'react'
import { Link } from 'react-router-dom'

import Header from '../../components/Header/Header'
import './Home.css'

import homeHero from '../../assets/home/home_hero.png'
import tennisImg from '../../assets/home/sport_tennis.png'
import footballImg from '../../assets/home/sport_football.png'
import basketballImg from '../../assets/home/sport_basketball.png'
import baseballImg from '../../assets/home/sport_baseball.png'
import cyclingImg from '../../assets/home/sport_cycling.png'
import runningImg from '../../assets/home/sport_running.png'

function Home() {
  const railRef = useRef(null)

  const scrollRail = (direction) => {
    railRef.current?.scrollBy({
      left: direction * 380,
      behavior: 'smooth',
    })
  }

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

  const scrollToSports = () => {
    document
      .getElementById('explore-sports')
      ?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <div className="home-page">
      <Header variant="overlay" />

      <section className="hero">
        <img
          src={homeHero}
          alt="People participating in several different sports"
        />

        <div className="hero-scrim" />

        <div className="hero-copy">
          <p className="eyebrow">Sports + Story</p>

          <h1 className="display">
            SPORTS CREATE
            <br />
            <em>MORE STORIES</em>
          </h1>

          <p>
            스포츠는 경기 그 이상입니다. <br /> 
            사람, 기록, 그리고 이야기가 모이는 곳, <br />
            SPORTORY.
          </p>

          <button className="cta" onClick={scrollToSports}>
            Explore sports

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
      </section>

      <section className="explore" id="explore-sports">
        <div className="explore-head">
          <div>
            <h2>EXPLORE SPORTS</h2>
            <p>다양한 스포츠의 선수, 기록, 이야기를 만나보세요.</p>
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

        <div className="rail" ref={railRef}>
          {sports.map((sport) => {
            const tile = (
              <>
                <img src={sport.image} alt={sport.name} />

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

                  <span className="status">{sport.status}</span>
                </div>
              </>
            )

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
              <div className="tile" key={sport.name}>
                {tile}
              </div>
            )
          })}
        </div>
      </section>
    </div>
  )
}

export default Home