/* eslint-disable */
import * as types from './graphql';
import type { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';

/**
 * Map of all GraphQL operations in the project.
 *
 * This map has several performance disadvantages:
 * 1. It is not tree-shakeable, so it will include all operations in the project.
 * 2. It is not minifiable, so the string of a GraphQL query will be multiple times inside the bundle.
 * 3. It does not support dead code elimination, so it will add unused operations.
 *
 * Therefore it is highly recommended to use the babel or swc plugin for production.
 * Learn more about it here: https://the-guild.dev/graphql/codegen/plugins/presets/preset-client#reducing-bundle-size
 */
type Documents = {
    "fragment CartFields on ShoppingCart {\n  id\n  lastUpdate\n  cartItem {\n    id\n    quantity\n    purchaseOption\n    productOffering {\n      id\n      name\n    }\n    itemPrice {\n      name\n      priceType\n      recurringChargePeriod\n      price {\n        dutyFreeAmount {\n          unit\n          value\n        }\n      }\n    }\n    itemTotalPrice {\n      name\n      priceType\n      recurringChargePeriod\n      price {\n        taxIncludedAmount {\n          unit\n          value\n        }\n      }\n    }\n  }\n  cartTotalPrice {\n    name\n    priceType\n    recurringChargePeriod\n    price {\n      taxIncludedAmount {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Cart($id: String!) {\n  shoppingCart(id: $id) {\n    ...CartFields\n  }\n}\n\nmutation CreateCart {\n  createShoppingCart {\n    ...CartFields\n  }\n}\n\nmutation AddCartItem($cartId: String!, $productOfferingId: String!, $quantity: Int!, $purchaseOption: String) {\n  addCartItem(\n    cartId: $cartId\n    productOfferingId: $productOfferingId\n    quantity: $quantity\n    purchaseOption: $purchaseOption\n  ) {\n    ...CartFields\n  }\n}\n\nmutation RemoveCartItem($cartId: String!, $cartItemId: String!) {\n  removeCartItem(cartId: $cartId, cartItemId: $cartItemId) {\n    ...CartFields\n  }\n}": typeof types.CartFieldsFragmentDoc,
};
const documents: Documents = {
    "fragment CartFields on ShoppingCart {\n  id\n  lastUpdate\n  cartItem {\n    id\n    quantity\n    purchaseOption\n    productOffering {\n      id\n      name\n    }\n    itemPrice {\n      name\n      priceType\n      recurringChargePeriod\n      price {\n        dutyFreeAmount {\n          unit\n          value\n        }\n      }\n    }\n    itemTotalPrice {\n      name\n      priceType\n      recurringChargePeriod\n      price {\n        taxIncludedAmount {\n          unit\n          value\n        }\n      }\n    }\n  }\n  cartTotalPrice {\n    name\n    priceType\n    recurringChargePeriod\n    price {\n      taxIncludedAmount {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Cart($id: String!) {\n  shoppingCart(id: $id) {\n    ...CartFields\n  }\n}\n\nmutation CreateCart {\n  createShoppingCart {\n    ...CartFields\n  }\n}\n\nmutation AddCartItem($cartId: String!, $productOfferingId: String!, $quantity: Int!, $purchaseOption: String) {\n  addCartItem(\n    cartId: $cartId\n    productOfferingId: $productOfferingId\n    quantity: $quantity\n    purchaseOption: $purchaseOption\n  ) {\n    ...CartFields\n  }\n}\n\nmutation RemoveCartItem($cartId: String!, $cartItemId: String!) {\n  removeCartItem(cartId: $cartId, cartItemId: $cartItemId) {\n    ...CartFields\n  }\n}": types.CartFieldsFragmentDoc,
};

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 *
 *
 * @example
 * ```ts
 * const query = graphql(`query GetUser($id: ID!) { user(id: $id) { name } }`);
 * ```
 *
 * The query argument is unknown!
 * Please regenerate the types.
 */
export function graphql(source: string): unknown;

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "fragment CartFields on ShoppingCart {\n  id\n  lastUpdate\n  cartItem {\n    id\n    quantity\n    purchaseOption\n    productOffering {\n      id\n      name\n    }\n    itemPrice {\n      name\n      priceType\n      recurringChargePeriod\n      price {\n        dutyFreeAmount {\n          unit\n          value\n        }\n      }\n    }\n    itemTotalPrice {\n      name\n      priceType\n      recurringChargePeriod\n      price {\n        taxIncludedAmount {\n          unit\n          value\n        }\n      }\n    }\n  }\n  cartTotalPrice {\n    name\n    priceType\n    recurringChargePeriod\n    price {\n      taxIncludedAmount {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Cart($id: String!) {\n  shoppingCart(id: $id) {\n    ...CartFields\n  }\n}\n\nmutation CreateCart {\n  createShoppingCart {\n    ...CartFields\n  }\n}\n\nmutation AddCartItem($cartId: String!, $productOfferingId: String!, $quantity: Int!, $purchaseOption: String) {\n  addCartItem(\n    cartId: $cartId\n    productOfferingId: $productOfferingId\n    quantity: $quantity\n    purchaseOption: $purchaseOption\n  ) {\n    ...CartFields\n  }\n}\n\nmutation RemoveCartItem($cartId: String!, $cartItemId: String!) {\n  removeCartItem(cartId: $cartId, cartItemId: $cartItemId) {\n    ...CartFields\n  }\n}"): (typeof documents)["fragment CartFields on ShoppingCart {\n  id\n  lastUpdate\n  cartItem {\n    id\n    quantity\n    purchaseOption\n    productOffering {\n      id\n      name\n    }\n    itemPrice {\n      name\n      priceType\n      recurringChargePeriod\n      price {\n        dutyFreeAmount {\n          unit\n          value\n        }\n      }\n    }\n    itemTotalPrice {\n      name\n      priceType\n      recurringChargePeriod\n      price {\n        taxIncludedAmount {\n          unit\n          value\n        }\n      }\n    }\n  }\n  cartTotalPrice {\n    name\n    priceType\n    recurringChargePeriod\n    price {\n      taxIncludedAmount {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Cart($id: String!) {\n  shoppingCart(id: $id) {\n    ...CartFields\n  }\n}\n\nmutation CreateCart {\n  createShoppingCart {\n    ...CartFields\n  }\n}\n\nmutation AddCartItem($cartId: String!, $productOfferingId: String!, $quantity: Int!, $purchaseOption: String) {\n  addCartItem(\n    cartId: $cartId\n    productOfferingId: $productOfferingId\n    quantity: $quantity\n    purchaseOption: $purchaseOption\n  ) {\n    ...CartFields\n  }\n}\n\nmutation RemoveCartItem($cartId: String!, $cartItemId: String!) {\n  removeCartItem(cartId: $cartId, cartItemId: $cartItemId) {\n    ...CartFields\n  }\n}"];

export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;