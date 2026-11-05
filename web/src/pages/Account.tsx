import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { AccountBilling } from '../components/AccountBilling'
import { AccountOrders } from '../components/AccountOrders'
import { AccountServices } from '../components/AccountServices'
import { AccountTabs, type TabDef } from '../components/AccountTabs'
import { AuthForm, type AuthMode } from '../components/AuthForm'
import { useAuth } from '../hooks/useAuth'

type TabId = 'orders' | 'services' | 'billing'

const TABS: TabDef<TabId>[] = [
  { id: 'orders', label: 'Orders' },
  { id: 'services', label: 'Services' },
  { id: 'billing', label: 'Billing' },
]

const MODES: { id: AuthMode; label: string }[] = [
  { id: 'signIn', label: 'Sign in' },
  { id: 'register', label: 'Create account' },
]

const isTab = (value: string | null): value is TabId => TABS.some((t) => t.id === value)

// Anonymous visitors get the same sign-in form as checkout here; after signing in the page shows the account.
function SignInGate() {
  const [mode, setMode] = useState<AuthMode>('signIn')
  return (
    <div className="wrap cart">
      <p className="kicker">My account</p>
      <h1 className="cart__title">Sign in to see your account</h1>
      <section className="checkout account__gate" aria-label="Sign in">
        <div className="seg" role="group" aria-label="Account">
          {MODES.map((m) => (
            <button key={m.id} type="button" aria-pressed={mode === m.id} onClick={() => setMode(m.id)}>
              {m.label}
            </button>
          ))}
        </div>
        <AuthForm key={mode} mode={mode} />
      </section>
    </div>
  )
}

export function Account() {
  const { profile, token, loading } = useAuth()
  const [params, setParams] = useSearchParams()
  const tabParam = params.get('tab')
  const tab: TabId = isTab(tabParam) ? tabParam : 'orders'

  if (loading) {
    return (
      <div className="wrap" aria-busy="true">
        <div className="skeleton__media skeleton__media--tall" />
      </div>
    )
  }
  if (!token || !profile) return <SignInGate />

  return (
    <div className="wrap cart account">
      <p className="kicker">My account</p>
      <h1 className="cart__title">{profile.name}</h1>
      <AccountTabs
        tabs={TABS}
        active={tab}
        label="Account sections"
        onChange={(id) => setParams({ tab: id }, { replace: true, preventScrollReset: true })}
      />
      <section id={`panel-${tab}`} role="tabpanel" aria-labelledby={`tab-${tab}`} tabIndex={0} className="account__panel">
        {tab === 'orders' && <AccountOrders />}
        {tab === 'services' && <AccountServices />}
        {tab === 'billing' && <AccountBilling />}
      </section>
    </div>
  )
}
