import { Link } from 'react-router-dom'
import { useMyServices } from '../hooks/useMyServices'
import { phoneNumber, shortDate } from '../lib/format'
import { serviceStateLabel } from '../lib/fulfilment'
import { ListSkeleton } from './ListSkeleton'
import { ErrorState, StateCard } from './StateViews'

// Services tab: what the customer has, with the phone number from the TEL_MSISDN characteristic.
export function AccountServices() {
  const services = useMyServices()

  if (services.isPending) return <ListSkeleton label="Loading services" />
  if (services.isError) return <ErrorState error={services.error} onRetry={() => services.refetch()} />
  if (services.data.length === 0) {
    return (
      <StateCard
        emoji="📶"
        title="No services yet"
        action={
          <Link to="/" className="btn">
            Browse offers
          </Link>
        }
      >
        Your services appear here once an order has been fulfilled.
      </StateCard>
    )
  }

  return (
    <ul className="rows" aria-label="Services">
      {services.data.map((s) => {
        const msisdn = s.serviceCharacteristic.find((c) => c.name === 'TEL_MSISDN')?.value
        const number = msisdn ? phoneNumber(msisdn) : s.supportingResource[0]?.name
        return (
          <li key={s.id} className="row">
            <div className="row__main">
              <p className="row__title">{s.name}</p>
              <p className="row__meta">Service {s.id}</p>
            </div>
            <dl className="row__facts">
              <div>
                <dt>State</dt>
                <dd>
                  <span className="state-pill">{serviceStateLabel(s.state)}</span>
                </dd>
              </div>
              <div>
                <dt>Number</dt>
                <dd>{number ?? 'None'}</dd>
              </div>
              <div>
                <dt>Started</dt>
                <dd>{shortDate(s.startDate) || 'Not started'}</dd>
              </div>
            </dl>
          </li>
        )
      })}
    </ul>
  )
}
