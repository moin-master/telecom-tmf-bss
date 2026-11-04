import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { createContext, useContext, useState, type ReactNode } from 'react'
import { cartApi } from '../api/client'
import {
  AddCartItemDocument,
  CartDocument,
  CreateCartDocument,
  RemoveCartItemDocument,
  type CartFieldsFragment,
} from '../api/generated/shopping-cart/graphql'
import { apiError } from '../lib/errors'

const STORAGE_KEY = 'bss.cartId'

// localStorage can throw (private windows, blocked storage), so the cart then lives for the page only.
const readId = () => {
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}
const writeId = (id: string | null) => {
  try {
    if (id) localStorage.setItem(STORAGE_KEY, id)
    else localStorage.removeItem(STORAGE_KEY)
  } catch {
    /* ignore */
  }
}

type CartContextValue = {
  cart: CartFieldsFragment | undefined
  count: number
  loading: boolean
  add: (offering: { id: string; name: string }, quantity?: number) => Promise<void>
  remove: (itemId: string) => Promise<void>
  busy: boolean
  lastAdded: { name: string; n: number } | null
}

const CartContext = createContext<CartContextValue | null>(null)

const isCartMissing = (error: unknown) => {
  const e = apiError(error)
  return e.code === 'NotFound' && e.message.startsWith('ShoppingCart')
}

export function CartProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient()
  const [cartId, setCartId] = useState<string | null>(readId)
  const [lastAdded, setLastAdded] = useState<CartContextValue['lastAdded']>(null)

  const query = useQuery({
    queryKey: ['cart', cartId],
    enabled: !!cartId,
    retry: false,
    queryFn: async () => {
      try {
        return (await cartApi.request(CartDocument, { id: cartId! })).shoppingCart
      } catch (error) {
        // A cart that no longer exists (for example after it expired) is forgotten.
        if (isCartMissing(error)) {
          writeId(null)
          setCartId(null)
        }
        throw error
      }
    },
  })

  const startCart = async () => {
    const created = await cartApi.request(CreateCartDocument)
    const id = created.createShoppingCart.id
    writeId(id)
    setCartId(id)
    return id
  }

  const addMutation = useMutation({
    mutationFn: async ({ offering, quantity }: { offering: { id: string; name: string }; quantity: number }) => {
      const run = (id: string) =>
        cartApi.request(AddCartItemDocument, { cartId: id, productOfferingId: offering.id, quantity })
      // The cart is created on the first add, not on page load.
      let id = cartId ?? (await startCart())
      try {
        return { id, cart: (await run(id)).addCartItem }
      } catch (error) {
        if (!isCartMissing(error)) throw error
        id = await startCart()
        return { id, cart: (await run(id)).addCartItem }
      }
    },
    onSuccess: ({ id, cart }, { offering }) => {
      queryClient.setQueryData(['cart', id], cart)
      // The "added" message shows for a moment, then clears itself.
      const n = Date.now()
      setLastAdded({ name: offering.name, n })
      window.setTimeout(() => setLastAdded((current) => (current?.n === n ? null : current)), 2600)
    },
  })

  const removeMutation = useMutation({
    mutationFn: (itemId: string) =>
      cartApi.request(RemoveCartItemDocument, { cartId: cartId!, cartItemId: itemId }),
    onSuccess: (data) => queryClient.setQueryData(['cart', cartId], data.removeCartItem),
  })

  const cart = query.data
  const value: CartContextValue = {
    cart,
    count: cart?.cartItem.reduce((sum, item) => sum + item.quantity, 0) ?? 0,
    loading: !!cartId && query.isLoading,
    add: async (offering, quantity = 1) => {
      await addMutation.mutateAsync({ offering, quantity })
    },
    remove: async (itemId) => {
      await removeMutation.mutateAsync(itemId)
    },
    busy: addMutation.isPending || removeMutation.isPending,
    lastAdded,
  }

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

export function useCart(): CartContextValue {
  const value = useContext(CartContext)
  if (!value) throw new Error('useCart must be used inside CartProvider')
  return value
}
