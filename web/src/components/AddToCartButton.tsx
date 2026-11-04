import { useEffect, useState } from 'react'
import { useCart } from '../hooks/useCart'
import { apiError } from '../lib/errors'
import { Burst } from './Burst'

type Props = {
  offering: { id: string; name: string }
  quantity?: number
  sellable?: boolean
}

export function AddToCartButton({ offering, quantity = 1, sellable = true }: Props) {
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
      await add(offering, quantity)
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
