import { useQuery } from '@tanstack/react-query'
import { serviceRegistryApi } from '../api/client'
import { ServicesDocument } from '../api/generated/service-registry/graphql'
import { useAuth } from './useAuth'

const bearer = (token: string | null) => (token ? { Authorization: `Bearer ${token}` } : undefined)

// The signed-in customer's services (the backend returns only their own).
export function useMyServices() {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['services', token],
    enabled: !!token,
    retry: false,
    queryFn: () => serviceRegistryApi.request(ServicesDocument, undefined, bearer(token)).then((r) => r.serviceList),
  })
}
