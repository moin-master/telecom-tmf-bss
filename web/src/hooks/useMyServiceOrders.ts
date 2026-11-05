import { useQuery } from '@tanstack/react-query'
import { serviceOrderApi } from '../api/client'
import { ServiceOrdersDocument } from '../api/generated/service-order/graphql'
import { useAuth } from './useAuth'

const bearer = (token: string | null) => (token ? { Authorization: `Bearer ${token}` } : undefined)

// Fulfilment records of the signed-in customer; each points back to its product order.
export function useMyServiceOrders() {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['service-orders', token],
    enabled: !!token,
    retry: false,
    queryFn: () => serviceOrderApi.request(ServiceOrdersDocument, undefined, bearer(token)).then((r) => r.serviceOrderList),
  })
}
