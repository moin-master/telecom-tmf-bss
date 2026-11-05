import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { orderApi } from '../api/client'
import { OrderDocument, OrdersDocument, PlaceOrderDocument } from '../api/generated/order/graphql'
import { useAuth } from './useAuth'

const bearer = (token: string | null) => (token ? { Authorization: `Bearer ${token}` } : undefined)

// Creates the order from the cart. The backend deletes the cart; the caller then forgets its id.
export function usePlaceOrder() {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (v: { cartId: string; billingAccountId: string }) =>
      orderApi.request(PlaceOrderDocument, v, bearer(token)).then((r) => r.createProductOrder),
    onSuccess: (order) => queryClient.setQueryData(['order', order.id], order),
  })
}

export function useOrder(id: string) {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['order', id, token],
    enabled: !!id && !!token,
    retry: false,
    queryFn: () => orderApi.request(OrderDocument, { id }, bearer(token)).then((r) => r.productOrder),
  })
}

// The signed-in customer's orders, as the backend returns them.
export function useMyOrders() {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['orders', token],
    enabled: !!token,
    retry: false,
    queryFn: () => orderApi.request(OrdersDocument, undefined, bearer(token)).then((r) => r.productOrderList),
  })
}
