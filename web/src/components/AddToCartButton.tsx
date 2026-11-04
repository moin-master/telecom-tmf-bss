import { useEffect, useState } from 'react'
import { useCart } from '../hooks/useCart'
import { apiError } from '../lib/errors'
import type { CartChoice } from '../lib/purchase'
import { Burst } from './Burst'

type Props = {
  offering: { id: string; name: string }
  quantity?: number
  choice?: CartChoice
  // Optional extras ticked by the shopper; each is added as its own line with the same quantity.
  extras?: { id: string; name: string }[]
  sellable?: boolean
  // Replaces the default "add" with another action, such as updating a cart line.
  run?: () => Promise<void>
  label?: string
  doneLabel?: string
  disabled?: boolean
}

export function AddToCartButton({
  offering,
  quantity = 1,
  choice,
  extras = [],
  sellable = true,
  run,
  label = 'Add to cart',
  doneLabel = 'Added ✓',
  disabled = false,
}: Props) {
  const { add } = useCart()
  const [pending, setPending] = useState(false)
  const [done, setDone] = useState(false)
  // The confirmation is fixed when the shopper clicks, because the panel may switch from add to update right after.
  const [doneText, setDoneText] = useState(doneLabel)
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
      if (run) {
        await run()
      } else {
        await add(offering, quantity, choice)
      }
      for (const extra of extras) {
        try {
          await add(extra, quantity)
        } catch (e) {
          throw new Error(`${offering.name} was added, but ${extra.name} was not: ${apiError(e).message}`)
        }
      }
      setBurst((n) => n + 1)
      setDoneText(doneLabel)
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
        disabled={!sellable || pending || disabled}
      >
        {!sellable ? 'Not for sale' : pending ? (run ? 'Saving…' : 'Adding…') : done ? doneText : label}
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
