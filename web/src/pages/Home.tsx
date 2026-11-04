import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { OfferCard } from '../components/OfferCard'
import { ErrorState, OfferSkeletons, StateCard } from '../components/StateViews'
import { useCategories, useOffers } from '../hooks/useOffers'

export function Home() {
  const [params, setParams] = useSearchParams()
  const categoryId = params.get('cat') ?? ''
  const urlQuery = params.get('q') ?? ''
  const [text, setText] = useState(urlQuery)

  // Keep the search in the URL, a moment after typing stops.
  useEffect(() => {
    const timer = window.setTimeout(() => {
      setParams(
        (prev) => {
          const next = new URLSearchParams(prev)
          if (text.trim()) next.set('q', text.trim())
          else next.delete('q')
          return next
        },
        // Filtering changes the URL but not the page: keep the scroll position.
        { replace: true, preventScrollReset: true },
      )
    }, 300)
    return () => window.clearTimeout(timer)
  }, [text, setParams])

  const categories = useCategories()
  const offers = useOffers({ name: urlQuery, categoryId })

  const pickCategory = (id: string) =>
    setParams(
      (prev) => {
        const next = new URLSearchParams(prev)
        if (id) next.set('cat', id)
        else next.delete('cat')
        return next
      },
      { preventScrollReset: true },
    )

  return (
    <>
      <section className="hero wrap">
        <div className="hero__copy">
          <p className="pill">
            <span className="pill__dot" aria-hidden="true" /> Live offers from the catalog
          </p>
          <h1 className="hero__title">
            Plans and phones, <span className="mark">priced clearly</span>.
          </h1>
          <p className="hero__sub">
            Browse the current offers, compare prices and add what you want to a cart in one step. No account needed.
          </p>
          <div className="hero__cta">
            <a href="#shop" className="btn btn--big">
              Browse offers
            </a>
            <ul className="trust">
              <li>No account needed</li>
              <li>Live prices</li>
              <li>One-step cart</li>
            </ul>
          </div>
        </div>

        <div className="hero__art" aria-hidden="true">
          <div className="art-card art-card--main">
            <span className="art-emoji">📱</span>
          </div>
          <div className="art-card art-card--plan">
            <span className="art-tile">📶</span>
            <b>Plans</b>
          </div>
          <div className="art-card art-card--addon">
            <span className="art-tile">✈️</span>
            <b>Add-ons</b>
          </div>
          <div className="art-chip">
            <i /> Live prices
          </div>
        </div>
      </section>

      <div className="band">
        <section id="shop" className="wrap shop" aria-labelledby="shop-title">
          <div className="shop__head">
            <h2 id="shop-title" className="shop__title">
              Browse offers
            </h2>
            <p className="shop__sub">Everything below is live from the catalog.</p>
          </div>

          <div className="controls">
            <form role="search" className="search" onSubmit={(e) => e.preventDefault()}>
              <label htmlFor="q" className="sr-only">
                Search offers
              </label>
              <svg className="search__icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
                <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2" />
                <path d="m20 20-3.5-3.5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
              <input
                id="q"
                type="search"
                placeholder="Search plans, phones, SIMs…"
                value={text}
                onChange={(e) => setText(e.target.value)}
                autoComplete="off"
              />
            </form>

            <ul className="cats" aria-label="Categories">
              <li>
                <button type="button" className="cat" aria-pressed={!categoryId} onClick={() => pickCategory('')}>
                  All
                </button>
              </li>
              {categories.data?.map((c) => (
                <li key={c.id}>
                  <button
                    type="button"
                    className="cat"
                    aria-pressed={categoryId === c.id}
                    onClick={() => pickCategory(c.id)}
                  >
                    {c.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {offers.isPending && <OfferSkeletons />}
          {offers.isError && <ErrorState error={offers.error} onRetry={() => offers.refetch()} />}

          {offers.data && offers.data.length === 0 && (
            <StateCard
              emoji="🫥"
              title="Nothing here yet"
              action={
                <button
                  type="button"
                  className="btn"
                  onClick={() => {
                    setText('')
                    pickCategory('')
                  }}
                >
                  Clear filters
                </button>
              }
            >
              No offers match that. Try another word or category.
            </StateCard>
          )}

          {offers.data && offers.data.length > 0 && (
            <>
              <div className="grid">
                {offers.data.map((offer, i) => (
                  <OfferCard key={offer.id} offer={offer} index={i} />
                ))}
              </div>
              {offers.hasNextPage && (
                <div className="more">
                  <button
                    type="button"
                    className="btn btn--ghost btn--big"
                    onClick={() => offers.fetchNextPage()}
                    disabled={offers.isFetchingNextPage}
                  >
                    {offers.isFetchingNextPage ? 'Loading…' : 'Show more offers'}
                  </button>
                </div>
              )}
            </>
          )}
        </section>
      </div>
    </>
  )
}
