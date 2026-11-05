import { Link } from 'react-router-dom'
import { useMyOrders } from '../hooks/useOrders'
import { useMyServiceOrders } from '../hooks/useMyServiceOrders'
import { amount, totalLabel } from '../lib/cart'
import { fulfilmentFor, fulfilmentLabel } from '../lib/fulfilment'
import { shortDate } from '../lib/format'
import { ListSkeleton } from './ListSkeleton'
import { ErrorState, StateCard } from './StateViews'

// Orders tab: every product order with its fulfilment state from the matching service order.
export function AccountOrders() {
  const orders = useMyOrders()
  const fulfilment = useMyServiceOrders()

  if (orders.isPending) return <ListSkeleton label="Loading orders" />
  if (orders.isError) return <ErrorState error={orders.error} onRetry={() => orders.refetch()} />
  if (orders.data.length === 0) {
    return (
      <StateCard
        emoji="📦"
        title="No orders yet"
        action={
          <Link to="/" className="btn">
            Browse offers
          </Link>
        }
      >
        Orders you place show up here with their progress.
      </StateCard>
    )
  }

  return (
    <>
      {fulfilment.isError && (
        <p className="rows__note" role="status">
          Fulfilment progress could not be loaded.{' '}
          <button type="button" className="configure__keep" onClick={() => fulfilment.refetch()}>
            Try again
          </button>
        </p>
      )}
      <ul className="rows" aria-label="Orders">
        {[...orders.data].reverse().map((order) => {
          const match = fulfilment.data ? fulfilmentFor(order.id, fulfilment.data) : undefined
          const totals = order.orderTotalPrice.filter((t) => t.priceType === 'oneTime' || t.priceType === 'recurring')
          return (
            <li key={order.id} className="row">
              <div className="row__main">
                <p className="row__title">
                  <Link to={`/orders/${order.id}`} className="row__link">
                    Order {order.id}
                  </Link>
                </p>
                <p className="row__meta">
                  {shortDate(order.creationDate)}
                  {order.billingAccount && <> · Billed to {order.billingAccount.name}</>}
                </p>
                {match?.errorMessage && <p className="row__meta">{match.errorMessage}</p>}
              </div>
              <dl className="row__facts">
                <div>
                  <dt>Order</dt>
                  <dd>
                    <span className="state-pill">{order.state}</span>
                  </dd>
                </div>
                <div>
                  <dt>Fulfilment</dt>
                  <dd>
                    {match ? (
                      <span className="state-pill">{fulfilmentLabel(match.state)}</span>
                    ) : (
                      <span className="row__none">Not fulfilled</span>
                    )}
                  </dd>
                </div>
                <div>
                  <dt>Total</dt>
                  <dd>
                    {totals.map((t, i) => (
                      <span key={i} className="row__total">
                        {amount(t)} <small>{t.priceType === 'oneTime' ? 'today' : totalLabel(t).toLowerCase()}</small>
                      </span>
                    ))}
                  </dd>
                </div>
              </dl>
            </li>
          )
        })}
      </ul>
    </>
  )
}
