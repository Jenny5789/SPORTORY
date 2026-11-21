// 선수 상세 Biography 섹션: PERSONAL, CAREER 분류 탭과 KO, EN 언어 전환
import { useMemo, useState } from 'react'

import './PlayerBio.css'

// bio: GET /players/{player_id}/bio 응답 ({ personal: [], career: [] })
function PlayerBio({ bio }) {
  const [category, setCategory] = useState('personal')
  const [language, setLanguage] = useState('ko')

  // 선택 분류 항목을 item_order 순 정렬
  // KO: 번역문 우선, EN: 원문 우선, 선택 언어 문장이 없으면 다른 언어로 대체, 빈 항목 제외
  const stories = useMemo(() => {
    const items = bio?.[category] ?? []

    return [...items]
      .sort(
        (a, b) =>
          (a.item_order ?? 0) - (b.item_order ?? 0),
      )
      .map((item) => ({
        id: item.item_order,
        text:
          language === 'ko'
            ? item.translated_text || item.original_text
            : item.original_text || item.translated_text,
      }))
      .filter((item) => item.text)
  }, [bio, category, language])

  // bio 미수신 시 섹션 생략 (Hook 호출 이후에 반환)
  if (!bio) {
    return null
  }

  return (
    <section
      id="biography"
      className="player-bio"
    >
      <div className="player-bio-header">
        <div>
          <p className="player-bio-kicker">
            BIOGRAPHY
          </p>

          <h2>
            BEYOND
            <br />
            THE NUMBERS
          </h2>
        </div>

        <div className="player-bio-controls">
          <div className="player-bio-tabs">
            <button
              type="button"
              className={
                category === 'personal'
                  ? 'is-active'
                  : ''
              }
              onClick={() =>
                setCategory('personal')
              }
            >
              PERSONAL
            </button>

            <button
              type="button"
              className={
                category === 'career'
                  ? 'is-active'
                  : ''
              }
              onClick={() =>
                setCategory('career')
              }
            >
              CAREER
            </button>
          </div>

          <div className="player-bio-tabs">
            <button
              type="button"
              className={
                language === 'ko'
                  ? 'is-active'
                  : ''
              }
              onClick={() => setLanguage('ko')}
            >
              KO
            </button>

            <button
              type="button"
              className={
                language === 'en'
                  ? 'is-active'
                  : ''
              }
              onClick={() => setLanguage('en')}
            >
              EN
            </button>
          </div>
        </div>
      </div>

      <div className="player-bio-reading">
        {stories.length > 0 ? (
          <article className="player-bio-article">
            {stories.map((story, index) => (
              <p key={`${category}-${story.id ?? index}`}>
                {story.text}
              </p>
            ))}
          </article>
        ) : (
          <p className="player-bio-empty">
            Biography is not available.
          </p>
        )}
      </div>
    </section>
  )
}

export default PlayerBio