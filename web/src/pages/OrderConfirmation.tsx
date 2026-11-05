import { Link, useParams } from 'react-router-dom'
import { ErrorState, StateCard } from '../components/StateViews'
import { useAuth } from '../hooks/useAuth'
import { useOrder } from '../hooks/useOrders'
import { amount, totalLabel } from '../lib/cart'
import { phoneNumber } from '../lib/format'

export function OrderConfirmation() {
  const { id = '' } = useParams()
  const { token, profile, loading: authLoading } = useAuth()
  const order = useOrder(id)

  if (authLoading || (token && order.isPending)) {
    return (
      <div className="wrap" aria-busy="true">
        <div className="skeleton__media skeleton__media--tall" />
      </div>
    )
  }
  if (!token || !profile) {
    return (
      <div className="wrap">
        <StateCard
          emoji="🔒"
          title="Sign in to see your order"
          action={
            <Link to="/checkout" className="btn">
              Sign in
            </Link>
          }
        >
          Orders are private to the customer who placed them.
        </StateCard>
      </div>
    )
  }
  if (order.isError) {
    return (
      <div className="wrap">
        <ErrorState error={order.error} onRetry={() => order.refetch()} />
      </div>
    )
  }
  const data = order.data
  if (!data) return null

  const customer = data.relatedParty.find((p) => p.role === 'customer')?.partyOrPartyRole
  const totals = data.orderTotalPrice.filter((t) => t.priceType === 'oneTime' || t.priceType === 'recurring')

  return (
    <div className="wrap order">
      <p className="kicker">Order {data.id}</p>
      <h1 className="cart__title">Thank you{customer ? `, ${customer.name.split(' ')[0]}` : ''}</h1>
      <p className="order__lead">
        We have received your order. Its state is <span className="state-pill">Acknowledged</span>.
      </p>

      <div className="cart__grid">
        <ul className="order__items" aria-label="Items">
          {data.productOrderItem.map((item) => {
            const number = item.product.productCharacteristic.find((c) => c.name === 'TEL_MSISDN')?.value
            return (
              <li key={item.id} className="order__item">
                <p className="order__name">
                  {item.productOffering.name}
                  {item.quantity > 1 && <span className="order__qty"> × {item.quantity}</span>}
                </p>
                {item.itemTerm.map((t) => (
                  <p key={t.name} className="order__detail">
                    {t.name}: {t.duration.amount / 12} year{t.duration.amount === 12 ? '' : 's'}
                  </p>
                ))}
                {number && <p className="order__detail">Phone number {phoneNumber(number)}</p>}
              </li>
            )
          })}
        </ul>

        <aside className="receipt" aria-label="Order total">
          <h2 className="receipt__head">Order total</h2>
          <dl className="charges__totals">
            {totals.map((t, i) => (
              <div key={i}>
                <dt>{totalLabel(t)}</dt>
                <dd>{amount(t)}</dd>
              </div>
            ))}
          </dl>
          <Link to="/" className="btn btn--ghost receipt__checkout">
            Keep browsing
          </Link>
        </aside>
      </div>
    </div>
  )
}
