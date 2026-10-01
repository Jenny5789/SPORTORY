import { useMemo, useState } from 'react'

import './PlayerBio.css'

function PlayerBio({ bio }) {
  const [category, setCategory] = useState('personal')
  const [language, setLanguage] = useState('ko')

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