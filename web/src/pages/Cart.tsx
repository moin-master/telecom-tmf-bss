import { useState } from 'react'
import { Link } from 'react-router-dom'
import { CartLine } from '../components/CartLine'
import { OrderSummary } from '../components/OrderSummary'
import { StateCard } from '../components/StateViews'
import { useCart } from '../hooks/useCart'
import { apiError } from '../lib/errors'

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
            <CartLine key={item.id} item={item} busy={busy} onRemove={() => onRemove(item.id)} />
          ))}
        </ul>

        <aside className="receipt" aria-label="Order summary">
          <h2 className="receipt__head">Order summary</h2>

          {error && (
            <p className="add__error" role="alert">
              {error}
            </p>
          )}

          <OrderSummary cart={cart} />

          <Link to="/checkout" className="btn btn--big receipt__checkout">
            Checkout
          </Link>
          <p className="receipt__note">Prices shown are those in the catalog when you added each item.</p>
        </aside>
      </div>
    </div>
  )
}
