import { useState, type CSSProperties } from 'react'
import { Link } from 'react-router-dom'
import type { OffersQuery } from '../api/generated/product-catalog/graphql'
import { headlinePrice, humanize, money, otherPrices, perLabel } from '../lib/format'
import { optionsOf, preview, pricesFor, type PurchaseOption } from '../lib/purchase'
import { offerEmoji, offerTheme } from '../lib/theme'
import { AddToCartButton } from './AddToCartButton'
import { ProtectionAddOn } from './ProtectionAddOn'
import { PurchaseOptions } from './PurchaseOptions'

export type Offer = OffersQuery['productOfferingList'][number]

export function OfferCard({ offer, index }: { offer: Offer; index: number }) {
  const theme = offerTheme(offer.category)
  const [option, setOption] = useState<PurchaseOption>('own')
  const [withAddOn, setWithAddOn] = useState(false)
  const addOn = offer.productOfferingRelationship.find((r) => r.relationshipType === 'addOn')
  const available = optionsOf(offer.productOfferingPrice)
  const hasOptions = available.length > 0
  const prices = hasOptions ? pricesFor(offer.productOfferingPrice, option) : offer.productOfferingPrice
  const headline = headlinePrice(prices)
  const extras = otherPrices(prices, headline)
  const sum = hasOptions ? preview(prices) : null
  const specs = offer.productSpecification?.productSpecCharacteristic ?? []
  const includes = offer.bundledProductOffering

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

        {includes.length > 0 && (
          <ul className="chips chips--names" aria-label="includes">
            {includes.map((b) => (
              <li key={b.id}>{b.name}</li>
            ))}
          </ul>
        )}

        {specs.length > 0 && (
          <ul className="chips" aria-label="specs">
            {specs.map((s) => (
              <li key={s.name}>
                {humanize(s.name)} · {s.values.join(' / ')}
              </li>
            ))}
          </ul>
        )}

        {hasOptions && <PurchaseOptions available={available} value={option} onChange={setOption} compact />}

        <div className="offer__price">
          {sum && (
            <dl className="offer__split">
              <div>
                <dt>Due today</dt>
                <dd>{money(sum.unit, sum.today)}</dd>
              </div>
              <div>
                <dt>Every month</dt>
                <dd>{money(sum.unit, sum.monthly)}</dd>
              </div>
            </dl>
          )}
          {!sum && headline?.price && (
            <p className="offer__amount">
              <strong>{money(headline.price.unit, headline.price.value)}</strong>
              <span>{perLabel(headline.recurringChargePeriodType)}</span>
            </p>
          )}
          {!sum && extras.length > 0 && (
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

        {addOn && <ProtectionAddOn offerId={addOn.id} checked={withAddOn} onChange={setWithAddOn} />}

        <AddToCartButton
          offering={offer}
          option={hasOptions ? option : undefined}
          extras={addOn && withAddOn ? [addOn] : []}
          sellable={offer.isSellable}
        />
      </div>
    </article>
  )
}
