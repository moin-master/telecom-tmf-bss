import type { ReactNode } from 'react'
import { useOffer } from '../hooks/useOffers'
import { componentEmoji, roleLabel, type BundlePart } from '../lib/configure'

type Props = {
  part: BundlePart
  selected: boolean
  onSelect: () => void
  // The line under the description: what the shopper still has to do here.
  status: ReactNode
}

// One component of the bundle. The tile is a button: selecting it shows its configuration below the tree.
export function BundleNode({ part, selected, onSelect, status }: Props) {
  const offer = useOffer(part.id)
  const classes = ['tree__kid', part.optional ? 'is-optional' : '', selected ? 'is-selected' : '']
  return (
    <li className={classes.filter(Boolean).join(' ')}>
      <button type="button" className="node" aria-pressed={selected} onClick={onSelect}>
        <span className="node__icon" aria-hidden="true">
          {componentEmoji(part.role, part.name)}
        </span>
        <span className="node__role">
          {roleLabel(part.role)} <span>{part.optional ? 'Optional' : 'Included'}</span>
        </span>
        <span className="node__name">{part.name}</span>
        {offer.data?.description && <span className="node__desc">{offer.data.description}</span>}
        {status}
      </button>
    </li>
  )
}
