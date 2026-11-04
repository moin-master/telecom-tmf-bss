import type { CartItemFieldsFragment } from '../api/generated/shopping-cart/graphql'
import { Charges } from './Charges'

type Props = {
  quote: CartItemFieldsFragment | undefined
  updating: boolean
  failed: boolean
}

// What the shopper would pay with the current choices, priced by the backend.
export function BillPreview({ quote, updating, failed }: Props) {
  if (failed && !quote) {
    return <p className="bill__note">The bill is shown in your cart after you add this offer.</p>
  }
  if (!quote) return <div className="bill__skeleton" aria-busy="true" />

  return (
    <div className={`bill${updating ? ' is-updating' : ''}`} aria-live="polite">
      <Charges
        title="First bill only"
        hint="One-time charges, not repeated"
        rows={quote.itemTotalPrice.filter((p) => p.priceType === 'oneTime')}
        totals={quote.itemSubtotal.filter((t) => t.priceType === 'oneTime')}
      />
      <Charges
        title="Every month"
        hint="Discounts end after their period"
        rows={quote.itemTotalPrice.filter((p) => p.priceType === 'recurring')}
        totals={quote.itemSubtotal.filter((t) => t.priceType === 'recurring')}
      />
    </div>
  )
}
