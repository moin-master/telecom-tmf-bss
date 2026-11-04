import { useInfiniteQuery, useQuery } from '@tanstack/react-query'
import { catalogApi } from '../api/client'
import { CategoriesDocument, OfferDocument, OffersDocument } from '../api/generated/product-catalog/graphql'

export const PAGE_SIZE = 8

export type OfferFilter = { name?: string; categoryId?: string }

export function useOffers(filter: OfferFilter) {
  return useInfiniteQuery({
    queryKey: ['offers', filter],
    initialPageParam: 0,
    queryFn: ({ pageParam }) =>
      catalogApi.request(OffersDocument, {
        offset: pageParam,
        limit: PAGE_SIZE,
        // Promotions are applied by the cart; they are not shown as products.
        filter: { name: filter.name || null, categoryId: filter.categoryId || null, isSellable: true },
      }),
    getNextPageParam: (last, all) =>
      last.productOfferingList.length < PAGE_SIZE ? undefined : all.length * PAGE_SIZE,
    select: (data) => data.pages.flatMap((page) => page.productOfferingList),
  })
}

export function useOffer(id: string) {
  return useQuery({
    queryKey: ['offer', id],
    queryFn: () => catalogApi.request(OfferDocument, { id }).then((r) => r.productOffering),
    enabled: !!id,
    retry: false,
  })
}

export function useCategories() {
  return useQuery({
    queryKey: ['categories'],
    queryFn: () => catalogApi.request(CategoriesDocument).then((r) => r.categoryList),
  })
}
