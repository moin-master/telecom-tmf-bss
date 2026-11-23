import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useMyOrders } from '../hooks/useOrders'
import { useMyServices } from '../hooks/useMyServices'
import { buildServiceTrees } from '../lib/serviceTree'
import { ListSkeleton } from './ListSkeleton'
import { ServiceTreeList } from './ServiceTreeList'
import { ErrorState, StateCard } from './StateViews'

// Services tab: one tree per root service. A bundle shows its parts, a single service is a tree of one.
export function AccountServices() {
  const services = useMyServices()
  const orders = useMyOrders()
  const trees = useMemo(() => buildServiceTrees(services.data ?? []), [services.data])

  if (services.isPending) return <ListSkeleton label="Loading services" />
  if (services.isError) return <ErrorState error={services.error} onRetry={() => services.refetch()} />
  if (services.data.length === 0) {
    return (
      <StateCard
        emoji="📶"
        title="No services yet"
        action={
          <Link to="/" className="btn">
            Browse offers
          </Link>
        }
      >
        Your services appear here once an order has been fulfilled.
      </StateCard>
    )
  }

  return <ServiceTreeList trees={trees} orders={orders.data ?? []} label="Services" />
}
