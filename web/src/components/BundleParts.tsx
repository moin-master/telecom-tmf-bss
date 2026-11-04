import { Link } from 'react-router-dom'
import { componentEmoji, roleLabel } from '../lib/configure'
import { phoneNumber } from '../lib/format'

type Component = { id: string; name: string; role: string }

type Props = {
  components: Component[]
  // Set when the SIM part still needs a number: the SIM tile then carries the Configure button.
  configureHref?: string
  // The reserved number, once the shopper has one.
  number?: string | null
}

// The bundle's parts as quiet tiles in the order of the tree on the configure page.
export function BundleParts({ components, configureHref, number }: Props) {
  return (
    <ul className="parts" aria-label="Includes">
      {components.map((c) => {
        const isSim = c.role === 'sim' && !!configureHref
        const open = isSim && !number
        return (
          <li key={c.id} className={open ? 'part is-open' : 'part'}>
            <p className="part__role">
              <span aria-hidden="true">{componentEmoji(c.role, c.name)}</span> {roleLabel(c.role)}
            </p>
            <p className="part__name">{c.name}</p>
            {isSim && (
              <>
                <p className="part__note">{number ? phoneNumber(number) : 'Needs a number'}</p>
                <Link to={configureHref} className="link-action">
                  {number ? 'Edit' : 'Configure'}
                </Link>
              </>
            )}
          </li>
        )
      })}
    </ul>
  )
}
