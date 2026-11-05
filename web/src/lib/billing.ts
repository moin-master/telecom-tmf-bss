import type { BillingAccountFieldsFragment } from '../api/generated/account/graphql'

export type BillingAccount = BillingAccountFieldsFragment

// The first address and the first e-mail of the account's contacts.
export function addressOf(account: BillingAccount) {
  for (const contact of account.contact) {
    for (const m of contact.contactMedium) {
      if (m.__typename === 'GeographicAddressContactMedium') return m
    }
  }
  return undefined
}

export function emailOf(account: BillingAccount): string | undefined {
  for (const contact of account.contact) {
    for (const m of contact.contactMedium) {
      if (m.__typename === 'EmailContactMedium') return m.emailAddress
    }
  }
  return undefined
}

export function addressLine(account: BillingAccount): string {
  const a = addressOf(account)
  if (!a) return ''
  return [a.street1, a.street2, a.city, a.stateOrProvince, a.postCode, a.country].filter(Boolean).join(', ')
}
