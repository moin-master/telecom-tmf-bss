import { useEffect, useState } from 'react'
import { useCart } from '../hooks/useCart'
import { useOffer } from '../hooks/useOffers'
import { useQuote } from '../hooks/useQuote'
import { optionLabel, optionsOf, type CartChoice, type PurchaseOption } from '../lib/purchase'
import { AddToCartButton } from './AddToCartButton'
import { BillPreview } from './BillPreview'
import { ContractStatus } from './ContractStatus'
import { DealNote } from './DealNote'
import { LaunchOffers } from './LaunchOffers'
import { ModeSwitch, type Mode } from './ModeSwitch'
import type { OfferData } from './OfferInfo'
import { ProtectionAddOn } from './ProtectionAddOn'
import { PurchaseOptions } from './PurchaseOptions'

const MAX_QUANTITY = 99

// The right panel: everything that changes the price or the bill. The bill itself is priced by the backend.
export function PricePanel({ offer }: { offer: OfferData }) {
  const { cart, add, update, remove } = useCart()

  const available = optionsOf(offer.productOfferingPrice)
  const hasOptions = available.length > 0
  const links = offer.productOfferingRelationship
  const launchOffers = links.filter((l) => l.relationshipType === 'launchOffer')
  const contractLink = links.find((l) => l.relationshipType === 'contract')
  const waiverLink = links.find((l) => l.relationshipType === 'activationWaiver')
  const doubleLink = links.find((l) => l.relationshipType === 'multiBundleDiscount')
  const addOn = links.find((l) => l.relationshipType === 'addOn')
  const term = useOffer(contractLink?.id ?? '').data?.productOfferingTerm[0]

  // Lines of this offer already in the cart, and protection plan lines that go with it.
  const inCart = cart?.cartItem.filter((i) => i.productOffering.id === offer.id) ?? []
  const planLines = addOn ? (cart?.cartItem.filter((i) => i.productOffering.id === addOn.id) ?? []) : []

  const [picked, setPicked] = useState<Mode | null>(null)
  const [editId, setEditId] = useState<string | null>(null)
  const mode: Mode = inCart.length === 0 ? 'build' : (picked ?? 'update')
  const editing = inCart.find((i) => i.id === editId) ?? inCart[0]

  const [option, setOption] = useState<PurchaseOption>('own')
  const [launchPick, setLaunchPick] = useState<string | undefined>()
  const [quantity, setQuantity] = useState(1)
  const [withAddOn, setWithAddOn] = useState(false)

  // Updating starts from what the line already has; building starts clean.
  useEffect(() => {
    if (mode === 'update' && editing) {
      setOption((editing.purchaseOption as PurchaseOption | null) ?? 'own')
      setLaunchPick(editing.launchOffer?.id)
      setQuantity(editing.quantity)
      setWithAddOn(planLines.length > 0)
    } else {
      setOption('own')
      setLaunchPick(undefined)
      setQuantity(1)
      setWithAddOn(false)
    }
  }, [mode, editing?.id]) // eslint-disable-line react-hooks/exhaustive-deps

  // The contract follows the purchase option; the activation fee waiver follows the contract (in the backend).
  const contractAllowed = !!term && hasOptions && (term.availableWith.length === 0 || term.availableWith.includes(option))
  const launchOffer = launchPick ?? launchOffers[0]?.id
  const choice: CartChoice = {
    option: hasOptions ? option : undefined,
    contractMonths: contractAllowed ? term?.duration.amount : undefined,
    launchOffer: launchOffers.length > 0 ? launchOffer : undefined,
  }
  const quote = useQuote(offer.id, quantity, choice, offer.isSellable)

  const changed =
    !editing ||
    (editing.purchaseOption ?? null) !== (choice.option ?? null) ||
    (editing.contractMonths ?? null) !== (choice.contractMonths ?? null) ||
    (editing.launchOffer?.id ?? null) !== (choice.launchOffer ?? null) ||
    editing.quantity !== quantity ||
    withAddOn !== planLines.length > 0

  async function saveUpdate() {
    if (!editing) return
    await update(editing.id, quantity, choice)
    if (!addOn) return
    if (withAddOn && planLines.length === 0) await add(addOn, quantity)
    if (!withAddOn) for (const line of planLines) await remove(line.id)
  }

  return (
    <aside className="panel" aria-label="Price and bill">
      <h2 className="panel__title">Price and bill</h2>

      {inCart.length > 0 && (
        <div className="panel__section">
          <ModeSwitch value={mode} onChange={setPicked} />
          {mode === 'update' && inCart.length > 1 && (
            <label className="panel__select">
              Which one?
              <select value={editing?.id} onChange={(e) => setEditId(e.target.value)}>
                {inCart.map((i) => (
                  <option key={i.id} value={i.id}>
                    {optionLabel(i.purchaseOption) ?? 'Standard'}
                    {i.contractMonths ? ` · ${i.contractMonths / 12}-year contract` : ''} · qty {i.quantity}
                  </option>
                ))}
              </select>
            </label>
          )}
        </div>
      )}

      {hasOptions && (
        <div className="panel__section">
          <PurchaseOptions available={available} value={option} onChange={setOption} />
        </div>
      )}

      <div className="panel__section">
        <h3 className="panel__h">Your bill</h3>
        <BillPreview quote={quote.data} updating={quote.isFetching} failed={quote.isError} />
      </div>

      {(launchOffers.length > 0 || contractLink || doubleLink) && (
        <div className="panel__section">
          <h3 className="panel__h">Deals</h3>
          {launchOffers.length > 0 && <LaunchOffers offers={launchOffers} value={launchOffer} onChange={setLaunchPick} />}
          {contractLink && term && (
            <ContractStatus
              name={term.name}
              months={term.duration.amount}
              included={contractAllowed}
              includedHint={waiverLink ? `${waiverLink.name}: no activation fee with the contract` : 'Locks in your plan for the full term'}
              excludedHint="Choose Trade-in or Finance to add the contract and waive the activation fee"
            />
          )}
          {doubleLink && <DealNote id={doubleLink.id} />}
        </div>
      )}

      {addOn && (
        <div className="panel__section">
          <ProtectionAddOn offerId={addOn.id} checked={withAddOn} onChange={setWithAddOn} />
        </div>
      )}

      <div className="buy">
        <div className="stepper" role="group" aria-label="Quantity">
          <button type="button" onClick={() => setQuantity((q) => Math.max(1, q - 1))} disabled={quantity <= 1} aria-label="One less">
            −
          </button>
          <output aria-live="polite">{quantity}</output>
          <button type="button" onClick={() => setQuantity((q) => Math.min(MAX_QUANTITY, q + 1))} disabled={quantity >= MAX_QUANTITY} aria-label="One more">
            +
          </button>
        </div>
        {mode === 'update' && editing ? (
          <AddToCartButton
            offering={offer}
            sellable={offer.isSellable}
            run={saveUpdate}
            label={changed ? 'Update offer' : 'No changes to save'}
            doneLabel="Updated ✓"
            disabled={!changed}
          />
        ) : (
          <AddToCartButton
            offering={offer}
            quantity={quantity}
            choice={hasOptions ? choice : undefined}
            extras={addOn && withAddOn ? [addOn] : []}
            sellable={offer.isSellable}
          />
        )}
      </div>
    </aside>
  )
}
