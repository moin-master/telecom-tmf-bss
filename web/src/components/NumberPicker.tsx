import { useDeferredValue, useState } from 'react'
import { useAvailableNumbers } from '../hooks/useAvailableNumbers'
import { phoneNumber } from '../lib/format'
import { ErrorState } from './StateViews'

export type PickedNumber = { id: string; value: string }

type Props = { offerName: string; picked: string | null; onPick: (number: PickedNumber) => void }

// Free numbers from the resource inventory, filtered by the digits typed.
export function NumberPicker({ offerName, picked, onPick }: Props) {
  const [search, setSearch] = useState('')
  const deferred = useDeferredValue(search.trim())
  const numbers = useAvailableNumbers(deferred)

  return (
    <section className="picker" aria-labelledby="picker-title">
      <h3 id="picker-title" className="picker__title">
        Choose a phone number for {offerName}
      </h3>
      <label className="picker__search">
        <span className="sr-only">Search by digits</span>
        <input
          type="search"
          inputMode="numeric"
          placeholder="Search by digits, for example 170"
          value={search}
          onChange={(e) => setSearch(e.target.value.replace(/\D/g, ''))}
        />
      </label>

      {numbers.isError && <ErrorState error={numbers.error} onRetry={() => numbers.refetch()} />}
      {numbers.isPending && <p className="picker__note" aria-busy="true">Loading numbers</p>}
      {numbers.data && numbers.data.length === 0 && (
        <p className="picker__note">No free number contains {deferred}.</p>
      )}
      {numbers.data && numbers.data.length > 0 && (
        <>
          <p className="picker__note" aria-live="polite">
            {numbers.data.length} free {numbers.data.length === 1 ? 'number' : 'numbers'}
          </p>
          <ul className="picker__grid">
            {numbers.data.map((n) => (
              <li key={n.id}>
                <button
                  type="button"
                  className="picker__num"
                  aria-pressed={picked === n.id}
                  onClick={() => onPick({ id: n.id, value: n.value })}
                >
                  {phoneNumber(n.value)}
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  )
}
