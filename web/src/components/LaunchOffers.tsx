import { useId } from 'react'

type Props = {
  offers: { id: string; name: string }[]
  value: string | undefined
  onChange: (id: string) => void
}

const sentence = (text: string) => text.charAt(0).toUpperCase() + text.slice(1)

// The shopper picks one of the first-6-months discounts.
export function LaunchOffers({ offers, value, onChange }: Props) {
  const name = useId()
  return (
    <fieldset className="options options--stack">
      <legend className="options__legend">First 6 months, pick one</legend>
      <div className="options__row">
        {offers.map((o) => (
          <label key={o.id} className="option">
            <input type="radio" name={name} value={o.id} checked={value === o.id} onChange={() => onChange(o.id)} />
            <span className="option__label">{sentence(o.name.replace(/^Launch offer: /, ''))}</span>
          </label>
        ))}
      </div>
    </fieldset>
  )
}
