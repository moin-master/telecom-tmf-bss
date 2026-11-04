import type { CSSProperties } from 'react'

const COLORS = ['#fff700', '#1c1c1a', '#fffb80', '#999400', '#fff700']

// Confetti dots around the parent. Changing `n` replays it; reduced motion hides it in CSS.
export function Burst({ n }: { n: number }) {
  if (n === 0) return null
  return (
    <span className="burst" key={n} aria-hidden="true">
      {Array.from({ length: 14 }, (_, i) => (
        <span
          key={i}
          style={{ '--a': `${i * (360 / 14)}deg`, '--d': `${56 + (i % 3) * 16}px`, '--c': COLORS[i % COLORS.length] } as CSSProperties}
        />
      ))}
    </span>
  )
}
