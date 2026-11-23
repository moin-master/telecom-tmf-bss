import { offerEmoji, offerTheme } from '../lib/theme'

type Props = {
  name: string
  src?: string
  // Extra order lines beyond the first, shown as a "+N" badge.
  more?: number
  size?: 'card' | 'hero'
}

// The picture of an order's first item. The name sits next to it, so the image has an empty alt.
// Without a picture the tile shows the same emoji the offer cards use.
export function OrderImage({ name, src, more = 0, size = 'card' }: Props) {
  return (
    <div className={`order-image order-image--${size}`}>
      {src ? (
        <img src={src} alt="" width={160} height={160} loading="lazy" />
      ) : (
        <span className="order-image__emoji" aria-hidden="true">
          {offerEmoji(name, offerTheme([]))}
        </span>
      )}
      {more > 0 && (
        <span className="order-image__more">
          <span aria-hidden="true">+{more}</span>
          <span className="sr-only">and {more} more {more === 1 ? 'item' : 'items'}</span>
        </span>
      )}
    </div>
  )
}
