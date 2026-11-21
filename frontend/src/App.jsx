/*
 * 라우트 정의
 * - /                          → /tennis/players 리다이렉트
 * - /home                      → Home
 * - /tennis/players            → 선수 목록
 * - /tennis/players/:playerId  → 선수 상세
 * - /about                     → About
 */
import { useEffect } from 'react'
import { Routes, Route, useLocation, Navigate } from 'react-router-dom'

import Home from './pages/Home/Home'
import Players from './pages/Players/Players'
import PlayerDetail from './pages/PlayerDetail/PlayerDetail'
import About from './pages/About/About'

// 경로(pathname) 변경 시 스크롤 최상단 이동 (클라이언트 라우팅은 이전 스크롤 위치 유지), 렌더링 요소 없음
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
        {/* 첫 접속 → Players */}
        <Route
          path="/"
          element={<Navigate to="/tennis/players" replace />}
        />

        {/* 기존 Home 유지 */}
        <Route path="/home" element={<Home />} />

        {/* Tennis */}
        <Route path="/tennis/players" element={<Players />} />
        <Route
          path="/tennis/players/:playerId"
          element={<PlayerDetail />}
        />

        {/* About */}
        <Route path="/about" element={<About />} />
      </Routes>
    </>
  )
}

export default App