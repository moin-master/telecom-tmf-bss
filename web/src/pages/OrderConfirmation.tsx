import { useMemo } from 'react'
import { Link, useParams } from 'react-router-dom'
import { BillTo } from '../components/BillTo'
import { OrderImage } from '../components/OrderImage'
import { ServiceTreeList } from '../components/ServiceTreeList'
import { ErrorState, StateCard } from '../components/StateViews'
import { useAuth } from '../hooks/useAuth'
import { useMyServices } from '../hooks/useMyServices'
import { useOfferImages } from '../hooks/useOfferImages'
import { useOrder } from '../hooks/useOrders'
import { amount, totalLabel } from '../lib/cart'
import { phoneNumber } from '../lib/format'
import { buildServiceTrees, treesOfOrder } from '../lib/serviceTree'

export function OrderConfirmation() {
  const { id = '' } = useParams()
  const { token, profile, loading: authLoading } = useAuth()
  const order = useOrder(id)
  const services = useMyServices()
  const images = useOfferImages()
  const trees = useMemo(() => treesOfOrder(buildServiceTrees(services.data ?? []), id), [services.data, id])

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
      <header className="order__head">
        <OrderImage
          size="hero"
          name={data.productOrderItem[0]?.productOffering.name ?? ''}
          src={data.productOrderItem[0] ? images.data?.get(data.productOrderItem[0].productOffering.id) : undefined}
          more={Math.max(data.productOrderItem.length - 1, 0)}
        />
        <div>
          <p className="kicker">Order {data.id}</p>
          <h1 className="cart__title">Thank you{customer ? `, ${customer.name.split(' ')[0]}` : ''}</h1>
          <p className="order__lead">
            We have received your order. Its state is <span className="state-pill">Acknowledged</span>.
          </p>
        </div>
      </header>

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
          {data.billingAccount && <li><BillTo accountId={data.billingAccount.id} /></li>}
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

      {trees.length > 0 && (
        <section className="order__services" aria-labelledby="your-services">
          <h2 id="your-services" className="order__heading">
            Your services
          </h2>
          <ServiceTreeList trees={trees} orders={[data]} label="Your services" />
        </section>
      )}
    </div>
  )
}
