import { useOffer } from '../hooks/useOffers'

// A rule the cart applies by itself, explained in the offer's own words.
export function DealNote({ id }: { id: string }) {
  const offer = useOffer(id)
  if (!offer.data) return null
  return (
    <p className="deal-note">
      <b>{offer.data.name}</b> {offer.data.description}
    </p>
  )
}
