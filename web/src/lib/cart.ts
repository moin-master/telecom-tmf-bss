import { money } from './format'

type Money = { price: { taxIncludedAmount: { unit: string; value: string } } }

export const amount = (p: Money) => money(p.price.taxIncludedAmount.unit, p.price.taxIncludedAmount.value)

export const isCredit = (p: Money) => p.price.taxIncludedAmount.value.startsWith('-')

// The backend names each total ("Total per month, first 6 months"); this words it for the shopper.
export const totalLabel = (t: { name: string; priceType: string }) =>
  t.priceType === 'oneTime'
    ? 'Due today'
    : t.name.replace(/^Total per (\w+)/, (_, period: string) => `Every ${period}`)
