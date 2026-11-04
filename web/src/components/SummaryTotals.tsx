import type { CartFieldsFragment } from '../api/generated/shopping-cart/graphql'
import { amount, totalLabel } from '../lib/cart'

export function SummaryTotals({ totals }: { totals: CartFieldsFragment['cartTotalPrice'] }) {
  return (
    <dl className="receipt__totals">
      {totals.map((t, i) => (
        <div key={i}>
          <dt>{totalLabel(t)}</dt>
          <dd>{amount(t)}</dd>
        </div>
      ))}
    </dl>
  )
}
