import { useState } from 'react'
import { Link } from 'react-router-dom'
import { AuthForm, type AuthMode } from '../components/AuthForm'
import { BillingStep } from '../components/BillingStep'
import { OrderSummary } from '../components/OrderSummary'
import { PlaceOrder } from '../components/PlaceOrder'
import { StateCard } from '../components/StateViews'
import { useAuth } from '../hooks/useAuth'
import { useCart } from '../hooks/useCart'

const MODES: { id: AuthMode; label: string }[] = [
  { id: 'register', label: 'Create account' },
  { id: 'signIn', label: 'Sign in' },
]

export function Checkout() {
  const { cart, loading: cartLoading } = useCart()
  const { profile, loading: authLoading, signOut } = useAuth()
  const [mode, setMode] = useState<AuthMode>('register')
  const [billingId, setBillingId] = useState<string | null>(null)
  const owner = cart?.relatedParty.find((p) => p.role === 'customer')?.partyOrPartyRole

  if (cartLoading || authLoading) {
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
          Add something before you check out.
        </StateCard>
      </div>
    )
  }

  return (
    <div className="wrap cart">
      <h1 className="cart__title">Checkout</h1>

      <div className="cart__grid">
        <div className="checkout-col">
          <section className="checkout" aria-labelledby="account-title">
            <h2 id="account-title" className="checkout__step">
              <span className="checkout__num" aria-hidden="true">
                1
              </span>
              Your account
            </h2>

            {profile ? (
              <div className="signedin">
                <p className="signedin__name">{profile.name}</p>
                <p className="signedin__email">{profile.email}</p>
                {owner && <p className="signedin__link">This cart belongs to customer {owner.id}.</p>}
                <button type="button" className="configure__keep" onClick={() => void signOut()}>
                  Not you? Sign out
                </button>
              </div>
            ) : (
              <>
                <div className="seg" role="group" aria-label="Account">
                  {MODES.map((m) => (
                    <button key={m.id} type="button" aria-pressed={mode === m.id} onClick={() => setMode(m.id)}>
                      {m.label}
                    </button>
                  ))}
                </div>
                <AuthForm key={mode} mode={mode} />
              </>
            )}
          </section>
          {profile && <BillingStep selectedId={billingId} onSelect={setBillingId} />}
          {profile && <PlaceOrder billingAccountId={billingId} />}
        </div>

        <aside className="receipt" aria-label="Order summary">
          <h2 className="receipt__head">Order summary</h2>
          <OrderSummary cart={cart} />
        </aside>
      </div>
    </div>
  )
}
