import { componentEmoji, roleLabel } from '../lib/configure'
import { phoneNumber, shortDate } from '../lib/format'
import { serviceStateLabel } from '../lib/fulfilment'
import { serviceNumber, type Contract, type ServiceTreeData } from '../lib/serviceTree'
import { ServiceContract } from './ServiceContract'
import { ServiceNode } from './ServiceNode'

type Props = { tree: ServiceTreeData; contract: Contract | null }

// A service as a tree, drawn like the bundle tree in the cart: the root with its kind, a stem and the
// parts joined to it. A single service is a tree of one. serviceRelationship is not drawn.
export function ServiceTree({ tree, contract }: Props) {
  const { service, children } = tree
  const role = service.serviceType ?? 'service'
  const kind = service.isBundle ? 'Bundle' : roleLabel(role)
  const msisdn = serviceNumber(service)
  const number = msisdn ? phoneNumber(msisdn) : service.isBundle ? undefined : service.supportingResource[0]?.name
  const started = shortDate(service.startDate)

  return (
    <section className="tree tree--service" aria-label={`${service.name} structure`}>
      <div className="tree__root">
        {!service.isBundle && (
          <span className="tree__rooticon" aria-hidden="true">
            {componentEmoji(role, service.name)}
          </span>
        )}
        <span className="tree__rootname">{service.name}</span>
        <span className="tree__rootkind">{kind}</span>
        {number && (
          <span className="tree__rootnum">
            <span className="sr-only">Number </span>
            {number}
          </span>
        )}
        <span className="tree__rootstate">{serviceStateLabel(service.state)}</span>
      </div>
      <p className="tree__meta">
        Service {service.id}
        {started && !contract && <> · Started {started}</>}
      </p>

      {children.length > 0 && (
        <>
          <div className="tree__stem" aria-hidden="true" />
          <ul className="tree__kids" style={{ '--n': children.length } as React.CSSProperties} aria-label={`Parts of ${service.name}`}>
            {children.map((c) => (
              <ServiceNode key={c.service.id} node={c} />
            ))}
          </ul>
        </>
      )}

      {contract && (
        <div className="tree__contract">
          <ServiceContract contract={contract} />
        </div>
      )}
    </section>
  )
}
