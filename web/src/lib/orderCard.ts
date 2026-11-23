import type { OrdersQuery } from '../api/generated/order/graphql'
import type { ServiceOrder } from './fulfilment'

export type Order = OrdersQuery['productOrderList'][number]

export type StepState = 'done' | 'current' | 'pending' | 'failed'
export type Step = { label: string; state: StepState }

// Placed, Fulfilling, Fulfilled from the order and its service order. An order with no service
// order yet stops at Placed; a failed service order marks the Fulfilling step as failed.
export function orderSteps(fulfilment?: ServiceOrder): Step[] {
  const state = fulfilment?.state
  const fulfilling: StepState =
    state === 'failed' ? 'failed' : state === 'completed' ? 'done' : state ? 'current' : 'pending'
  return [
    { label: 'Placed', state: state ? 'done' : 'current' },
    { label: 'Fulfilling', state: fulfilling },
    { label: 'Fulfilled', state: state === 'completed' ? 'done' : 'pending' },
  ]
}

export const stepStatus = (s: StepState) =>
  ({ done: 'done', current: 'in progress', pending: 'not yet', failed: 'failed' })[s]

// The first line's offering gives the picture; the rest count in the "+N" badge.
export const firstOfferId = (order: Order) => order.productOrderItem[0]?.productOffering.id
