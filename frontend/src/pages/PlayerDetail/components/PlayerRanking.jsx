// 선수 상세 Ranking 섹션: 현재 단식, Race 순위와 단식 순위, 포인트 이력 차트
import RankingChart from './RankingChart'
import './PlayerRanking.css'

// rankings: GET /players/{player_id}/rankings 응답, rank_date 내림차순 (API 기본 최근 10건)
function PlayerRanking({ rankings }) {
  if (rankings.length === 0) return null

  // [0]: 최신 순위, reverse: 차트용 과거 → 최신 순서
  const currentRanking = rankings[0]
  const rankingHistory = [...rankings].reverse()

  return (
    <section className="player-ranking">
      <div className="player-ranking-heading">
        <p>RANKING</p>
        <h2>CURRENT</h2>
      </div>

      <div className="player-ranking-current">
        <div className="ranking-current-item">
          <span className="ranking-label">SINGLES</span>
          <strong className="ranking-number">
            #{String(currentRanking.singles_rank).padStart(2, '0')}
          </strong>
          <span className="ranking-points">
            {currentRanking.singles_points.toLocaleString()} PTS
          </span>
        </div>

        <div className="ranking-current-item">
          <span className="ranking-label">RACE</span>
          <strong className="ranking-number">
            #{String(currentRanking.race_rank).padStart(2, '0')}
          </strong>
          <span className="ranking-points">
            {currentRanking.race_points.toLocaleString()} PTS
          </span>
        </div>

        <p className="ranking-date">AS OF {currentRanking.rank_date}</p>
      </div>

      <div className="ranking-history">
        <div className="ranking-history-heading">
          <p>RANKING HISTORY</p>
          <span>
            {rankingHistory[0]?.rank_date} — {rankingHistory[rankingHistory.length - 1]?.rank_date}
          </span>
        </div>

        <div className="ranking-history-block">
          <div className="ranking-history-label">
            <span>SINGLES RANK</span>
            <strong>#{String(currentRanking.singles_rank).padStart(2, '0')}</strong>
          </div>
          <RankingChart data={rankingHistory} valueKey="singles_rank" type="rank" />
        </div>

        <div className="ranking-history-block">
          <div className="ranking-history-label">
            <span>SINGLES POINTS</span>
            <strong>{currentRanking.singles_points.toLocaleString()}</strong>
          </div>
          <RankingChart data={rankingHistory} valueKey="singles_points" type="points" />
        </div>
      </div>
    </section>
  )
}

export default PlayerRanking
