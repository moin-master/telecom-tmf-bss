import { componentEmoji, roleLabel } from '../lib/configure'
import { phoneNumber } from '../lib/format'
import { serviceStateLabel } from '../lib/fulfilment'
import { serviceNumber, type ServiceTreeData } from '../lib/serviceTree'

// One part of a service tree: the tile, then its own parts when it has any.
export function ServiceNode({ node }: { node: ServiceTreeData }) {
  const { service } = node
  const role = service.serviceType ?? 'service'
  const msisdn = serviceNumber(service)
  const number = msisdn ? phoneNumber(msisdn) : service.supportingResource[0]?.name
  return (
    <li className="tree__kid">
      <div className="node node--static">
        <span className="node__icon" aria-hidden="true">
          {componentEmoji(role, service.name)}
        </span>
        <span className="node__role">{roleLabel(role)}</span>
        <span className="node__name">{service.name}</span>
        {number && (
          <span className="node__desc">
            <span className="sr-only">Number </span>
            {number}
          </span>
        )}
        <span className="state-pill">{serviceStateLabel(service.state)}</span>
      </div>
      {node.children.length > 0 && (
        <ul className="tree__kids tree__kids--nested" aria-label={`Parts of ${service.name}`}>
          {node.children.map((c) => (
            <ServiceNode key={c.service.id} node={c} />
          ))}
        </ul>
      )}
    </li>
  )
}
