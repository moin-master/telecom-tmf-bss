import { useId } from 'react'

export type Mode = 'build' | 'update'

type Props = {
  value: Mode
  onChange: (mode: Mode) => void
}

// Shown only when the offer is already in the cart: start a new line or change the one there.
export function ModeSwitch({ value, onChange }: Props) {
  const name = useId()
  const choices: { key: Mode; label: string; hint: string }[] = [
    { key: 'update', label: 'Update offer in cart', hint: 'Change what you already added' },
    { key: 'build', label: 'Build new offer', hint: 'Add it again with other choices' },
  ]
  return (
    <fieldset className="options options--two">
      <legend className="options__legend">This offer is already in your cart</legend>
      <div className="options__row">
        {choices.map((c) => (
          <label key={c.key} className="option">
            <input type="radio" name={name} value={c.key} checked={value === c.key} onChange={() => onChange(c.key)} />
            <span className="option__label">{c.label}</span>
            <span className="option__hint">{c.hint}</span>
          </label>
        ))}
      </div>
    </fieldset>
  )
}
