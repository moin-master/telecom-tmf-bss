import { Link } from 'react-router-dom'
import { componentEmoji, roleLabel } from '../lib/configure'

type Component = { id: string; name: string; role: string }

type Props = {
  components: Component[]
  // Set when the SIM part still needs a number: the SIM tile then carries the Configure button.
  configureHref?: string
}

// The bundle's parts as quiet tiles in the order of the tree on the configure page.
export function BundleParts({ components, configureHref }: Props) {
  return (
    <ul className="parts" aria-label="Includes">
      {components.map((c) => {
        const open = c.role === 'sim' && !!configureHref
        return (
          <li key={c.id} className={open ? 'part is-open' : 'part'}>
            <p className="part__role">
              <span aria-hidden="true">{componentEmoji(c.role, c.name)}</span> {roleLabel(c.role)}
            </p>
            <p className="part__name">{c.name}</p>
            {open && (
              <>
                <p className="part__note">Needs a number</p>
                <Link to={configureHref} className="link-action">
                  Configure
                </Link>
              </>
            )}
          </li>
        )
      })}
    </ul>
  )
}
