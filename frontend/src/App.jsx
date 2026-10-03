import { useEffect } from 'react'
import { Routes, Route, useLocation } from 'react-router-dom'

import Home from './pages/Home/Home'
import Players from './pages/Players/Players'
import PlayerDetail from './pages/PlayerDetail/PlayerDetail'
import About from './pages/About/About'

function ScrollToTop() {
  const { pathname } = useLocation()

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return null
}

function App() {
  return (
    <>
      <ScrollToTop />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tennis/players" element={<Players />} />
        <Route
          path="/tennis/players/:playerId"
          element={<PlayerDetail />}
        />
        <Route path="/about" element={<About />} />
      </Routes>
    </>
  )
}

export default App