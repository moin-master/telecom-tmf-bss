import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { AddToCartButton } from '../components/AddToCartButton'
import { ProtectionAddOn } from '../components/ProtectionAddOn'
import { PurchaseOptions } from '../components/PurchaseOptions'
import { ErrorState, StateCard } from '../components/StateViews'
import { useOffer } from '../hooks/useOffers'
import { apiError } from '../lib/errors'
import { humanize, money, perLabel } from '../lib/format'
import { optionsOf, pricesFor, type PurchaseOption } from '../lib/purchase'
import { offerEmoji, offerTheme } from '../lib/theme'

const MAX_QUANTITY = 99

export function OfferDetail() {
  const { id = '' } = useParams()
  const offer = useOffer(id)
  const [quantity, setQuantity] = useState(1)
  const [option, setOption] = useState<PurchaseOption>('own')
  const [withAddOn, setWithAddOn] = useState(false)

  if (offer.isPending) {
    return (
      <div className="wrap detail" aria-busy="true">
        <div className="skeleton__media skeleton__media--tall" />
      </div>
    )
  }

  if (offer.isError) {
    const gone = apiError(offer.error).code === 'NotFound'
    return (
      <div className="wrap">
        {gone ? (
          <StateCard
            emoji="🕳️"
            title="This offer is gone"
            action={
              <Link to="/" className="btn">
                Back to offers
              </Link>
            }
          >
            That offer is not available right now.
          </StateCard>
        ) : (
          <ErrorState error={offer.error} onRetry={() => offer.refetch()} />
        )}
      </div>
    )
  }

  const data = offer.data
  const theme = offerTheme(data.category)
  const specs = data.productSpecification?.productSpecCharacteristic ?? []
  const addOn = data.productOfferingRelationship.find((r) => r.relationshipType === 'addOn')
  const available = optionsOf(data.productOfferingPrice)
  const hasOptions = available.length > 0
  const prices = hasOptions ? pricesFor(data.productOfferingPrice, option) : data.productOfferingPrice.filter((p) => p.price)

  return (
    <div className="wrap detail" data-theme={theme.key}>
      <nav className="crumbs" aria-label="Breadcrumb">
        <Link to="/">Offers</Link> <span aria-hidden="true">/</span> <span>{theme.label}</span>
      </nav>

      <div className="detail__grid">
        <div className="detail__art">
          <span className="offer__tag">{theme.label}</span>
          <span className="detail__emoji" aria-hidden="true">
            {offerEmoji(data.name, theme)}
          </span>
          {specs.slice(0, 3).map((s, i) => (
            <span key={s.name} className={`float float--${i}`} aria-hidden="true">
              {humanize(s.name)} · {s.values.join(' / ')}
            </span>
          ))}
        </div>

        <div className="detail__info">
          <p className="kicker">{data.productSpecification?.brand ?? 'vibe exclusive'}</p>
          <h1 className="detail__title">{data.name}</h1>
          {data.description && <p className="detail__desc">{data.description}</p>}

          {data.bundledProductOffering.length > 0 && (
            <>
              <h2 className="detail__h">Includes</h2>
              <ul className="chips chips--names" aria-label="includes">
                {data.bundledProductOffering.map((b) => (
                  <li key={b.id}>
                    <Link to={`/offers/${b.id}`}>{b.name}</Link>
                  </li>
                ))}
              </ul>
            </>
          )}

          {hasOptions && <PurchaseOptions available={available} value={option} onChange={setOption} />}

          <h2 className="detail__h">Pricing</h2>
          <ul className="tickets">
            {prices.map((p) => (
              <li key={p.id} className="ticket">
                <span className="ticket__name">
                  {p.name}
                  <small>
                    {p.priceType === 'recurring' ? `Every ${p.recurringChargePeriodType ?? 'period'}` : 'One time'}
                  </small>
                </span>
                <b className="ticket__amount">
                  {money(p.price!.unit, p.price!.value)}
                  <small>{perLabel(p.recurringChargePeriodType)}</small>
                </b>
              </li>
            ))}
          </ul>

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

          {addOn && <ProtectionAddOn offerId={addOn.id} checked={withAddOn} onChange={setWithAddOn} />}

          <div className="buy">
            <div className="stepper" role="group" aria-label="Quantity">
              <button
                type="button"
                onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                disabled={quantity <= 1}
                aria-label="One less"
              >
                −
              </button>
              <output aria-live="polite">{quantity}</output>
              <button
                type="button"
                onClick={() => setQuantity((q) => Math.min(MAX_QUANTITY, q + 1))}
                disabled={quantity >= MAX_QUANTITY}
                aria-label="One more"
              >
                +
              </button>
            </div>
            <AddToCartButton
              offering={data}
              quantity={quantity}
              option={hasOptions ? option : undefined}
              extras={addOn && withAddOn ? [addOn] : []}
              sellable={data.isSellable}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
