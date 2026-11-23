import { Link } from 'react-router-dom'
import type { ServiceOrder } from '../lib/fulfilment'
import { shortDate } from '../lib/format'
import { firstOfferId, type Order } from '../lib/orderCard'
import type { ServiceTreeData } from '../lib/serviceTree'
import { OrderImage } from './OrderImage'
import { OrderItemsList } from './OrderItemsList'
import { OrderServices } from './OrderServices'
import { OrderStatusSteps } from './OrderStatusSteps'
import { OrderTotals } from './OrderTotals'

type Props = {
  order: Order
  orders: Order[]
  fulfilment?: ServiceOrder
  // Undefined while the services are loading or could not be loaded.
  trees?: ServiceTreeData[]
  images: Map<string, string> | undefined
}

// One order on Account > Orders: picture, summary in the middle, the status line under it, totals on the right,
// and the services disclosure with a link to the full order in the footer.
export function OrderCard({ order, orders, fulfilment, trees, images }: Props) {
  const totals = order.orderTotalPrice.filter((t) => t.priceType === 'oneTime' || t.priceType === 'recurring')
  const offerId = firstOfferId(order)
  const firstName = order.productOrderItem[0]?.productOffering.name ?? ''
  const viewOrder = (
    <Link to={`/orders/${order.id}`} className="order-card__view">
      View order
    </Link>
  )

  return (
    <li className="order-card">
      <OrderImage
        name={firstName}
        src={offerId ? images?.get(offerId) : undefined}
        more={Math.max(order.productOrderItem.length - 1, 0)}
      />
      <div className="order-card__head">
        <p className="row__title">
          <Link to={`/orders/${order.id}`} className="row__link">
            Order {order.id}
          </Link>
        </p>
        <p className="row__meta">
          {shortDate(order.creationDate)}
          {order.billingAccount && <> · Billed to {order.billingAccount.name}</>}
        </p>
        <OrderItemsList items={order.productOrderItem} />
      </div>
      <div className="order-card__status">
        <OrderStatusSteps fulfilment={fulfilment} />
      </div>
      <OrderTotals totals={totals} />
      <div className="order-card__footer">
        {trees ? (
          <OrderServices orderId={order.id} trees={trees} orders={orders}>
            {viewOrder}
          </OrderServices>
        ) : (
          viewOrder
        )}
      </div>
    </li>
  )
}
