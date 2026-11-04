import type { CartItemFieldsFragment } from '../api/generated/shopping-cart/graphql'
import { amount, isCredit, totalLabel } from '../lib/cart'
import { LineAmount } from './LineAmount'

type Props = {
  title: string
  hint: string
  rows: CartItemFieldsFragment['itemTotalPrice']
  totals: CartItemFieldsFragment['itemSubtotal']
}

// One card of charges for a cart line or a quote: the lines, then the totals the backend calculated.
export function Charges({ title, hint, rows, totals }: Props) {
  if (rows.length === 0) return null
  return (
    <section className="charges" aria-label={title}>
      <h3 className="charges__title">{title}</h3>
      <p className="charges__hint">{hint}</p>
      <ul className="charges__rows">
        {rows.map((p, i) => (
          <li key={i} className={isCredit(p) ? 'is-credit' : undefined}>
            <span>{p.name}</span>
            <LineAmount line={p} />
          </li>
        ))}
      </ul>
      {rows.some((p) => p.regularPrice) && (
        <p className="charges__foot">The struck-out price is the regular price. You pay the price next to it.</p>
      )}
      <dl className="charges__totals">
        {totals.map((t, i) => (
          <div key={i}>
            <dt>{totalLabel(t)}</dt>
            <dd>{amount(t)}</dd>
          </div>
        ))}
      </dl>
    </section>
  )
}
