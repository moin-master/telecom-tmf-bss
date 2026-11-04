// Each category gets its own tint and emoji so the grid feels alive but organised.
export type Theme = { key: string; emoji: string; label: string }

const THEMES: Record<string, Theme> = {
  plans: { key: 'violet', emoji: '📶', label: 'Plans' },
  devices: { key: 'mint', emoji: '📱', label: 'Devices' },
  addons: { key: 'pink', emoji: '✨', label: 'Add-ons' },
  prepaid: { key: 'sky', emoji: '💳', label: 'Prepaid' },
}

const FALLBACK = [
  { key: 'sun', emoji: '⚡' },
  { key: 'pink', emoji: '🔥' },
  { key: 'sky', emoji: '🫧' },
  { key: 'mint', emoji: '🌀' },
]

const slug = (name: string) => name.toLowerCase().replace(/[^a-z]/g, '')

export function categoryTheme(id: string, name: string): Theme {
  const known = THEMES[slug(name)]
  if (known) return known
  let hash = 0
  for (const ch of id) hash = (hash * 31 + ch.charCodeAt(0)) >>> 0
  const pick = FALLBACK[hash % FALLBACK.length]
  return { ...pick, label: name }
}

// An offer takes the theme of its most specific known category (devices before prepaid).
const PREFERENCE = ['devices', 'addons', 'plans', 'prepaid']

export function offerTheme(categories: { id: string; name: string }[]): Theme {
  const sorted = [...categories].sort(
    (a, b) => PREFERENCE.indexOf(slug(a.name)) - PREFERENCE.indexOf(slug(b.name)),
  )
  const first = sorted.find((c) => slug(c.name) in THEMES) ?? categories[0]
  return first ? categoryTheme(first.id, first.name) : { key: 'sun', emoji: '⚡', label: 'Offer' }
}

export function offerEmoji(name: string, theme: Theme): string {
  const n = name.toLowerCase()
  if (n.includes('sim')) return '💳'
  if (n.includes('roaming')) return '✈️'
  if (n.includes('phone')) return '📱'
  if (n.includes('plan')) return '📶'
  return theme.emoji
}
