import { Link, NavLink } from 'react-router-dom'
import { useCart } from '../hooks/useCart'
import { ThemeToggle } from './ThemeToggle'

export function Header() {
  const { count } = useCart()
  return (
    <header className="site-header">
      <div className="wrap site-header__bar">
        <Link to="/" className="brand" aria-label="My Own Mobile, home">
          <span className="brand__word" aria-hidden="true">
            MOM
          </span>
          <span className="brand__sub" aria-hidden="true">
            My Own Mobile
          </span>
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
