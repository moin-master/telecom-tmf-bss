import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { cartApi } from '../api/client'
import { QuoteCartItemDocument } from '../api/generated/shopping-cart/graphql'
import type { CartChoice } from '../lib/purchase'

// The bill for a choice, priced by the backend the same way the cart will price it. Nothing is saved.
export function useQuote(offeringId: string, quantity: number, choice: CartChoice, enabled: boolean) {
  return useQuery({
    queryKey: ['quote', offeringId, quantity, choice],
    enabled,
    retry: false,
    placeholderData: keepPreviousData,
    queryFn: () =>
      cartApi
        .request(QuoteCartItemDocument, {
          productOfferingId: offeringId,
          quantity,
          purchaseOption: choice.option ?? null,
          contractMonths: choice.contractMonths ?? null,
          launchOffer: choice.launchOffer ?? null,
        })
        .then((r) => r.quoteCartItem),
  })
}
