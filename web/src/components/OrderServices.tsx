import { useId, useState, type ReactNode } from 'react'
import { type ServiceTreeData, type TermOrder } from '../lib/serviceTree'
import { ServiceTreeList } from './ServiceTreeList'

type Props = { orderId: string; trees: ServiceTreeData[]; orders: TermOrder[]; children?: ReactNode }

// The services of one order, behind a disclosure button (native button: Enter and Space toggle it).
// Children (for example a "View order" link) sit on the same bar as the button.
export function OrderServices({ orderId, trees, orders, children }: Props) {
  const [open, setOpen] = useState(false)
  const panelId = useId()

  if (trees.length === 0) {
    return (
      <div className="order-services">
        <div className="order-services__bar">
          <p className="row__none">No services yet</p>
          {children}
        </div>
      </div>
    )
  }

  return (
    <div className="order-services">
      <div className="order-services__bar">
        <button type="button" className="order-services__toggle" aria-expanded={open} aria-controls={panelId} onClick={() => setOpen(!open)}>
          {open ? 'Hide' : 'Show'} services ({trees.length})
        </button>
        {children}
      </div>
      <div id={panelId} hidden={!open}>
        {open && <ServiceTreeList trees={trees} orders={orders} label={`Services of order ${orderId}`} />}
      </div>
    </div>
  )
}
