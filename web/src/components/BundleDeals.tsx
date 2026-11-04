import { useEffect, useId, useState } from 'react'
import { useOffer } from '../hooks/useOffers'
import { OPTIONS, type PurchaseOption } from '../lib/purchase'

type Link = { id: string; name: string; relationshipType: string }

type Props = {
  links: Link[]
  option: PurchaseOption
  // Reports the contract and launch offer that will be sent to the cart.
  onChange: (deal: { contractMonths?: number; launchOffer?: string }) => void
}

const ofType = (links: Link[], type: string) => links.filter((l) => l.relationshipType === type)
const sentence = (text: string) => text.charAt(0).toUpperCase() + text.slice(1)
const optionName = (key: string) => OPTIONS.find((o) => o.key === key)?.label ?? key

// A rule with nothing to choose: the cart applies it by itself, so it is only explained here.
function DealNote({ id }: { id: string }) {
  const offer = useOffer(id)
  if (!offer.data) return null
  return (
    <li>
      <b>{offer.data.name}</b> {offer.data.description}
    </li>
  )
}

export function BundleDeals({ links, option, onChange }: Props) {
  const name = useId()
  const launch = ofType(links, 'launchOffer')
  const contractLink = ofType(links, 'contract')[0]
  const waiver = ofType(links, 'activationWaiver')[0]
  const double = ofType(links, 'multiBundleDiscount')[0]

  const contractOffer = useOffer(contractLink?.id ?? '')
  const term = contractOffer.data?.productOfferingTerm[0]
  const allowed = !!term && (term.availableWith.length === 0 || term.availableWith.includes(option))

  const [chosen, setChosen] = useState<string | null>(null)
  const [contract, setContract] = useState(false)
  const launchOffer = chosen ?? launch[0]?.id
  const contractMonths = contract && allowed ? term?.duration.amount : undefined

  useEffect(() => {
    onChange({ contractMonths, launchOffer })
  }, [contractMonths, launchOffer]) // eslint-disable-line react-hooks/exhaustive-deps

  if (launch.length === 0 && !contractLink && !double) return null

  return (
    <section className="deals" aria-label="Deals">
      <h2 className="detail__h">Deals</h2>

      {launch.length > 0 && (
        <fieldset className="options options--stack">
          <legend className="options__legend">First 6 months, pick one</legend>
          <div className="options__row">
            {launch.map((l) => (
              <label key={l.id} className="option">
                <input
                  type="radio"
                  name={name}
                  value={l.id}
                  checked={launchOffer === l.id}
                  onChange={() => setChosen(l.id)}
                />
                <span className="option__label">{sentence(l.name.replace(/^Launch offer: /, ''))}</span>
              </label>
            ))}
          </div>
        </fieldset>
      )}

      {contractLink && term && (
        <div className={`addon${allowed ? '' : ' is-disabled'}`}>
          <input
            id={`${name}-contract`}
            type="checkbox"
            checked={contract && allowed}
            disabled={!allowed}
            onChange={(e) => setContract(e.target.checked)}
          />
          <label htmlFor={`${name}-contract`} className="addon__box">
            <span className="addon__title">
              Add the {term.name} <b>{term.duration.amount} months</b>
            </span>
            <span className="addon__hint">
              {allowed
                ? waiver
                  ? `${waiver.name}: no activation fee with the contract`
                  : 'Locks in your plan for the full term'
                : `Needs ${term.availableWith.map(optionName).join(' or ')}`}
            </span>
          </label>
        </div>
      )}

      {double && (
        <ul className="deals__notes">
          <DealNote id={double.id} />
        </ul>
      )}
    </section>
  )
}
