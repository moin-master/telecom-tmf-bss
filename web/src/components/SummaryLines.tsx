import type { CartFieldsFragment } from '../api/generated/shopping-cart/graphql'
import { amount, isCredit } from '../lib/cart'
import { perLabel } from '../lib/format'

type Cart = CartFieldsFragment

// The lines of one kind (one-time or recurring) for each cart item, so every charge traces to its item.
export function SummaryLines({ cart, type }: { cart: Cart; type: 'oneTime' | 'recurring' }) {
  const groups = cart.cartItem
    .map((item) => ({
      id: item.id,
      name: item.productOffering.name,
      quantity: item.quantity,
      rows: item.itemTotalPrice.filter((p) => p.priceType === type),
    }))
    .filter((group) => group.rows.length > 0)

  return (
    <>
      {groups.map((group) => (
        <div key={group.id} className="receipt__group">
          <p className="receipt__item">
            {group.name}
            {group.quantity > 1 && <span> × {group.quantity}</span>}
          </p>
          <ul className="receipt__lines">
            {group.rows.map((p, i) => (
              <li key={i} className={isCredit(p) ? 'is-credit' : undefined}>
                <span>{p.name}</span>
                <b>
                  {amount(p)}
                  {perLabel(p.recurringChargePeriod)}
                </b>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </>
  )
}
