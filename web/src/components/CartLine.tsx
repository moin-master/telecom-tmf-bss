import { Link } from 'react-router-dom'
import type { CartFieldsFragment } from '../api/generated/shopping-cart/graphql'
import { useOffer } from '../hooks/useOffers'
import { needsNumber } from '../lib/configure'
import { phoneNumber } from '../lib/format'
import { optionLabel } from '../lib/purchase'
import { offerEmoji } from '../lib/theme'
import { BundleParts } from './BundleParts'
import { Charges } from './Charges'

type Item = CartFieldsFragment['cartItem'][number]

// One cart line: what it is, what it includes, what is paid on the first bill and what every month.
export function CartLine({ item, busy, onRemove }: { item: Item; busy: boolean; onRemove: () => void }) {
  // The offer is usually already loaded by the page the shopper came from.
  const offer = useOffer(item.productOffering.id)
  const includes = offer.data?.bundledProductOffering ?? []
  const configurable = !!offer.data && needsNumber(offer.data)
  const configureHref = `/cart/items/${item.id}/configure`
  const number = item.product?.productCharacteristic.find((c) => c.name === 'TEL_MSISDN')?.value ?? null
  const oneTime = item.itemTotalPrice.filter((p) => p.priceType === 'oneTime')
  const monthly = item.itemTotalPrice.filter((p) => p.priceType === 'recurring')

  return (
    <li className="line">
      <span className="line__tile" aria-hidden="true">
        {offerEmoji(item.productOffering.name, { key: 'sun', emoji: '🛍️', label: '' })}
      </span>

      <div className="line__main">
        <Link to={`/offers/${item.productOffering.id}`} className="line__name">
          {item.productOffering.name}
        </Link>
        {item.purchaseOption && <span className="line__option">{optionLabel(item.purchaseOption)}</span>}
        {item.contractMonths && <span className="line__option">{item.contractMonths / 12}-year contract</span>}
      </div>

      <div className="line__side">
        <span className="line__qty">Qty {item.quantity}</span>
        <button
          type="button"
          className="line__remove"
          onClick={onRemove}
          disabled={busy}
          aria-label={`Remove ${item.productOffering.name}`}
          title="Remove"
        >
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M3 6h18" />
            <path d="M8 6V4h8v2" />
            <path d="M6 6l1 14h10l1-14" />
            <path d="M10 11v5M14 11v5" />
          </svg>
        </button>
      </div>

      {includes.length > 0 && (
        <BundleParts
          components={includes}
          configureHref={configurable ? configureHref : undefined}
          number={number}
        />
      )}
      {/* A single SIM offer has no parts, so it carries its own Configure button. */}
      {configurable && includes.length === 0 && (
        <div className="line__configure">
          <span>{number ? `Number ${phoneNumber(number)}` : 'Needs a number'}</span>
          <Link to={configureHref} className="link-action">
            {number ? 'Edit' : 'Configure'}
          </Link>
        </div>
      )}

      <div className="line__charges">
        <Charges
          title="First bill only"
          hint="One-time, not repeated"
          rows={oneTime}
          totals={item.itemSubtotal.filter((t) => t.priceType === 'oneTime')}
        />
        <Charges
          title="Every month"
          hint="Discounts end after their period"
          rows={monthly}
          totals={item.itemSubtotal.filter((t) => t.priceType === 'recurring')}
        />
      </div>
    </li>
  )
}
