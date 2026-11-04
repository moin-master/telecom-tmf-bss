import { useEffect, useState } from 'react'
import { useCart } from '../hooks/useCart'
import { apiError } from '../lib/errors'
import type { PurchaseOption } from '../lib/purchase'
import { Burst } from './Burst'

type Props = {
  offering: { id: string; name: string }
  quantity?: number
  option?: PurchaseOption
  // Optional extras ticked by the shopper; each is added as its own line with the same quantity.
  extras?: { id: string; name: string }[]
  sellable?: boolean
}

export function AddToCartButton({ offering, quantity = 1, option, extras = [], sellable = true }: Props) {
  const { add } = useCart()
  const [pending, setPending] = useState(false)
  const [done, setDone] = useState(false)
  const [burst, setBurst] = useState(0)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!done) return
    const timer = window.setTimeout(() => setDone(false), 1600)
    return () => window.clearTimeout(timer)
  }, [done])

  async function onClick() {
    setError(null)
    setPending(true)
    try {
      await add(offering, quantity, option)
      for (const extra of extras) {
        try {
          await add(extra, quantity)
        } catch (e) {
          throw new Error(`${offering.name} was added, but ${extra.name} was not: ${apiError(e).message}`)
        }
      }
      setBurst((n) => n + 1)
      setDone(true)
    } catch (e) {
      setError(apiError(e).message)
    } finally {
      setPending(false)
    }
  }

  return (
    <div className="add">
      <button
        type="button"
        className={`btn${done ? ' is-done' : ''}`}
        onClick={onClick}
        disabled={!sellable || pending}
      >
        {!sellable ? 'Not for sale' : pending ? 'Adding…' : done ? 'Added ✓' : 'Add to cart'}
      </button>
      <Burst n={burst} />
      {error && (
        <p className="add__error" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}
