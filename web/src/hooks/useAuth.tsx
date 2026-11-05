import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { createContext, useContext, useState, type ReactNode } from 'react'
import { identityApi } from '../api/client'
import {
  MeDocument,
  RegisterDocument,
  SignInDocument,
  SignOutDocument,
  type ProfileFieldsFragment,
} from '../api/generated/identity/graphql'
import { apiError } from '../lib/errors'

const STORAGE_KEY = 'bss.token'

// localStorage can throw (private windows, blocked storage), so the sign-in then lives for the page only.
const readToken = () => {
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}
const writeToken = (token: string | null) => {
  try {
    if (token) localStorage.setItem(STORAGE_KEY, token)
    else localStorage.removeItem(STORAGE_KEY)
  } catch {
    /* ignore */
  }
}

const bearer = (token: string) => ({ Authorization: `Bearer ${token}` })

export type Profile = ProfileFieldsFragment

type NewAccount = { email: string; password: string; givenName: string; familyName: string }

type AuthContextValue = {
  profile: Profile | undefined
  token: string | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  register: (account: NewAccount) => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient()
  const [token, setToken] = useState<string | null>(readToken)

  const forget = () => {
    writeToken(null)
    setToken(null)
    queryClient.removeQueries({ queryKey: ['me'] })
  }

  const me = useQuery({
    queryKey: ['me', token],
    enabled: !!token,
    retry: false,
    queryFn: async () => {
      try {
        return (await identityApi.request(MeDocument, undefined, bearer(token!))).me
      } catch (error) {
        // An expired or unknown token is forgotten.
        if (apiError(error).code === 'Unauthorized') forget()
        throw error
      }
    },
  })

  const start = (session: { token: string; profile: Profile }) => {
    writeToken(session.token)
    setToken(session.token)
    queryClient.setQueryData(['me', session.token], session.profile)
  }

  const signInMutation = useMutation({
    mutationFn: (v: { email: string; password: string }) => identityApi.request(SignInDocument, v),
    onSuccess: (data) => start(data.signIn),
  })
  const registerMutation = useMutation({
    mutationFn: (v: NewAccount) => identityApi.request(RegisterDocument, v),
    onSuccess: (data) => start(data.register),
  })

  const value: AuthContextValue = {
    profile: token ? me.data : undefined,
    token,
    loading: !!token && me.isLoading,
    signIn: async (email, password) => {
      await signInMutation.mutateAsync({ email, password })
    },
    register: async (account) => {
      await registerMutation.mutateAsync(account)
    },
    signOut: async () => {
      const current = token
      forget()
      if (current) await identityApi.request(SignOutDocument, undefined, bearer(current)).catch(() => undefined)
    },
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const value = useContext(AuthContext)
  if (!value) throw new Error('useAuth must be used inside AuthProvider')
  return value
}
