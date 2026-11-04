import { useState } from 'react'
import { Link } from 'react-router-dom'
import { StateCard } from '../components/StateViews'
import { useCart } from '../hooks/useCart'
import { apiError } from '../lib/errors'
import { money, perLabel } from '../lib/format'
import { optionLabel } from '../lib/purchase'
import { offerEmoji } from '../lib/theme'

export function Cart() {
  const { cart, loading, remove, busy } = useCart()
  const [error, setError] = useState<string | null>(null)

  if (loading) {
    return (
      <div className="wrap" aria-busy="true">
        <div className="skeleton__media skeleton__media--tall" />
      </div>
    )
  }

  if (!cart || cart.cartItem.length === 0) {
    return (
      <div className="wrap">
        <StateCard
          emoji="🛍️"
          title="Your cart is empty"
          action={
            <Link to="/" className="btn">
              Browse offers
            </Link>
          }
        >
          Add a plan, a phone or a SIM and it shows up here.
        </StateCard>
      </div>
    )
  }

  async function onRemove(itemId: string) {
    setError(null)
    try {
      await remove(itemId)
    } catch (e) {
      setError(apiError(e).message)
    }
  }

  return (
    <div className="wrap cart">
      <h1 className="cart__title">Your cart</h1>

      <div className="cart__grid">
        <ul className="lines">
          {cart.cartItem.map((item) => (
            <li key={item.id} className="line">
              <span className="line__tile" aria-hidden="true">
                {offerEmoji(item.productOffering.name, { key: 'sun', emoji: '🛍️', label: '' })}
              </span>
              <div className="line__main">
                <Link to={`/offers/${item.productOffering.id}`} className="line__name">
                  {item.productOffering.name}
                </Link>
                {item.purchaseOption && <span className="line__option">{optionLabel(item.purchaseOption)}</span>}
                <ul className="line__prices">
                  {item.itemPrice.map((p, i) => (
                    <li key={i}>
                      {p.name}{' '}
                      <b>
                        {money(p.price.dutyFreeAmount.unit, p.price.dutyFreeAmount.value)}
                        {perLabel(p.recurringChargePeriod)}
                      </b>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="line__side">
                <span className="line__qty">Qty {item.quantity}</span>
                <button
                  type="button"
                  className="line__remove"
                  onClick={() => onRemove(item.id)}
                  disabled={busy}
                  aria-label={`Remove ${item.productOffering.name}`}
                >
                  Remove
                </button>
              </div>
            </li>
          ))}
        </ul>

        <aside className="receipt" aria-label="Order summary">
          <h2 className="receipt__head">Order summary</h2>

          {error && (
            <p className="add__error" role="alert">
              {error}
            </p>
          )}

          <dl className="receipt__totals">
            {cart.cartTotalPrice.map((t, i) => (
              <div key={i}>
                <dt>{t.priceType === 'recurring' ? `Every ${t.recurringChargePeriod ?? 'period'}` : 'Due today'}</dt>
                <dd>{money(t.price.taxIncludedAmount.unit, t.price.taxIncludedAmount.value)}</dd>
              </div>
            ))}
          </dl>

          <button type="button" className="btn btn--big receipt__checkout" disabled>
            Checkout opens soon
          </button>
          <p className="receipt__note">Prices shown are those in the catalog when you added each item.</p>
        </aside>
      </div>
    </div>
  )
}
