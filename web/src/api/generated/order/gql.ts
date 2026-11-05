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
    "fragment OrderFields on ProductOrder {\n  id\n  state\n  creationDate\n  billingAccount {\n    id\n    name\n  }\n  relatedParty {\n    role\n    partyOrPartyRole {\n      id\n      name\n    }\n  }\n  productOrderItem {\n    id\n    quantity\n    productOffering {\n      id\n      name\n    }\n    itemTerm {\n      name\n      duration {\n        amount\n        units\n      }\n    }\n    product {\n      productCharacteristic {\n        name\n        value\n      }\n    }\n  }\n  orderTotalPrice {\n    name\n    priceType\n    recurringChargePeriod\n    price {\n      taxIncludedAmount {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Order($id: String!) {\n  productOrder(id: $id) {\n    ...OrderFields\n  }\n}\n\nmutation PlaceOrder($cartId: String!, $billingAccountId: String) {\n  createProductOrder(cartId: $cartId, billingAccountId: $billingAccountId) {\n    ...OrderFields\n  }\n}\n\nquery Orders {\n  productOrderList {\n    ...OrderFields\n  }\n}": typeof types.OrderFieldsFragmentDoc,
};
const documents: Documents = {
    "fragment OrderFields on ProductOrder {\n  id\n  state\n  creationDate\n  billingAccount {\n    id\n    name\n  }\n  relatedParty {\n    role\n    partyOrPartyRole {\n      id\n      name\n    }\n  }\n  productOrderItem {\n    id\n    quantity\n    productOffering {\n      id\n      name\n    }\n    itemTerm {\n      name\n      duration {\n        amount\n        units\n      }\n    }\n    product {\n      productCharacteristic {\n        name\n        value\n      }\n    }\n  }\n  orderTotalPrice {\n    name\n    priceType\n    recurringChargePeriod\n    price {\n      taxIncludedAmount {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Order($id: String!) {\n  productOrder(id: $id) {\n    ...OrderFields\n  }\n}\n\nmutation PlaceOrder($cartId: String!, $billingAccountId: String) {\n  createProductOrder(cartId: $cartId, billingAccountId: $billingAccountId) {\n    ...OrderFields\n  }\n}\n\nquery Orders {\n  productOrderList {\n    ...OrderFields\n  }\n}": types.OrderFieldsFragmentDoc,
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
export function graphql(source: "fragment OrderFields on ProductOrder {\n  id\n  state\n  creationDate\n  billingAccount {\n    id\n    name\n  }\n  relatedParty {\n    role\n    partyOrPartyRole {\n      id\n      name\n    }\n  }\n  productOrderItem {\n    id\n    quantity\n    productOffering {\n      id\n      name\n    }\n    itemTerm {\n      name\n      duration {\n        amount\n        units\n      }\n    }\n    product {\n      productCharacteristic {\n        name\n        value\n      }\n    }\n  }\n  orderTotalPrice {\n    name\n    priceType\n    recurringChargePeriod\n    price {\n      taxIncludedAmount {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Order($id: String!) {\n  productOrder(id: $id) {\n    ...OrderFields\n  }\n}\n\nmutation PlaceOrder($cartId: String!, $billingAccountId: String) {\n  createProductOrder(cartId: $cartId, billingAccountId: $billingAccountId) {\n    ...OrderFields\n  }\n}\n\nquery Orders {\n  productOrderList {\n    ...OrderFields\n  }\n}"): (typeof documents)["fragment OrderFields on ProductOrder {\n  id\n  state\n  creationDate\n  billingAccount {\n    id\n    name\n  }\n  relatedParty {\n    role\n    partyOrPartyRole {\n      id\n      name\n    }\n  }\n  productOrderItem {\n    id\n    quantity\n    productOffering {\n      id\n      name\n    }\n    itemTerm {\n      name\n      duration {\n        amount\n        units\n      }\n    }\n    product {\n      productCharacteristic {\n        name\n        value\n      }\n    }\n  }\n  orderTotalPrice {\n    name\n    priceType\n    recurringChargePeriod\n    price {\n      taxIncludedAmount {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Order($id: String!) {\n  productOrder(id: $id) {\n    ...OrderFields\n  }\n}\n\nmutation PlaceOrder($cartId: String!, $billingAccountId: String) {\n  createProductOrder(cartId: $cartId, billingAccountId: $billingAccountId) {\n    ...OrderFields\n  }\n}\n\nquery Orders {\n  productOrderList {\n    ...OrderFields\n  }\n}"];

export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;