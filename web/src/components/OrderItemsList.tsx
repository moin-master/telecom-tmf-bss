import type { Order } from '../lib/orderCard'

// One line per order item: offering name, quantity, and a chip when the item has a contract term.
export function OrderItemsList({ items }: { items: Order['productOrderItem'] }) {
  return (
    <ul className="order-items" aria-label="Items">
      {items.map((item) => (
        <li key={item.id} className="order-items__line">
          <span>
            {item.productOffering.name} <span className="order-items__qty">× {item.quantity}</span>
          </span>
          {item.itemTerm.map((t) => (
            <span key={t.name} className="chip">
              Contract · {t.duration.amount} months
            </span>
          ))}
        </li>
      ))}
    </ul>
  )
}
