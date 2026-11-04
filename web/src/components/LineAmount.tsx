import { amount } from '../lib/cart'
import { money, perLabel } from '../lib/format'

type Props = {
  line: {
    recurringChargePeriod?: string | null
    price: { taxIncludedAmount: { unit: string; value: string } }
    regularPrice?: { unit: string; value: string } | null
  }
}

// The amount charged. When the catalog has a regular price, it is shown struck out before it,
// so the shopper sees the saving and that only the amount next to it is paid.
export function LineAmount({ line }: Props) {
  return (
    <b className="amount">
      {line.regularPrice && (
        <s className="amount__regular">
          <span className="sr-only">Regular price </span>
          {money(line.regularPrice.unit, line.regularPrice.value)}
        </s>
      )}
      {line.regularPrice && <span className="sr-only">You pay </span>}
      {amount(line)}
      {perLabel(line.recurringChargePeriod)}
    </b>
  )
}
