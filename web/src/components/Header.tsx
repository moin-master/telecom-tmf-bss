import { Link, NavLink } from 'react-router-dom'
import { useCart } from '../hooks/useCart'
import { ThemeToggle } from './ThemeToggle'

export function Header() {
  const { count } = useCart()
  return (
    <header className="site-header">
      <div className="wrap site-header__bar">
        <Link to="/" className="brand" aria-label="Lemon Mobile, home">
          <span className="brand__mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="18" height="18">
              <path d="M8 4v16h9" fill="none" stroke="currentColor" strokeWidth="3.2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </span>
          <span className="brand__word">Lemon</span>
          <span className="brand__sub">Mobile</span>
        </Link>
        <nav aria-label="Main" className="nav">
          <NavLink to="/" end>
            Offers
          </NavLink>
          <ThemeToggle />
          <NavLink to="/cart" className="cart-pill">
            Cart
            <b key={count} className="cart-pill__count" aria-label={`${count} items`}>
              {count}
            </b>
          </NavLink>
        </nav>
      </div>
    </header>
  )
}
