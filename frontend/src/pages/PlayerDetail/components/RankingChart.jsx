function RankingChart({ data, valueKey, type = 'points' }) {
  if (data.length === 0) return null

  const width = 1000
  const height = 240
  const paddingX = 32
  const paddingY = 42
  const values = data.map((item) => item[valueKey])
  const minValue = Math.min(...values)
  const maxValue = Math.max(...values)
  const valueRange = maxValue - minValue || 1

  const getX = (index) => {
    if (data.length === 1) return width / 2
    return paddingX + (index / (data.length - 1)) * (width - paddingX * 2)
  }

  const getY = (value) => {
    const normalized = (value - minValue) / valueRange
    const chartHeight = height - paddingY * 2

    if (type === 'rank') return paddingY + normalized * chartHeight
    return height - paddingY - normalized * chartHeight
  }

  const points = data
    .map((item, index) => `${getX(index)},${getY(item[valueKey])}`)
    .join(' ')

  const shouldShowDate = (index) => {
    if (data.length <= 6) return true
    return index === 0 || index === data.length - 1 || index % 2 === 0
  }

  return (
    <div className="ranking-chart">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={type === 'rank' ? 'Singles ranking history' : 'Singles points history'}
      >
        <line
          className="ranking-chart-guide"
          x1={paddingX}
          y1={height / 2}
          x2={width - paddingX}
          y2={height / 2}
        />
        <polyline className="ranking-chart-line" points={points} />

        {data.map((item, index) => {
          const x = getX(index)
          const y = getY(item[valueKey])

          return (
            <g key={`${item.rank_date}-${valueKey}`}>
              <circle className="ranking-chart-point" cx={x} cy={y} r="6" />
              <text className="ranking-chart-value" x={x} y={y - 18} textAnchor="middle">
                {type === 'rank' ? `#${item[valueKey]}` : item[valueKey].toLocaleString()}
              </text>
            </g>
          )
        })}
      </svg>

      <div
        className="ranking-chart-dates"
        style={{ gridTemplateColumns: `repeat(${data.length}, 1fr)` }}
      >
        {data.map((item, index) => (
          <span key={item.rank_date}>
            {shouldShowDate(index) ? item.rank_date.slice(5).replace('-', '/') : ''}
          </span>
        ))}
      </div>
    </div>
  )
}

export default RankingChart
