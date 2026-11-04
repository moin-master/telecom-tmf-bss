// Amounts arrive from the API as decimal strings. They are only formatted here;
// totals are always calculated by the backend.
export function money(unit: string, value: string): string {
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency: unit }).format(Number(value))
  } catch {
    return `${value} ${unit}`
  }
}

// "dataAllowance" -> "data allowance"
export const humanize = (name: string) => name.replace(/([a-z])([A-Z])/g, '$1 $2').toLowerCase()

type Price = {
  id?: string
  name: string
  priceType: string
  recurringChargePeriodType?: string | null
  price?: { unit: string; value: string } | null
}

export function perLabel(period?: string | null): string {
  return period ? `/${period === 'month' ? 'mo' : period}` : ''
}

// The headline price is the recurring fee if there is one, otherwise the first one-time price.
export function headlinePrice<T extends Price>(prices: T[]): T | undefined {
  const priced = prices.filter((p) => p.price)
  return priced.find((p) => p.priceType === 'recurring') ?? priced[0]
}

export function otherPrices<T extends Price>(prices: T[], headline?: T): T[] {
  return prices.filter((p) => p.price && p !== headline)
}

// "9991702283968" -> "+999 170 2283968" (country code, network, subscriber)
export function phoneNumber(msisdn: string): string {
  return msisdn.length > 6 ? `+${msisdn.slice(0, 3)} ${msisdn.slice(3, 6)} ${msisdn.slice(6)}` : `+${msisdn}`
}
