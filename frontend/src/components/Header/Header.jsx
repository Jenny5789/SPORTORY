// 공통 상단 헤더: 워드마크, Home, Sports 드롭다운(Tennis), About 링크
import { Link } from 'react-router-dom'
import './Header.css'

// variant: 'overlay' 지정 시 site-header--overlay 클래스 추가 (Home 히어로 위 배치용)
function Header({ variant = 'default' }) {
  const headerClassName =
    variant === 'overlay'
      ? 'site-header site-header--overlay'
      : 'site-header'

  return (
    <header className={headerClassName}>
      <Link to="/home" className="site-wordmark">
        SPORT<span>ORY</span>
      </Link>

      <nav className="site-nav" aria-label="Main navigation">
        <Link to="/home">Home</Link>

        <div className="site-nav-sports">
          <button type="button" className="site-nav-sports-trigger">
            Sports
            <span className="site-nav-arrow">▾</span>
          </button>

          <div className="site-nav-dropdown">
            <Link to="/tennis/players">Tennis</Link>
          </div>
        </div>

        <Link to="/about">About</Link>
      </nav>
    </header>
  )
}

export default Header