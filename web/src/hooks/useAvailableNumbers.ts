import { useQuery } from '@tanstack/react-query'
import { resourceApi } from '../api/client'
import { AvailableNumbersDocument } from '../api/generated/resource/graphql'

// Numbers nobody has reserved or taken, optionally containing the digits typed by the shopper.
export function useAvailableNumbers(search: string) {
  return useQuery({
    queryKey: ['numbers', search],
    queryFn: () =>
      resourceApi
        .request(AvailableNumbersDocument, {
          filter: { allocationStatus: 'available', usageState: 'idle', search: search || null },
        })
        .then((r) => r.resourceList),
    retry: false,
  })
}
