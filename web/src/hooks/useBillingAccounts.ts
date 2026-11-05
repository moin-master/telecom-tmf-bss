import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { accountApi } from '../api/client'
import {
  BillingAccountDocument,
  BillingAccountsDocument,
  CreateBillingAccountDocument,
  type ContactInput,
} from '../api/generated/account/graphql'
import { useAuth } from './useAuth'

const bearer = (token: string | null) => (token ? { Authorization: `Bearer ${token}` } : undefined)

// The signed-in customer's billing accounts, newest first.
export function useBillingAccounts() {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['billing-accounts', token],
    enabled: !!token,
    retry: false,
    queryFn: () => accountApi.request(BillingAccountsDocument, undefined, bearer(token)).then((r) => r.billingAccountList),
  })
}

export function useBillingAccount(id: string | undefined) {
  const { token } = useAuth()
  return useQuery({
    queryKey: ['billing-account', id, token],
    enabled: !!id && !!token,
    retry: false,
    queryFn: () => accountApi.request(BillingAccountDocument, { id: id! }, bearer(token)).then((r) => r.billingAccount),
  })
}

export function useCreateBillingAccount() {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (v: { name: string; contact: ContactInput[] }) =>
      accountApi.request(CreateBillingAccountDocument, v, bearer(token)).then((r) => r.createBillingAccount),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['billing-accounts'] }),
  })
}
