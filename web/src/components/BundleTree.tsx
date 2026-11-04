import type { ReactNode } from 'react'
import { bundleParts, type BundlePart } from '../lib/configure'
import { BundleNode } from './BundleNode'
import type { OfferData } from './OfferInfo'

type Credit = { name: string; amount: string }

type Props = {
  offer: OfferData
  selectedId: string
  onSelect: (id: string) => void
  status: (part: BundlePart) => ReactNode
  credits?: Credit[]
}

// The bundle as a tree: the bundle on top, its components joined to it, discounts hanging underneath.
// The tiles are the tabs of the configure page.
export function BundleTree({ offer, selectedId, onSelect, status, credits = [] }: Props) {
  const kids = bundleParts(offer)

  return (
    <section className="tree" aria-label={`${offer.name} structure`}>
      <div className="tree__root">
        <span className="tree__rootname">{offer.name}</span>
        <span className="tree__rootkind">Bundle</span>
      </div>
      <div className="tree__stem" aria-hidden="true" />
      <ul className="tree__kids" style={{ '--n': kids.length } as React.CSSProperties}>
        {kids.map((k) => (
          <BundleNode
            key={k.id}
            part={k}
            selected={k.id === selectedId}
            onSelect={() => onSelect(k.id)}
            status={status(k)}
          />
        ))}
      </ul>

      {credits.length > 0 && (
        <div className="tree__credits">
          <h3>Discounts on this bundle</h3>
          <ul>
            {credits.map((c, i) => (
              <li key={i}>
                <span>{c.name}</span>
                <b>{c.amount}</b>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  )
}
