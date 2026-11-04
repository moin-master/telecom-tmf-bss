import { useCart } from '../hooks/useCart'

// Announces additions to screen readers and shows a short confirmation until the cart clears the message.
export function Toast() {
  const { lastAdded } = useCart()

  return (
    <div className="toast-region" aria-live="polite">
      {lastAdded && (
        <p className="toast" key={lastAdded.n}>
          <span className="toast__check" aria-hidden="true">
            ✓
          </span>
          Added to cart · <b>{lastAdded.name}</b>
        </p>
      )}
    </div>
  )
}
