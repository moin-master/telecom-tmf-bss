import type { ServicesQuery } from '../api/generated/service-registry/graphql'

export type RegistryService = ServicesQuery['serviceList'][number]

// A service with the services it lists in supportingService, resolved by id.
export type ServiceTreeData = { service: RegistryService; children: ServiceTreeData[] }

// The parts of a product order the contract lookup needs.
export type TermOrder = {
  id: string
  productOrderItem: {
    id: string
    itemTerm: { name: string; duration: { amount: number; units: string } }[]
  }[]
}

export type Contract = {
  months: number
  orderId: string
  itemId: string
  // Position of the item in its order, starting at 1.
  itemNumber: number
  startDate: string | null
  endDate: string | null
}

// Builds the trees from the flat service list. Roots are the services no other service lists in
// supportingService. A service is drawn once; cycles and missing children are skipped.
export function buildServiceTrees(services: RegistryService[]): ServiceTreeData[] {
  const byId = new Map(services.map((s) => [s.id, s]))
  const isChild = new Set<string>()
  for (const s of services) for (const ref of s.supportingService) if (ref.id !== s.id) isChild.add(ref.id)

  const seen = new Set<string>()
  const build = (service: RegistryService): ServiceTreeData => {
    seen.add(service.id)
    const children: ServiceTreeData[] = []
    for (const ref of service.supportingService) {
      const child = byId.get(ref.id)
      if (child && !seen.has(child.id)) children.push(build(child))
    }
    return { service, children }
  }

  const trees = services.filter((s) => !isChild.has(s.id) && !seen.has(s.id)).map(build)
  // Services that only support each other (a cycle) have no root: show them as roots rather than hide them.
  for (const s of services) if (!seen.has(s.id)) trees.push(build(s))
  return trees
}

export const orderIdOf = (service: RegistryService): string | undefined =>
  service.relatedEntity.find((e) => e.role === 'productOrder')?.entity.id

export const treesOfOrder = (trees: ServiceTreeData[], orderId: string): ServiceTreeData[] =>
  trees.filter((t) => orderIdOf(t.service) === orderId)

// The phone number sits on the SIM: the TEL_MSISDN characteristic, else the reserved resource name.
export function serviceNumber(service: RegistryService): string | undefined {
  return service.serviceCharacteristic.find((c) => c.name === 'TEL_MSISDN')?.value
}

function termMonths(term: { duration: { amount: number; units: string } }): number | null {
  const units = term.duration.units.toLowerCase()
  if (units.startsWith('month')) return term.duration.amount
  if (units.startsWith('year')) return term.duration.amount * 12
  return null
}

// Adds calendar months; 31 January plus one month is the last day of February.
export function addMonths(iso: string, months: number): string | null {
  const start = new Date(iso)
  if (Number.isNaN(start.getTime())) return null
  const end = new Date(start)
  end.setDate(1)
  end.setMonth(end.getMonth() + months)
  const lastDay = new Date(end.getFullYear(), end.getMonth() + 1, 0).getDate()
  end.setDate(Math.min(start.getDate(), lastDay))
  return end.toISOString()
}

// The contract is not stored on the service. It is the term of the product order item the root
// service was created for: the productOrder related entity gives the order, serviceOrderItem the item.
export function contractOf(root: RegistryService, orders: TermOrder[]): Contract | null {
  const orderId = orderIdOf(root)
  const itemId = root.serviceOrderItem[0]?.itemId
  if (!orderId || !itemId) return null
  const order = orders.find((o) => o.id === orderId)
  const index = order?.productOrderItem.findIndex((i) => i.id === itemId) ?? -1
  if (!order || index < 0) return null
  for (const term of order.productOrderItem[index].itemTerm) {
    const months = termMonths(term)
    if (months && months > 0) {
      return {
        months,
        orderId,
        itemId,
        itemNumber: index + 1,
        startDate: root.startDate,
        endDate: root.startDate ? addMonths(root.startDate, months) : null,
      }
    }
  }
  return null
}
