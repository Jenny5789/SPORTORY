import { Link } from 'react-router-dom'

import Header from '../../components/Header/Header'
import './About.css'

function About() {
  return (
    <main className="about-page">
      <Header />

      {/* =====================================================
          HERO
      ===================================================== */}
      <section className="about-hero">
        <div className="about-hero-index">
          <span>ABOUT SPORTORY</span>
          <span>SPORTS + STORY</span>
        </div>

        <div className="about-hero-title">
          <h1>
            BEYOND
            <br />
            THE <span>NUMBERS.</span>
          </h1>
        </div>

        <div className="about-hero-bottom">
          <p className="about-hero-kicker">
            SPORTS
            <span>+</span>
            STORY
          </p>

          <p className="about-hero-description">
            스포츠의 기록을 넘어,
            <br />
            선수와 경기 속 이야기를
            <br />
            데이터로 연결합니다.
          </p>
        </div>
      </section>

      {/* =====================================================
          WHAT IS SPORTORY
      ===================================================== */}
      <section className="about-intro">
        <div className="about-section-label">
          <span>01</span>
          <span>WHAT IS SPORTORY</span>
        </div>

        <div className="about-intro-content">
          <p className="about-intro-lead">
            SPORTORY는
            <br />
            <strong>SPORTS</strong>
            <span className="about-inline-plus"> + </span>
            <strong>STORY</strong>를
            <br />
            연결합니다.
          </p>

          <div className="about-intro-copy">
            <p>
              선수, 경기, 기록 등 다양한 스포츠 데이터를
              수집하고 연결해 단순한 숫자를 넘어 스포츠를
              이해할 수 있는 정보로 전달합니다.
            </p>

            <p>
              하나의 기록이 선수의 커리어와 연결되고,
              하나의 경기가 더 큰 이야기의 일부가 되는 것.
              SPORTORY는 그 연결을 보여주고자 합니다.
            </p>
          </div>
        </div>
      </section>

      {/* =====================================================
          DATA TO STORY
      ===================================================== */}
      <section className="about-data">
        <div className="about-section-label about-section-label--dark">
          <span>02</span>
          <span>DATA TO STORY</span>
        </div>

        <div className="about-data-simple">
          <div className="about-data-copy">
            <span>SPORTS DATA</span>

            <p>
              선수의 프로필, 랭킹, 경기와 통계는
              <br />
              각각 떨어져 있는 숫자가 아닙니다.
            </p>
          </div>

          <div className="about-data-message">
            <h2>
              DATA
              <br />
              BECOMES
              <br />
              <span>STORY.</span>
            </h2>

            <p>
              데이터를 서로 연결해
              <br />
              선수와 스포츠를 이해할 수 있는
              <br />
              맥락으로 전달합니다.
            </p>
          </div>
        </div>
      </section>

      {/* =====================================================
          TENNIS — FIRST STORY
      ===================================================== */}
      <section className="about-tennis">
        <div className="about-section-label">
          <span>03</span>
          <span>THE FIRST STORY</span>
        </div>

        <div className="about-tennis-layout">
          <div className="about-tennis-title">
            <span>CURRENTLY AVAILABLE</span>

            <h2>
              TENNIS
              <span className="about-tennis-dot">.</span>
            </h2>
          </div>

          <div className="about-tennis-copy">
            <p className="about-tennis-lead">
              SPORTORY의 첫 번째 스포츠는
              <strong> Tennis</strong>입니다.
            </p>

            <p>
              현재 ATP 선수 데이터를 기반으로 선수의 기본 정보부터
              랭킹 변화, 경기 기록, 통계 그리고 Biography까지
              하나의 흐름으로 제공합니다.
            </p>

            <Link
              to="/tennis/players"
              className="about-tennis-link"
            >
              EXPLORE TENNIS
              <span>→</span>
            </Link>
          </div>
        </div>
      </section>

      {/* =====================================================
          ENDING
      ===================================================== */}
      <section className="about-ending">
        <p>SPORTS + STORY</p>

        <h2>
          EVERY RECORD
          <br />
          HAS A <span>STORY.</span>
        </h2>

        <div className="about-ending-wordmark">
          SPORT<span>ORY</span>
        </div>
      </section>
    </main>
  )
}

export default About