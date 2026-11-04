import type { CSSProperties } from 'react'
import { Link } from 'react-router-dom'
import type { OffersQuery } from '../api/generated/product-catalog/graphql'
import { headlinePrice, humanize, money, otherPrices, perLabel } from '../lib/format'
import { offerEmoji, offerTheme } from '../lib/theme'
import { AddToCartButton } from './AddToCartButton'

export type Offer = OffersQuery['productOfferingList'][number]

export function OfferCard({ offer, index }: { offer: Offer; index: number }) {
  const theme = offerTheme(offer.category)
  const prices = offer.productOfferingPrice
  const headline = headlinePrice(prices)
  const extras = otherPrices(prices, headline)
  const specs = offer.productSpecification?.productSpecCharacteristic ?? []

  return (
    <article className="offer" data-theme={theme.key} style={{ '--i': index % 8 } as CSSProperties}>
      <Link to={`/offers/${offer.id}`} className="offer__media" aria-label={`${offer.name}, details`}>
        <span className="offer__tag">{theme.label}</span>
        <span className="offer__emoji" aria-hidden="true">
          {offerEmoji(offer.name, theme)}
        </span>
      </Link>

      <div className="offer__body">
        <h3 className="offer__name">
          <Link to={`/offers/${offer.id}`}>{offer.name}</Link>
        </h3>
        {offer.description && <p className="offer__desc">{offer.description}</p>}

        {specs.length > 0 && (
          <ul className="chips" aria-label="specs">
            {specs.map((s) => (
              <li key={s.name}>
                {humanize(s.name)} · {s.values.join(' / ')}
              </li>
            ))}
          </ul>
        )}

        <div className="offer__price">
          {headline?.price && (
            <p className="offer__amount">
              <strong>{money(headline.price.unit, headline.price.value)}</strong>
              <span>{perLabel(headline.recurringChargePeriodType)}</span>
            </p>
          )}
          {extras.length > 0 && (
            <ul className="offer__fees">
              {extras.map((p) => (
                <li key={p.id}>
                  + {p.name.toLowerCase()}{' '}
                  <b>
                    {money(p.price!.unit, p.price!.value)}
                    {perLabel(p.recurringChargePeriodType)}
                  </b>
                </li>
              ))}
            </ul>
          )}
        </div>

        <AddToCartButton offering={offer} sellable={offer.isSellable} />
      </div>
    </article>
  )
}
