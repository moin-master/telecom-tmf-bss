import { useRef, type KeyboardEvent } from 'react'

export type TabDef<T extends string> = { id: T; label: string }

type Props<T extends string> = {
  tabs: TabDef<T>[]
  active: T
  onChange: (id: T) => void
  label: string
}

// Accessible tabs: arrow keys, Home and End move between tabs; only the active tab is in the tab order.
export function AccountTabs<T extends string>({ tabs, active, onChange, label }: Props<T>) {
  const refs = useRef<Record<string, HTMLButtonElement | null>>({})

  function onKeyDown(event: KeyboardEvent, index: number) {
    const last = tabs.length - 1
    const next =
      event.key === 'ArrowRight' ? (index === last ? 0 : index + 1)
      : event.key === 'ArrowLeft' ? (index === 0 ? last : index - 1)
      : event.key === 'Home' ? 0
      : event.key === 'End' ? last
      : null
    if (next === null) return
    event.preventDefault()
    const tab = tabs[next]
    onChange(tab.id)
    refs.current[tab.id]?.focus()
  }

  return (
    <div className="tabs" role="tablist" aria-label={label}>
      {tabs.map((tab, i) => (
        <button
          key={tab.id}
          ref={(el) => {
            refs.current[tab.id] = el
          }}
          type="button"
          role="tab"
          id={`tab-${tab.id}`}
          aria-selected={active === tab.id}
          aria-controls={`panel-${tab.id}`}
          tabIndex={active === tab.id ? 0 : -1}
          className="tabs__tab"
          onClick={() => onChange(tab.id)}
          onKeyDown={(e) => onKeyDown(e, i)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  )
}
