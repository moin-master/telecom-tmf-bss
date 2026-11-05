import { GraphQLClient } from 'graphql-request'

// Relative paths: the Vite dev server proxies them to the backend (no CORS needed).
const base = '/telecom-tmf-bss'

const client = (path: string) =>
  new GraphQLClient(new URL(`${base}/${path}/graphql`, window.location.origin).toString())

export const catalogApi = client('product-catalog')
export const accountApi = client('account')
export const cartApi = client('shopping-cart')
export const identityApi = client('identity')
export const orderApi = client('order')
export const resourceApi = client('resource')
