import type { OfferQuery } from '../api/generated/product-catalog/graphql'

type Offer = NonNullable<OfferQuery['productOffering']>

// A bundle needs a number when it contains a SIM or eSIM; a single offer when its
// specification has the MSISDN characteristic.
export function needsNumber(offer: Offer): boolean {
  if (offer.isBundle) return offer.bundledProductOffering.some((b) => b.role === 'sim')
  return !!offer.productSpecification?.productSpecCharacteristic.some((c) => c.name === 'MSISDN')
}

const ROLE_LABEL: Record<string, string> = { device: 'Device', plan: 'Plan', sim: 'SIM', addOn: 'Add-on' }

export const roleLabel = (role: string) => ROLE_LABEL[role] ?? role

// Emoji are illustrations only; the name and role are always in text next to them.
export function componentEmoji(role: string, name: string): string {
  const n = name.toLowerCase()
  if (role === 'device') return '📱'
  if (role === 'plan') return '📶'
  if (role === 'sim') return n.includes('esim') ? '📲' : '💳'
  if (n.includes('roaming')) return '✈️'
  if (n.includes('protection')) return '🛡️'
  return '✨'
}

export type BundlePart = { id: string; name: string; role: string; optional: boolean }

// The tiles of the bundle tree: the bundled offerings, then the optional add-ons the bundle points to.
export function bundleParts(offer: Offer): BundlePart[] {
  const parts = offer.bundledProductOffering.map((b) => ({
    id: b.id,
    name: b.name,
    role: b.role,
    optional: b.bundledProductOfferingOption.numberRelOfferLowerLimit === 0,
  }))
  const extras = offer.productOfferingRelationship
    .filter((r) => r.relationshipType === 'addOn')
    .map((r) => ({ id: r.id, name: r.name, role: 'addOn', optional: true }))
  return [...parts, ...extras]
}

// The tile that opens first: the one that needs configuration.
export const firstToConfigure = (parts: BundlePart[]) => (parts.find((p) => p.role === 'sim') ?? parts[0])?.id
