import { Link } from 'react-router-dom'
import './Header.css'

function Header({ variant = 'default' }) {
  const headerClassName =
    variant === 'overlay'
      ? 'site-header site-header--overlay'
      : 'site-header'

  return (
    <header className={headerClassName}>
      <Link to="/" className="site-wordmark">
        SPORT<span>ORY</span>
      </Link>

      <nav className="site-nav" aria-label="Main navigation">
        <Link to="/">Home</Link>

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