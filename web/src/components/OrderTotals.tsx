import { amount, totalLabel } from '../lib/cart'
import type { Order } from '../lib/orderCard'

// "Today" is the large figure; the monthly charges sit under it in a smaller size.
export function OrderTotals({ totals }: { totals: Order['orderTotalPrice'] }) {
  const today = totals.filter((t) => t.priceType === 'oneTime')
  const monthly = totals.filter((t) => t.priceType === 'recurring')
  return (
    <div className="order-totals">
      {today.map((t, i) => (
        <p key={i} className="order-totals__today">
          <b>{amount(t)}</b> <span>today</span>
        </p>
      ))}
      {monthly.map((t, i) => (
        <p key={i} className="order-totals__monthly">
          <b>{amount(t)}</b> <span>{totalLabel(t).toLowerCase()}</span>
        </p>
      ))}
    </div>
  )
}
