import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Layout } from './components/Layout'
import { Cart } from './pages/Cart'
import { Configure } from './pages/Configure'
import { Home } from './pages/Home'
import { NotFoundPage } from './pages/NotFoundPage'
import { OfferDetail } from './pages/OfferDetail'

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: '/', element: <Home /> },
      { path: '/offers/:id', element: <OfferDetail /> },
      { path: '/cart', element: <Cart /> },
      { path: '/cart/items/:itemId/configure', element: <Configure /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
