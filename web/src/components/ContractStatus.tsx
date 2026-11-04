type Props = {
  name: string
  months: number
  included: boolean
  includedHint: string
  excludedHint: string
}

// The contract follows the purchase option, so it is shown as a status and not a tick box.
export function ContractStatus({ name, months, included, includedHint, excludedHint }: Props) {
  return (
    <div className={`contract${included ? ' is-on' : ''}`} role="status">
      <span className="contract__title">
        {name} · {months} months
      </span>
      <span className="contract__state">{included ? '✓ Included' : 'Not included'}</span>
      <span className="contract__hint">{included ? includedHint : excludedHint}</span>
    </div>
  )
}
