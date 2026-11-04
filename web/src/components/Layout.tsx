import { Outlet, ScrollRestoration } from 'react-router-dom'
import { Footer } from './Footer'
import { Header } from './Header'
import { Toast } from './Toast'

export function Layout() {
  return (
    <>
      <a className="skip-link" href="#main">
        skip to content
      </a>
      <Header />
      <main id="main">
        <Outlet />
      </main>
      <Footer />
      <Toast />
      <ScrollRestoration />
    </>
  )
}
