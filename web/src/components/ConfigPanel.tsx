import { Link } from 'react-router-dom'
import { componentEmoji, roleLabel, type BundlePart } from '../lib/configure'
import { NumberPicker } from './NumberPicker'

type Props = {
  part: Pick<BundlePart, 'id' | 'name' | 'role'>
  // Set when the part belongs to a bundle.
  bundleName?: string
  picked: string | null
  onPick: (value: string) => void
}

// The configuration of the selected offer: a number picker for a SIM or eSIM, a plain message for the rest.
export function ConfigPanel({ part, bundleName, picked, onPick }: Props) {
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

      {part.role === 'sim' ? (
        <>
          <NumberPicker offerName={part.name} picked={picked} onPick={onPick} />
          <div className="configure__actions">
            <button type="button" className="btn btn--big" disabled>
              Reserve this number
            </button>
            <p className="receipt__note">
              Reserving comes in the next step. Today this page lists the numbers that are free in the resource
              inventory.
            </p>
          </div>
        </>
      ) : (
        <p className="cpanel__none">
          Nothing to configure. {part.name} is included as it is, so there is nothing to choose.
        </p>
      )}
    </section>
  )
}
