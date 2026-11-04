import { useId } from 'react'
import { useOffer } from '../hooks/useOffers'
import { money, perLabel } from '../lib/format'

type Props = {
  offerId: string
  checked: boolean
  onChange: (checked: boolean) => void
}

// An optional extra offered with another offer. It loads the extra's own offer, so every card shares one request.
export function ProtectionAddOn({ offerId, checked, onChange }: Props) {
  const id = useId()
  const extra = useOffer(offerId)
  if (!extra.data || !extra.data.isSellable) return null

  const fee = extra.data.productOfferingPrice.find((p) => p.price)
  const covered = extra.data.productSpecification?.productSpecCharacteristic.find((c) => c.name === 'coverage')

  return (
    <div className="addon">
      <input id={id} type="checkbox" checked={checked} onChange={(e) => onChange(e.target.checked)} />
      <label htmlFor={id} className="addon__box">
        <span className="addon__title">
          Add {extra.data.name}
          {fee?.price && (
            <b>
              +{money(fee.price.unit, fee.price.value)}
              {perLabel(fee.recurringChargePeriodType)}
            </b>
          )}
        </span>
        {covered && <span className="addon__hint">{covered.values.join(' · ')}</span>}
      </label>
    </div>
  )
}
