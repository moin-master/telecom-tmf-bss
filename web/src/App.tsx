import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Layout } from './components/Layout'
import { Account } from './pages/Account'
import { Cart } from './pages/Cart'
import { Checkout } from './pages/Checkout'
import { Configure } from './pages/Configure'
import { Home } from './pages/Home'
import { NotFoundPage } from './pages/NotFoundPage'
import { OrderConfirmation } from './pages/OrderConfirmation'
import { OfferDetail } from './pages/OfferDetail'

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: '/', element: <Home /> },
      { path: '/offers/:id', element: <OfferDetail /> },
      { path: '/account', element: <Account /> },
      { path: '/cart', element: <Cart /> },
      { path: '/checkout', element: <Checkout /> },
      { path: '/orders/:id', element: <OrderConfirmation /> },
      { path: '/cart/items/:itemId/configure', element: <Configure /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
