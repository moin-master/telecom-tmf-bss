import type { CartFieldsFragment } from '../api/generated/shopping-cart/graphql'
import { amount, isCredit } from '../lib/cart'
import { perLabel } from '../lib/format'
import { SummaryLines } from './SummaryLines'
import { SummaryTotals } from './SummaryTotals'

export function OrderSummary({ cart }: { cart: CartFieldsFragment }) {
  const oneTime = cart.cartTotalPrice.filter((t) => t.priceType === 'oneTime')
  const monthly = cart.cartTotalPrice.filter((t) => t.priceType === 'recurring')
  const cartDiscounts = cart.cartTotalPrice.filter((t) => t.priceType === 'discount')

  return (
    <>
      {oneTime.length > 0 && (
        <section className="receipt__section" aria-labelledby="first-bill">
          <h3 id="first-bill" className="receipt__heading">
            First bill only
          </h3>
          <p className="receipt__sub">One-time charges, such as the activation fee. They are not repeated.</p>
          <SummaryLines cart={cart} type="oneTime" />
          <SummaryTotals totals={oneTime} />
        </section>
      )}

      {monthly.length > 0 && (
        <section className="receipt__section" aria-labelledby="every-month">
          <h3 id="every-month" className="receipt__heading">
            Every month
          </h3>
          <p className="receipt__sub">Charged on every bill. Time-limited discounts end after their period.</p>
          <SummaryLines cart={cart} type="recurring" />
          {cartDiscounts.length > 0 && (
            <div className="receipt__group">
              <p className="receipt__item">Whole cart</p>
              <ul className="receipt__lines">
                {cartDiscounts.map((d, i) => (
                  <li key={i} className={isCredit(d) ? 'is-credit' : undefined}>
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
          <SummaryTotals totals={monthly} />
        </section>
      )}
    </>
  )
}
