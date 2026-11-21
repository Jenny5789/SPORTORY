// 순위 이력 SVG 꺾은선 차트 (차트 라이브러리 없이 직접 좌표 계산)
// data: 날짜 오름차순 이력, valueKey: 표시할 값 필드, type: 'rank' | 'points'
function RankingChart({ data, valueKey, type = 'points' }) {
  if (data.length === 0) return null

  const width = 1000
  const height = 240
  const paddingX = 32
  const paddingY = 42
  const values = data.map((item) => item[valueKey])
  const minValue = Math.min(...values)
  const maxValue = Math.max(...values)
  // 모든 값이 같으면 범위 0, 0 나눗셈 방지용 1 사용
  const valueRange = maxValue - minValue || 1

  // 인덱스 기준 균등 가로 배치, 데이터 1건이면 가운데
  const getX = (index) => {
    if (data.length === 1) return width / 2
    return paddingX + (index / (data.length - 1)) * (width - paddingX * 2)
  }

  // 최솟값~최댓값을 차트 높이로 정규화 (SVG y축은 아래로 증가)
  // rank: 작은 값(상위 순위)을 위쪽, points: 큰 값을 위쪽에 배치
  const getY = (value) => {
    const normalized = (value - minValue) / valueRange
    const chartHeight = height - paddingY * 2

    if (type === 'rank') return paddingY + normalized * chartHeight
    return height - paddingY - normalized * chartHeight
  }

  const points = data
    .map((item, index) => `${getX(index)},${getY(item[valueKey])}`)
    .join(' ')

  // 7건 이상이면 처음, 마지막, 짝수 인덱스 날짜만 표시
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

      {/* 날짜 라벨: 'YYYY-MM-DD' → 'MM/DD' */}
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
