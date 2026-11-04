import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { BundleTree } from '../components/BundleTree'
import { ConfigPanel } from '../components/ConfigPanel'
import type { PickedNumber } from '../components/NumberPicker'
import { ErrorState, StateCard } from '../components/StateViews'
import { useCart } from '../hooks/useCart'
import { useOffer } from '../hooks/useOffers'
import { apiError } from '../lib/errors'
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
  const { cart, loading, configure, busy } = useCart()
  const item = cart?.cartItem.find((i) => i.id === itemId)
  const offer = useOffer(item?.productOffering.id ?? '')
  const [picked, setPicked] = useState<PickedNumber | null>(null)
  const [changing, setChanging] = useState(false)
  const [error, setError] = useState<string | null>(null)
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

  // The number reserved for this line is kept on the cart item (TMF663 product characteristic).
  const saved = item.product?.productCharacteristic.find((c) => c.name === 'TEL_MSISDN')?.value ?? null

  async function reserve() {
    if (!picked) return
    setError(null)
    try {
      await configure(item!.id, picked.id)
      setChanging(false)
    } catch (e) {
      const err = apiError(e)
      setError(err.code === 'Conflict' ? 'That number was just taken. Pick another one.' : err.message)
    }
    setPicked(null)
  }

  const credits = item.itemTotalPrice.filter(isCredit).map((p) => ({ name: p.name, amount: amount(p) }))
  const parts = data.isBundle ? bundleParts(data) : []
  const selected =
    parts.find((p) => p.id === selectedId) ?? parts.find((p) => p.id === firstToConfigure(parts)) ?? null
  // A single SIM offer has no tree: its own panel is all there is.
  const active = selected ?? { id: data.id, name: data.name, role: 'sim' }
  const status = (part: BundlePart) =>
    part.role === 'sim' ? (
      <span className={saved ? 'node__state is-set' : 'node__state'}>
        {saved ? `Reserved ${phoneNumber(saved)}` : 'Needs a number'}
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
        saved={saved}
        picked={picked}
        onPick={setPicked}
        onReserve={reserve}
        changing={changing}
        onChange={(value) => {
          setChanging(value)
          setPicked(null)
          setError(null)
        }}
        reserving={busy}
        error={error}
      />
    </div>
  )
}
