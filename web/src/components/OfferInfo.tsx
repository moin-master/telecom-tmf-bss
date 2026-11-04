import { Link } from 'react-router-dom'
import type { OfferQuery } from '../api/generated/product-catalog/graphql'
import { humanize } from '../lib/format'
import { offerEmoji, offerTheme } from '../lib/theme'

export type OfferData = NonNullable<OfferQuery['productOffering']>

// The left panel: what the offer is. Everything about price and the bill is on the right.
export function OfferInfo({ offer }: { offer: OfferData }) {
  const theme = offerTheme(offer.category)
  const specs = offer.productSpecification?.productSpecCharacteristic ?? []

  return (
    <div className="detail__left">
      <div className="detail__art">
        <span className="offer__tag">{theme.label}</span>
        <span className="detail__emoji" aria-hidden="true">
          {offerEmoji(offer.name, theme)}
        </span>
      </div>

      <p className="kicker">{offer.productSpecification?.brand ?? 'vibe exclusive'}</p>
      <h1 className="detail__title">{offer.name}</h1>
      {offer.description && <p className="detail__desc">{offer.description}</p>}

      {offer.bundledProductOffering.length > 0 && (
        <>
          <h2 className="detail__h">Includes</h2>
          <ul className="chips chips--names" aria-label="includes">
            {offer.bundledProductOffering.map((b) => (
              <li key={b.id}>
                <Link to={`/offers/${b.id}`}>{b.name}</Link>
              </li>
            ))}
          </ul>
        </>
      )}

      {specs.length > 0 && (
        <>
          <h2 className="detail__h">Specs</h2>
          <dl className="specs-list">
            {specs.map((s) => (
              <div key={s.name}>
                <dt>{humanize(s.name)}</dt>
                <dd>{s.values.join(' / ')}</dd>
              </div>
            ))}
          </dl>
        </>
      )}
    </div>
  )
}
