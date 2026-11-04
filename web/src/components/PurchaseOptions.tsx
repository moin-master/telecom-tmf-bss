import { useId } from 'react'
import { OPTIONS, type PurchaseOption } from '../lib/purchase'

type Props = {
  available: typeof OPTIONS
  value: PurchaseOption
  onChange: (option: PurchaseOption) => void
  // Cards are narrow, so the short hints are left out there.
  compact?: boolean
}

// A radio group drawn as cards, so it works with the keyboard and screen readers out of the box.
export function PurchaseOptions({ available, value, onChange, compact = false }: Props) {
  const name = useId()
  return (
    <fieldset className={`options${compact ? ' options--compact' : ''}`}>
      <legend className="options__legend">How do you want to buy it?</legend>
      <div className="options__row">
        {available.map((o) => (
          <label key={o.key} className="option">
            <input
              type="radio"
              name={name}
              value={o.key}
              checked={value === o.key}
              onChange={() => onChange(o.key)}
            />
            <span className="option__label">{o.label}</span>
            <span className="option__hint">{o.hint}</span>
          </label>
        ))}
      </div>
    </fieldset>
  )
}
