import { contractOf, type ServiceTreeData, type TermOrder } from '../lib/serviceTree'
import { ServiceTree } from './ServiceTree'

type Props = { trees: ServiceTreeData[]; orders: TermOrder[]; label: string }

// One tree per root service. The orders only supply the contract term of each root.
export function ServiceTreeList({ trees, orders, label }: Props) {
  return (
    <ul className="trees" aria-label={label}>
      {trees.map((t) => (
        <li key={t.service.id}>
          <ServiceTree tree={t} contract={contractOf(t.service, orders)} />
        </li>
      ))}
    </ul>
  )
}
