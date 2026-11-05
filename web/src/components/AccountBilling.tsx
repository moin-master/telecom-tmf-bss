import { Link } from 'react-router-dom'
import { useBillingAccounts } from '../hooks/useBillingAccounts'
import { addressLine, emailOf } from '../lib/billing'
import { ListSkeleton } from './ListSkeleton'
import { ErrorState, StateCard } from './StateViews'

// Billing tab: read only. Accounts are created and changed at checkout.
export function AccountBilling() {
  const accounts = useBillingAccounts()

  if (accounts.isPending) return <ListSkeleton label="Loading billing accounts" />
  if (accounts.isError) return <ErrorState error={accounts.error} onRetry={() => accounts.refetch()} />
  if (accounts.data.length === 0) {
    return (
      <StateCard
        emoji="🧾"
        title="No billing accounts yet"
        action={
          <Link to="/" className="btn">
            Browse offers
          </Link>
        }
      >
        A billing account is created when you check out.
      </StateCard>
    )
  }

  return (
    <ul className="rows" aria-label="Billing accounts">
      {accounts.data.map((a) => (
        <li key={a.id} className="row">
          <div className="row__main">
            <p className="row__title">{a.name}</p>
            <p className="row__meta">Account {a.id}</p>
          </div>
          <dl className="row__facts">
            <div>
              <dt>State</dt>
              <dd>
                <span className="state-pill">{a.state}</span>
              </dd>
            </div>
            <div>
              <dt>Contact</dt>
              <dd>{a.contact[0]?.contactName ?? 'None'}</dd>
            </div>
            <div>
              <dt>E-mail</dt>
              <dd className="row__wrap">{emailOf(a) ?? 'None'}</dd>
            </div>
            <div>
              <dt>Address</dt>
              <dd>{addressLine(a) || 'None'}</dd>
            </div>
          </dl>
        </li>
      ))}
    </ul>
  )
}
