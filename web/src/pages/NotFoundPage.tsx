import { Link } from 'react-router-dom'
import { StateCard } from '../components/StateViews'

export function NotFoundPage() {
  return (
    <div className="wrap">
      <StateCard
        emoji="🛸"
        title="Lost in space"
        action={
          <Link to="/" className="btn">
            Back to offers
          </Link>
        }
      >
        This page does not exist.
      </StateCard>
    </div>
  )
}
