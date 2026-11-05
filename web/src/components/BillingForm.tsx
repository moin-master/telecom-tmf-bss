import { useState, type FormEvent } from 'react'
import { useAuth } from '../hooks/useAuth'
import { useCreateBillingAccount } from '../hooks/useBillingAccounts'
import { apiError } from '../lib/errors'

type Props = {
  onCreated: (id: string) => void
  // Offered when the shopper already has accounts and can go back to them.
  onCancel?: () => void
}

// A new billing account: a name, a contact (prefilled from the sign-in), an address and a bill e-mail.
export function BillingForm({ onCreated, onCancel }: Props) {
  const { profile } = useAuth()
  const create = useCreateBillingAccount()
  const [name, setName] = useState('Home')
  const [contactName, setContactName] = useState(profile?.name ?? '')
  const [street1, setStreet1] = useState('')
  const [street2, setStreet2] = useState('')
  const [city, setCity] = useState('')
  const [stateOrProvince, setStateOrProvince] = useState('')
  const [postCode, setPostCode] = useState('')
  const [country, setCountry] = useState('')
  const [email, setEmail] = useState(profile?.email ?? '')
  const [error, setError] = useState<string | null>(null)

  async function onSubmit(event: FormEvent) {
    event.preventDefault()
    setError(null)
    try {
      const account = await create.mutateAsync({
        name,
        contact: [
          {
            contactName,
            contactMedium: [
              {
                type: 'GeographicAddressContactMedium',
                street1,
                street2: street2 || null,
                city,
                stateOrProvince: stateOrProvince || null,
                postCode,
                country,
              },
              { type: 'EmailContactMedium', emailAddress: email },
            ],
          },
        ],
      })
      onCreated(account.id)
    } catch (e) {
      setError(apiError(e).message)
    }
  }

  return (
    <form className="auth billing" onSubmit={onSubmit}>
      <label className="field">
        <span>Account name</span>
        <input value={name} onChange={(e) => setName(e.target.value)} required />
      </label>
      <label className="field">
        <span>Contact name</span>
        <input value={contactName} onChange={(e) => setContactName(e.target.value)} autoComplete="name" required />
      </label>
      <label className="field">
        <span>Street</span>
        <input value={street1} onChange={(e) => setStreet1(e.target.value)} autoComplete="address-line1" required />
      </label>
      <label className="field">
        <span>Apartment, suite (optional)</span>
        <input value={street2} onChange={(e) => setStreet2(e.target.value)} autoComplete="address-line2" />
      </label>
      <div className="auth__row">
        <label className="field">
          <span>City</span>
          <input value={city} onChange={(e) => setCity(e.target.value)} autoComplete="address-level2" required />
        </label>
        <label className="field">
          <span>State or province (optional)</span>
          <input value={stateOrProvince} onChange={(e) => setStateOrProvince(e.target.value)} autoComplete="address-level1" />
        </label>
      </div>
      <div className="auth__row">
        <label className="field">
          <span>Post code</span>
          <input value={postCode} onChange={(e) => setPostCode(e.target.value)} autoComplete="postal-code" required />
        </label>
        <label className="field">
          <span>Country</span>
          <input value={country} onChange={(e) => setCountry(e.target.value)} autoComplete="country-name" required />
        </label>
      </div>
      <label className="field">
        <span>Email for bills</span>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="email" required />
      </label>
      {error && (
        <p className="add__error" role="alert">
          {error}
        </p>
      )}
      <div className="billing__actions">
        <button type="submit" className="btn btn--big" disabled={create.isPending}>
          {create.isPending ? 'Saving' : 'Save billing details'}
        </button>
        {onCancel && (
          <button type="button" className="configure__keep" onClick={onCancel}>
            Use an existing account
          </button>
        )}
      </div>
    </form>
  )
}
