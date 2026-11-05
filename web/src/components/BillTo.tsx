import { useBillingAccount } from '../hooks/useBillingAccounts'
import { addressLine, emailOf } from '../lib/billing'

// Who is billed for an order: the billing account's name, address and e-mail.
export function BillTo({ accountId }: { accountId: string }) {
  const account = useBillingAccount(accountId)
  if (!account.data) return null
  return (
    <div className="order__item">
      <p className="order__name">Billed to {account.data.name}</p>
      <p className="order__detail">{account.data.contact[0]?.contactName}</p>
      <p className="order__detail">{addressLine(account.data)}</p>
      <p className="order__detail">Bills are sent to {emailOf(account.data)}</p>
    </div>
  )
}
