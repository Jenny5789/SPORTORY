import './PlayerProfile.css'

const API_BASE_URL = 'http://127.0.0.1:8000'

function PlayerProfile({ player }) {
  return (
    <section className="player-profile">
      <div className="player-profile-content">
        <p className="player-profile-country">
          {player.nationality}
        </p>

        <h1>
          <span>{player.first_name}</span>
          <span>{player.last_name}</span>
        </h1>

        <div className="player-profile-facts">
          <div>
            <span className="fact-label">
              BORN
            </span>

            <strong>
              {player.birth_date || '—'}
            </strong>
          </div>

          <div>
            <span className="fact-label">
              HEIGHT
            </span>

            <strong>
              {player.height_cm
                ? `${player.height_cm} cm`
                : '—'}
            </strong>
          </div>

          <div>
            <span className="fact-label">
              WEIGHT
            </span>

            <strong>
              {player.weight_kg
                ? `${player.weight_kg} kg`
                : '—'}
            </strong>
          </div>

          <div>
            <span className="fact-label">
              PLAYS
            </span>

            <strong>
              {player.play_hand || '—'}
            </strong>
          </div>

          <div>
            <span className="fact-label">
              BACKHAND
            </span>

            <strong>
              {player.backhand || '—'}
            </strong>
          </div>

          <div>
            <span className="fact-label">
              PRO SINCE
            </span>

            <strong>
              {player.pro_year || '—'}
            </strong>
          </div>
        </div>
      </div>

      <div className="player-profile-visual">
        {player.image_url && (
          <img
            src={`${API_BASE_URL}${player.image_url}`}
            alt={`${player.first_name} ${player.last_name}`}
          />
        )}
      </div>
    </section>
  )
}

export default PlayerProfile