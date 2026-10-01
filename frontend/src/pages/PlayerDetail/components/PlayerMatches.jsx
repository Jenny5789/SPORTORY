import './PlayerMatches.css'

function formatEventType(eventType) {
  const eventTypeLabels = {
    GS: 'GRAND SLAM',
    1000: 'ATP MASTERS 1000',
    500: 'ATP 500',
    250: 'ATP 250',
    LVR: 'LAVER CUP',
    DC: 'DAVIS CUP',
  }

  return eventTypeLabels[eventType] || eventType
}

function formatTournamentDate(startDate, endDate) {
  if (!startDate || !endDate) return ''
  return `${startDate.replaceAll('-', '.')} — ${endDate.replaceAll('-', '.')}`
}

function getMatchSets(score) {
  if (!score) return []
  return Object.values(score).filter(
    (set) => set && set.player !== null && set.opponent !== null,
  )
}

function groupMatchesByTournament(matches) {
  const groups = []

  matches.forEach((match) => {
    const tournamentKey = [
      match.tournament.name,
      match.tournament.start_date,
      match.tournament.end_date,
    ].join('-')

    let group = groups.find((item) => item.key === tournamentKey)

    if (!group) {
      group = { key: tournamentKey, tournament: match.tournament, matches: [] }
      groups.push(group)
    }

    group.matches.push(match)
  })

  return groups
}

function PlayerMatches({ matches }) {
  const tournamentGroups = groupMatchesByTournament(matches)

  return (
    <section className="player-matches">
      <div className="player-matches-heading">
        <p>MATCHES</p>
        <h2>RECENT RESULTS</h2>
      </div>

      <div className="tournament-list">
        {tournamentGroups.map((group) => {
          const tournament = group.tournament

          return (
            <article className="tournament-block" key={group.key}>
              <header className="tournament-header">
                <div>
                  <span className="tournament-type">
                    {formatEventType(tournament.event_type)}
                  </span>
                  <h3>{tournament.name}</h3>
                </div>

                <div className="tournament-meta">
                  <span>{tournament.city}, {tournament.country}</span>
                  <span>{tournament.surface}</span>
                  <span>{tournament.indoor_outdoor === 'I' ? 'INDOOR' : 'OUTDOOR'}</span>
                  <span>{formatTournamentDate(tournament.start_date, tournament.end_date)}</span>
                </div>
              </header>

              <div className="match-list">
                {group.matches.map((match) => {
                  const sets = getMatchSets(match.score)

                  return (
                    <div className="match-row" key={`${group.key}-${match.source_match_id}`}>
                      <div className="match-round"><span>{match.round_name}</span></div>
                      <div className={`match-result match-result--${match.win_loss.toLowerCase()}`}>
                        {match.win_loss}
                      </div>

                      <div className="match-opponent">
                        <span className="match-opponent-label">VS</span>
                        <strong>{match.opponent.first_name} {match.opponent.last_name}</strong>
                        <span className="match-opponent-meta">
                          {match.opponent.nationality_code}
                          {match.opponent.rank ? ` · #${match.opponent.rank}` : ''}
                        </span>
                      </div>

                      <div className="match-score">
                        {sets.map((set, index) => (
                          <div className="match-set" key={`${match.source_match_id}-set-${index}`}>
                            <strong>{set.player}</strong>
                            <span>{set.opponent}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )
                })}
              </div>
            </article>
          )
        })}
      </div>
    </section>
  )
}

export default PlayerMatches
