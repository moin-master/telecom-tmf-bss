import { Link } from 'react-router-dom'
import { componentEmoji, roleLabel, type BundlePart } from '../lib/configure'
import { phoneNumber } from '../lib/format'
import { NumberPicker, type PickedNumber } from './NumberPicker'

type Props = {
  part: Pick<BundlePart, 'id' | 'name' | 'role'>
  // Set when the part belongs to a bundle.
  bundleName?: string
  // The number already reserved for this cart line, if any.
  saved: string | null
  picked: PickedNumber | null
  onPick: (number: PickedNumber) => void
  onReserve: () => void
  // Open the picker again to swap a reserved number for another.
  changing: boolean
  onChange: (changing: boolean) => void
  reserving: boolean
  error: string | null
}

// The configuration of the selected offer: a number picker for a SIM or eSIM, a plain message for the rest.
export function ConfigPanel({
  part,
  bundleName,
  saved,
  picked,
  onPick,
  onReserve,
  changing,
  onChange,
  reserving,
  error,
}: Props) {
  const showPicker = !saved || changing
  return (
    <section className="cpanel" aria-live="polite" aria-label={`Configuration of ${part.name}`}>
      <header className="cpanel__head">
        <span className="cpanel__icon" aria-hidden="true">
          {componentEmoji(part.role, part.name)}
        </span>
        <div>
          <p className="cpanel__eyebrow">
            Configuring {roleLabel(part.role).toLowerCase()}
            {bundleName && <> in {bundleName}</>}
          </p>
          <h2 className="cpanel__name">{part.name}</h2>
        </div>
        <Link to={`/offers/${part.id}`} className="cpanel__view">
          View offer
        </Link>
      </header>

      {part.role !== 'sim' && (
        <p className="cpanel__none">
          Nothing to configure. {part.name} is included as it is, so there is nothing to choose.
        </p>
      )}

      {part.role === 'sim' && saved && !changing && (
        <div className="reserved">
          <p className="reserved__label">Reserved for {part.name}</p>
          <p className="reserved__number">{phoneNumber(saved)}</p>
          <p className="receipt__note">The number is held for you while it is in your cart.</p>
          <button type="button" className="btn btn--ghost" onClick={() => onChange(true)}>
            Change number
          </button>
        </div>
      )}

      {part.role === 'sim' && showPicker && (
        <>
          <NumberPicker offerName={part.name} picked={picked?.id ?? null} onPick={onPick} />
          {error && (
            <p className="add__error" role="alert">
              {error}
            </p>
          )}
          <div className="configure__actions">
            <button type="button" className="btn btn--big" disabled={!picked || reserving} onClick={onReserve}>
              {reserving ? 'Reserving' : 'Reserve this number'}
            </button>
            {saved && (
              <button type="button" className="configure__keep" onClick={() => onChange(false)}>
                Keep {phoneNumber(saved)}
              </button>
            )}
          </div>
        </>
      )}
    </section>
  )
}
