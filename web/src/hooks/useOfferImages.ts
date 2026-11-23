import { useQuery } from '@tanstack/react-query'
import { catalogApi } from '../api/client'
import { OfferImagesDocument } from '../api/generated/product-catalog/graphql'

// Picture url by offering id, from the catalog's attachment[] (attachmentType "image").
// Offerings without a picture are not in the map; callers fall back to the emoji tile.
export function useOfferImages() {
  return useQuery({
    queryKey: ['offer-images'],
    staleTime: 5 * 60_000,
    queryFn: () => catalogApi.request(OfferImagesDocument),
    select: (data) => {
      const images = new Map<string, string>()
      for (const offer of data.productOfferingList) {
        const image = offer.attachment.find((a) => a.attachmentType === 'image')
        if (image) images.set(offer.id, image.url)
      }
      return images
    },
  })
}
