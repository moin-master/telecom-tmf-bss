import { useEffect, useMemo, useState } from 'react'
import { useBillingAccounts } from '../hooks/useBillingAccounts'
import { addressLine, emailOf } from '../lib/billing'
import { BillingForm } from './BillingForm'
import { ErrorState } from './StateViews'

type Props = { selectedId: string | null; onSelect: (id: string) => void }

// Step 2 of checkout: choose one of the shopper's billing accounts or add a new one.
export function BillingStep({ selectedId, onSelect }: Props) {
  const accounts = useBillingAccounts()
  const [adding, setAdding] = useState(false)
  const list = useMemo(() => accounts.data ?? [], [accounts.data])

  // The newest account is preselected.
  useEffect(() => {
    if (list.length > 0 && !list.some((a) => a.id === selectedId)) onSelect(list[0].id)
  }, [list, selectedId, onSelect])

  const showForm = adding || (accounts.isSuccess && list.length === 0)

  return (
    <section className="checkout" aria-labelledby="billing-title">
      <h2 id="billing-title" className="checkout__step">
        <span className="checkout__num" aria-hidden="true">
          2
        </span>
        Billing details
      </h2>

      {accounts.isError && <ErrorState error={accounts.error} onRetry={() => accounts.refetch()} />}
      {accounts.isPending && <p className="picker__note" aria-busy="true">Loading your billing accounts</p>}

      {!showForm && list.length > 0 && (
        <fieldset className="choices">
          <legend className="sr-only">Billing account</legend>
          {list.map((a) => (
            <label key={a.id} className={a.id === selectedId ? 'choice is-selected' : 'choice'}>
              <input
                type="radio"
                name="billing-account"
                checked={a.id === selectedId}
                onChange={() => onSelect(a.id)}
              />
              <span className="choice__body">
                <span className="choice__name">{a.name}</span>
                <span className="choice__line">{a.contact[0]?.contactName}</span>
                <span className="choice__line">{addressLine(a)}</span>
                <span className="choice__line">{emailOf(a)}</span>
              </span>
            </label>
          ))}
          <button type="button" className="configure__keep choices__add" onClick={() => setAdding(true)}>
            Add a new billing account
          </button>
        </fieldset>
      )}

      {showForm && (
        <BillingForm
          key={list.length}
          onCreated={(id) => {
            onSelect(id)
            setAdding(false)
          }}
          onCancel={list.length > 0 ? () => setAdding(false) : undefined}
        />
      )}
    </section>
  )
}
