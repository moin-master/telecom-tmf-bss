// How a bundle can be bought. The catalog tags prices with one of these; untagged prices apply to every option.
export type PurchaseOption = 'own' | 'tradeIn' | 'finance'

export const OPTIONS: { key: PurchaseOption; label: string; hint: string }[] = [
  { key: 'own', label: 'Own it', hint: 'Pay for the phone today' },
  { key: 'tradeIn', label: 'Trade-in', hint: 'Credit for your old phone' },
  { key: 'finance', label: 'Finance', hint: 'Pay a little now, the rest monthly' },
]

export const optionLabel = (key?: string | null) => OPTIONS.find((o) => o.key === key)?.label

type Price = {
  priceType: string
  purchaseOption?: string | null
  price?: { unit: string; value: string } | null
}

// Options the offering has prices for, in display order. Empty for offers without options.
export function optionsOf(prices: Price[]): typeof OPTIONS {
  const present = new Set(prices.map((p) => p.purchaseOption).filter(Boolean))
  return OPTIONS.filter((o) => present.has(o.key))
}

// The prices that apply when the shopper picks `option`.
export function pricesFor<T extends Price>(prices: T[], option?: PurchaseOption): T[] {
  return prices.filter((p) => p.price && (!p.purchaseOption || p.purchaseOption === option))
}

// Quick preview for the card: due today and every month. The cart shows the totals the backend calculates.
export function preview(prices: Price[]): { unit: string; today: string; monthly: string } | null {
  const priced = prices.filter((p) => p.price)
  if (priced.length === 0) return null
  const cents = (v: string) => Math.round(Number(v) * 100)
  const sum = (type: string) =>
    priced.filter((p) => (type === 'recurring') === (p.priceType === 'recurring')).reduce((n, p) => n + cents(p.price!.value), 0)
  const fixed = (n: number) => (n / 100).toFixed(2)
  return { unit: priced[0].price!.unit, today: fixed(sum('oneTime')), monthly: fixed(sum('recurring')) }
}
