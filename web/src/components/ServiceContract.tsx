import { Link } from 'react-router-dom'
import { shortDate } from '../lib/format'
import type { Contract } from '../lib/serviceTree'

// The contract looks like the one chosen in the cart. It is not stored on the service: it is the
// term of the product order item, so the link goes to the order that holds it.
export function ServiceContract({ contract }: { contract: Contract }) {
  const start = shortDate(contract.startDate)
  const end = shortDate(contract.endDate)
  return (
    <div className="contract contract--service is-on">
      <span className="contract__title">Contract · {contract.months} months</span>
      <span className="contract__state">{end ? `Ends ${end}` : 'Not started'}</span>
      <span className="contract__hint">
        {start ? `Started ${start} · ` : 'Starts when the service is active · '}
        <Link to={`/orders/${contract.orderId}`}>
          {contract.orderId} · item {contract.itemNumber}
        </Link>
      </span>
    </div>
  )
}
