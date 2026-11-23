import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useMyOrders } from '../hooks/useOrders'
import { useMyServiceOrders } from '../hooks/useMyServiceOrders'
import { useMyServices } from '../hooks/useMyServices'
import { useOfferImages } from '../hooks/useOfferImages'
import { fulfilmentFor } from '../lib/fulfilment'
import { buildServiceTrees, treesOfOrder } from '../lib/serviceTree'
import { ListSkeleton } from './ListSkeleton'
import { OrderCard } from './OrderCard'
import { ErrorState, StateCard } from './StateViews'

// Orders tab: every product order with its fulfilment state from the matching service order.
export function AccountOrders() {
  const orders = useMyOrders()
  const fulfilment = useMyServiceOrders()
  const services = useMyServices()
  const images = useOfferImages()
  const trees = useMemo(() => buildServiceTrees(services.data ?? []), [services.data])

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
      {services.isError && (
        <p className="rows__note" role="status">
          Services could not be loaded.{' '}
          <button type="button" className="configure__keep" onClick={() => services.refetch()}>
            Try again
          </button>
        </p>
      )}
      <ul className="rows" aria-label="Orders">
        {[...orders.data].reverse().map((order) => (
          <OrderCard
            key={order.id}
            order={order}
            orders={orders.data}
            fulfilment={fulfilment.data ? fulfilmentFor(order.id, fulfilment.data) : undefined}
            trees={services.data ? treesOfOrder(trees, order.id) : undefined}
            images={images.data}
          />
        ))}
      </ul>
    </>
  )
}
