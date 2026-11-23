import type { ServiceOrder } from '../lib/fulfilment'
import { orderSteps, stepStatus } from '../lib/orderCard'

// Three steps as a list with text for each state, so colour is never the only signal.
export function OrderStatusSteps({ fulfilment }: { fulfilment?: ServiceOrder }) {
  const steps = orderSteps(fulfilment)
  const error = fulfilment?.state === 'failed' ? fulfilment.errorMessage : null
  return (
    <div className="steps">
      <ol className="steps__list" aria-label="Order progress">
        {steps.map((s) => (
          <li key={s.label} className={`steps__step is-${s.state}`} aria-current={s.state === 'current' ? 'step' : undefined}>
            <span className="steps__dot" aria-hidden="true">
              {s.state === 'done' ? '✓' : s.state === 'failed' ? '!' : ''}
            </span>
            <span className="steps__label">{s.label}</span>
            <span className="sr-only">, {stepStatus(s.state)}</span>
          </li>
        ))}
      </ol>
      {error && (
        <p className="steps__error" role="status">
          Fulfilment failed: {error}
        </p>
      )}
    </div>
  )
}
