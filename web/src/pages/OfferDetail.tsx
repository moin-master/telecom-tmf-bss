import { Link, useParams } from 'react-router-dom'
import { OfferInfo } from '../components/OfferInfo'
import { PricePanel } from '../components/PricePanel'
import { ErrorState, StateCard } from '../components/StateViews'
import { useOffer } from '../hooks/useOffers'
import { apiError } from '../lib/errors'
import { offerTheme } from '../lib/theme'

export function OfferDetail() {
  const { id = '' } = useParams()
  const offer = useOffer(id)

  if (offer.isPending) {
    return (
      <div className="wrap detail" aria-busy="true">
        <div className="skeleton__media skeleton__media--tall" />
      </div>
    )
  }

  if (offer.isError) {
    const gone = apiError(offer.error).code === 'NotFound'
    return (
      <div className="wrap">
        {gone ? (
          <StateCard
            emoji="🕳️"
            title="This offer is gone"
            action={
              <Link to="/" className="btn">
                Back to offers
              </Link>
            }
          >
            That offer is not available right now.
          </StateCard>
        ) : (
          <ErrorState error={offer.error} onRetry={() => offer.refetch()} />
        )}
      </div>
    )
  }

  const data = offer.data
  const theme = offerTheme(data.category)

  return (
    <div className="wrap detail" data-theme={theme.key}>
      <nav className="crumbs" aria-label="Breadcrumb">
        <Link to="/">Offers</Link> <span aria-hidden="true">/</span> <span>{theme.label}</span>
      </nav>

      <div className="detail__grid">
        <OfferInfo offer={data} />
        {/* Keyed by offer so choices never carry over from another offer. */}
        <PricePanel key={data.id} offer={data} />
      </div>
    </div>
  )
}
