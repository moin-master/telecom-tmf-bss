import { useCallback, useEffect, useState } from 'react'

export type Theme = 'light' | 'dark'

const STORAGE_KEY = 'bss.theme'
const BROWSER_COLOR: Record<Theme, string> = { light: '#ffffff', dark: '#141414' }

// localStorage can throw (private windows, blocked storage); the choice then lasts for the page only.
const savedTheme = (): Theme | null => {
  try {
    const value = localStorage.getItem(STORAGE_KEY)
    return value === 'light' || value === 'dark' ? value : null
  } catch {
    return null
  }
}

const applyTheme = (theme: Theme) => {
  document.documentElement.dataset.theme = theme
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', BROWSER_COLOR[theme])
}

// The first value was set before paint by the script in index.html.
export function useTheme() {
  const [theme, setTheme] = useState<Theme>(() => (document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light'))

  // Follow the system setting until the visitor picks a theme.
  useEffect(() => {
    const query = window.matchMedia('(prefers-color-scheme: dark)')
    const onChange = () => {
      if (savedTheme()) return
      const next: Theme = query.matches ? 'dark' : 'light'
      applyTheme(next)
      setTheme(next)
    }
    query.addEventListener('change', onChange)
    return () => query.removeEventListener('change', onChange)
  }, [])

  const toggle = useCallback(() => {
    const next: Theme = theme === 'dark' ? 'light' : 'dark'
    applyTheme(next)
    try {
      localStorage.setItem(STORAGE_KEY, next)
    } catch {
      /* ignore */
    }
    setTheme(next)
  }, [theme])

  return { theme, toggle }
}
