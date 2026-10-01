import './PlayerStatistics.css'

function PlayerStatistics({ stats }) {
  const careerStats = stats.find(
    (item) => item.category === 'Career' && item.surface === 'ALL',
  )

  if (!careerStats) return null

  return (
    <section className="player-statistics">
      <div className="player-statistics-heading">
        <p>STATISTICS</p>
        <h2>CAREER</h2>
      </div>

      <div className="statistics-context">
        <span>ALL SURFACES</span>
        <span>AS OF {careerStats.rank_date}</span>
      </div>

      <div className="statistics-overall">
        <span className="statistics-overall-label">TOTAL POINTS WON</span>
        <strong>{careerStats.total_points_won_percentage}<small>%</small></strong>
        <p>CAREER · ALL SURFACES</p>
      </div>

      <div className="statistics-group">
        <div className="statistics-group-heading"><span>01</span><h3>SERVE</h3></div>
        <div className="statistics-grid">
          <div className="stat-item stat-item--large"><strong>{careerStats.aces.toLocaleString()}</strong><span>ACES</span></div>
          <div className="stat-item"><strong>{careerStats.first_serve_percentage}<small>%</small></strong><span>1ST SERVE IN</span></div>
          <div className="stat-item"><strong>{careerStats.first_serve_points_won_percentage}<small>%</small></strong><span>1ST SERVE POINTS WON</span></div>
          <div className="stat-item"><strong>{careerStats.second_serve_points_won_percentage}<small>%</small></strong><span>2ND SERVE POINTS WON</span></div>
          <div className="stat-item"><strong>{careerStats.service_games_won_percentage}<small>%</small></strong><span>SERVICE GAMES WON</span></div>
          <div className="stat-item"><strong>{careerStats.break_points_saved_percentage}<small>%</small></strong><span>BREAK POINTS SAVED</span></div>
          <div className="stat-item"><strong>{careerStats.service_points_won_percentage}<small>%</small></strong><span>SERVICE POINTS WON</span></div>
        </div>

        <div className="statistics-secondary">
          <div><span>DOUBLE FAULTS</span><strong>{careerStats.double_faults.toLocaleString()}</strong></div>
          <div><span>BREAK POINTS FACED</span><strong>{careerStats.break_points_faced.toLocaleString()}</strong></div>
          <div><span>SERVICE GAMES PLAYED</span><strong>{careerStats.service_games_played.toLocaleString()}</strong></div>
        </div>
      </div>

      <div className="statistics-group">
        <div className="statistics-group-heading"><span>02</span><h3>RETURN</h3></div>
        <div className="statistics-grid statistics-grid--return">
          <div className="stat-item"><strong>{careerStats.first_serve_return_points_won_percentage}<small>%</small></strong><span>1ST SERVE RETURN POINTS WON</span></div>
          <div className="stat-item"><strong>{careerStats.second_serve_return_points_won_percentage}<small>%</small></strong><span>2ND SERVE RETURN POINTS WON</span></div>
          <div className="stat-item"><strong>{careerStats.break_points_converted_percentage}<small>%</small></strong><span>BREAK POINTS CONVERTED</span></div>
          <div className="stat-item"><strong>{careerStats.return_games_won_percentage}<small>%</small></strong><span>RETURN GAMES WON</span></div>
          <div className="stat-item"><strong>{careerStats.return_points_won_percentage}<small>%</small></strong><span>RETURN POINTS WON</span></div>
        </div>

        <div className="statistics-secondary">
          <div><span>BREAK POINT OPPORTUNITIES</span><strong>{careerStats.break_points_opportunities.toLocaleString()}</strong></div>
          <div><span>RETURN GAMES PLAYED</span><strong>{careerStats.return_games_played.toLocaleString()}</strong></div>
        </div>
      </div>
    </section>
  )
}

export default PlayerStatistics
