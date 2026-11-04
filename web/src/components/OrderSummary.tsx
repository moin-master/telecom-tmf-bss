import type { CartFieldsFragment } from '../api/generated/shopping-cart/graphql'
import { amount, isCredit, totalLabel } from '../lib/cart'
import { perLabel } from '../lib/format'

type Cart = CartFieldsFragment
type Total = Cart['cartTotalPrice'][number]

// Lines of one kind for each cart item, so every charge and discount can be traced to its item.
function itemLines(cart: Cart, type: 'oneTime' | 'recurring') {
  return cart.cartItem
    .map((item) => ({
      id: item.id,
      name: item.productOffering.name,
      quantity: item.quantity,
      rows: item.itemTotalPrice.filter((p) => p.priceType === type),
    }))
    .filter((group) => group.rows.length > 0)
}

function Lines({ groups }: { groups: ReturnType<typeof itemLines> }) {
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

function Totals({ totals }: { totals: Total[] }) {
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

export function OrderSummary({ cart }: { cart: Cart }) {
  const oneTime = cart.cartTotalPrice.filter((t) => t.priceType === 'oneTime')
  const monthly = cart.cartTotalPrice.filter((t) => t.priceType === 'recurring')
  const cartDiscounts = cart.cartTotalPrice.filter((t) => t.priceType === 'discount')
  const oneTimeGroups = itemLines(cart, 'oneTime')
  const monthlyGroups = itemLines(cart, 'recurring')

  return (
    <>
      {oneTime.length > 0 && (
        <section className="receipt__section" aria-labelledby="first-bill">
          <h3 id="first-bill" className="receipt__heading">
            First bill only
          </h3>
          <p className="receipt__sub">One-time charges, such as the activation fee. They are not repeated.</p>
          <Lines groups={oneTimeGroups} />
          <Totals totals={oneTime} />
        </section>
      )}

      {monthly.length > 0 && (
        <section className="receipt__section" aria-labelledby="every-month">
          <h3 id="every-month" className="receipt__heading">
            Every month
          </h3>
          <p className="receipt__sub">Charged on every bill. Time-limited discounts end after their period.</p>
          <Lines groups={monthlyGroups} />
          {cartDiscounts.length > 0 && (
            <div className="receipt__group">
              <p className="receipt__item">Whole cart</p>
              <ul className="receipt__lines">
                {cartDiscounts.map((d, i) => (
                  <li key={i} className="is-credit">
                    <span>{d.name}</span>
                    <b>
                      {amount(d)}
                      {perLabel(d.recurringChargePeriod)}
                    </b>
                  </li>
                ))}
              </ul>
            </div>
          )}
          <Totals totals={monthly} />
        </section>
      )}
    </>
  )
}
