import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { useCart } from '../hooks/useCart'
import { usePlaceOrder } from '../hooks/useOrders'
import { apiError } from '../lib/errors'
import { LineCheck } from './LineCheck'

// Step 3 of checkout: check every line and turn the cart into an order.
export function PlaceOrder({ billingAccountId }: { billingAccountId: string | null }) {
  const { cart, forget } = useCart()
  const { profile } = useAuth()
  const place = usePlaceOrder()
  const navigate = useNavigate()
  const [error, setError] = useState<string | null>(null)
  if (!cart || !profile) return null

  // The cart is attached to the signed-in customer a moment after sign-in.
  const linked = cart.relatedParty.some(
    (p) => p.role === 'customer' && p.partyOrPartyRole.id === profile.customerId,
  )

  async function onPlace() {
    setError(null)
    try {
      const order = await place.mutateAsync({ cartId: cart!.id, billingAccountId: billingAccountId! })
      forget()
      navigate(`/orders/${order.id}`)
    } catch (e) {
      setError(apiError(e).message)
    }
  }

  return (
    <section className="checkout" aria-labelledby="order-title">
      <h2 id="order-title" className="checkout__step">
        <span className="checkout__num" aria-hidden="true">
          3
        </span>
        Place your order
      </h2>
      <ul className="checks" aria-label="Order check">
        {cart.cartItem.map((item) => (
          <LineCheck key={item.id} item={item} />
        ))}
      </ul>
      {error && (
        <p className="add__error" role="alert">
          {error}
        </p>
      )}
      <button type="button" className="btn btn--big checkout__place" disabled={!linked || !billingAccountId || place.isPending} onClick={onPlace}>
        {place.isPending ? 'Placing your order' : 'Place order'}
      </button>
      <p className="receipt__note checkout__note">No payment is taken in this step.</p>
    </section>
  )
}
