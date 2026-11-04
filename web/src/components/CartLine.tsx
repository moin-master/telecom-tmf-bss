import { Link } from 'react-router-dom'
import type { CartFieldsFragment } from '../api/generated/shopping-cart/graphql'
import { useOffer } from '../hooks/useOffers'
import { optionLabel } from '../lib/purchase'
import { offerEmoji } from '../lib/theme'
import { Charges } from './Charges'

type Item = CartFieldsFragment['cartItem'][number]

// One cart line: what it is, what it includes, what is paid on the first bill and what every month.
export function CartLine({ item, busy, onRemove }: { item: Item; busy: boolean; onRemove: () => void }) {
  // The offer is usually already loaded by the page the shopper came from.
  const offer = useOffer(item.productOffering.id)
  const includes = offer.data?.bundledProductOffering ?? []
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
        {includes.length > 0 && (
          <p className="line__includes">
            <span>Includes</span> {includes.map((b) => b.name).join(' · ')}
          </p>
        )}
      </div>

      <div className="line__side">
        <span className="line__qty">Qty {item.quantity}</span>
        <button
          type="button"
          className="line__remove"
          onClick={onRemove}
          disabled={busy}
          aria-label={`Remove ${item.productOffering.name}`}
        >
          Remove
        </button>
      </div>

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
