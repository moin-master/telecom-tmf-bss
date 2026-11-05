import type { ServiceOrdersQuery } from '../api/generated/service-order/graphql'

export type ServiceOrder = ServiceOrdersQuery['serviceOrderList'][number]

const LABELS: Record<string, string> = {
  acknowledged: 'Received',
  inProgress: 'In progress',
  completed: 'Fulfilled',
  failed: 'Failed',
}

export const fulfilmentLabel = (state: string) => LABELS[state] ?? state

// The service order carries the product order id in externalReference.
export function fulfilmentFor(orderId: string, serviceOrders: ServiceOrder[]): ServiceOrder | undefined {
  return serviceOrders.find((so) => so.externalReference.some((r) => r.id === orderId))
}

const STATES: Record<string, string> = {
  feasibilityChecked: 'Checked',
  designed: 'Designed',
  reserved: 'Reserved',
  inactive: 'Inactive',
  active: 'Active',
  suspended: 'Suspended',
  terminated: 'Terminated',
}
export const serviceStateLabel = (state: string) => STATES[state] ?? state
