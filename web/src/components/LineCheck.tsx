import { Link } from 'react-router-dom'
import type { CartFieldsFragment } from '../api/generated/shopping-cart/graphql'
import { useOffer } from '../hooks/useOffers'
import { needsNumber } from '../lib/configure'
import { phoneNumber } from '../lib/format'

type Item = CartFieldsFragment['cartItem'][number]

// One cart line in the order check: ready, or what is still missing.
export function LineCheck({ item }: { item: Item }) {
  const offer = useOffer(item.productOffering.id)
  const number = item.product?.productCharacteristic.find((c) => c.name === 'TEL_MSISDN')?.value
  const missing = !!offer.data && needsNumber(offer.data) && !item.product

  return (
    <li className={missing ? 'check is-open' : 'check'}>
      <span className="check__mark" aria-hidden="true">
        {missing ? '!' : '✓'}
      </span>
      <span className="check__text">
        {item.productOffering.name}
        {number && <span className="check__detail"> · {phoneNumber(number)}</span>}
        {missing && <span className="check__detail"> needs a phone number</span>}
      </span>
      {missing && (
        <Link to={`/cart/items/${item.id}/configure`} className="link-action">
          Configure
        </Link>
      )}
    </li>
  )
}
