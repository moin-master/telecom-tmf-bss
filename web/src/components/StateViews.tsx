import type { ReactNode } from 'react'
import { apiError } from '../lib/errors'

export function OfferSkeletons({ count = 8 }: { count?: number }) {
  return (
    <div className="grid" aria-busy="true" aria-label="Loading offers">
      {Array.from({ length: count }, (_, i) => (
        <div key={i} className="skeleton" aria-hidden="true">
          <div className="skeleton__media" />
          <div className="skeleton__line" />
          <div className="skeleton__line skeleton__line--short" />
        </div>
      ))}
    </div>
  )
}

type StateProps = { emoji: string; title: string; children?: ReactNode; action?: ReactNode }

export function StateCard({ emoji, title, children, action }: StateProps) {
  return (
    <div className="state" role="status">
      <span className="state__emoji" aria-hidden="true">
        {emoji}
      </span>
      <h2>{title}</h2>
      {children && <p>{children}</p>}
      {action}
    </div>
  )
}

export function ErrorState({ error, onRetry }: { error: unknown; onRetry?: () => void }) {
  const e = apiError(error)
  const offline = e.code === 'Network'
  return (
    <StateCard
      emoji={offline ? '📡' : '🫠'}
      title={offline ? 'No connection' : 'That did not work'}
      action={
        onRetry && (
          <button type="button" className="btn" onClick={onRetry}>
            Try again
          </button>
        )
      }
    >
      {offline ? 'The server is not answering. Is the backend running?' : e.message}
    </StateCard>
  )
}
