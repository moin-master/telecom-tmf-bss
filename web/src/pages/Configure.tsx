import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { BundleTree } from '../components/BundleTree'
import { ConfigPanel } from '../components/ConfigPanel'
import { ErrorState, StateCard } from '../components/StateViews'
import { useCart } from '../hooks/useCart'
import { useOffer } from '../hooks/useOffers'
import { amount, isCredit } from '../lib/cart'
import { bundleParts, firstToConfigure, needsNumber, type BundlePart } from '../lib/configure'
import { phoneNumber } from '../lib/format'

const backToCart = (
  <Link to="/cart" className="btn">
    Back to cart
  </Link>
)

export function Configure() {
  const { itemId } = useParams()
  const { cart, loading } = useCart()
  const item = cart?.cartItem.find((i) => i.id === itemId)
  const offer = useOffer(item?.productOffering.id ?? '')
  const [picked, setPicked] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)

  if (loading || (item && offer.isPending)) {
    return (
      <div className="wrap" aria-busy="true">
        <div className="skeleton__media skeleton__media--tall" />
      </div>
    )
  }
  if (!item) {
    return (
      <div className="wrap">
        <StateCard emoji="🔎" title="That cart item is not here" action={backToCart}>
          It may have been removed.
        </StateCard>
      </div>
    )
  }
  if (offer.isError) {
    return (
      <div className="wrap">
        <ErrorState error={offer.error} onRetry={() => offer.refetch()} />
      </div>
    )
  }
  const data = offer.data
  if (!data || !needsNumber(data)) {
    return (
      <div className="wrap">
        <StateCard emoji="✅" title="Nothing to configure" action={backToCart}>
          {item.productOffering.name} has no SIM, so there is no number to choose.
        </StateCard>
      </div>
    )
  }

  const credits = item.itemTotalPrice.filter(isCredit).map((p) => ({ name: p.name, amount: amount(p) }))
  const parts = data.isBundle ? bundleParts(data) : []
  const selected =
    parts.find((p) => p.id === selectedId) ?? parts.find((p) => p.id === firstToConfigure(parts)) ?? null
  // A single SIM offer has no tree: its own panel is all there is.
  const active = selected ?? { id: data.id, name: data.name, role: 'sim' }
  const status = (part: BundlePart) =>
    part.role === 'sim' ? (
      <span className={picked ? 'node__state is-set' : 'node__state'}>
        {picked ? `Number ${phoneNumber(picked)}` : 'Needs a number'}
      </span>
    ) : (
      <span className="node__none">Nothing to configure</span>
    )

  return (
    <div className="wrap configure">
      <Link to="/cart" className="configure__back">
        Back to cart
      </Link>
      <h1 className="cart__title">Configure {item.productOffering.name}</h1>

      {selected && (
        <BundleTree offer={data} selectedId={selected.id} onSelect={setSelectedId} status={status} credits={credits} />
      )}

      <ConfigPanel
        part={active}
        bundleName={selected ? data.name : undefined}
        picked={picked}
        onPick={setPicked}
      />
    </div>
  )
}
