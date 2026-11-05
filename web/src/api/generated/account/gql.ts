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
    "fragment BillingAccountFields on BillingAccount {\n  id\n  name\n  state\n  contact {\n    id\n    contactName\n    contactMedium {\n      __typename\n      ... on EmailContactMedium {\n        emailAddress\n      }\n      ... on GeographicAddressContactMedium {\n        street1\n        street2\n        city\n        stateOrProvince\n        postCode\n        country\n      }\n    }\n  }\n}\n\nquery BillingAccounts {\n  billingAccountList {\n    ...BillingAccountFields\n  }\n}\n\nquery BillingAccount($id: String!) {\n  billingAccount(id: $id) {\n    ...BillingAccountFields\n  }\n}\n\nmutation CreateBillingAccount($name: String!, $contact: [ContactInput!]!) {\n  createBillingAccount(name: $name, contact: $contact) {\n    ...BillingAccountFields\n  }\n}": typeof types.BillingAccountFieldsFragmentDoc,
};
const documents: Documents = {
    "fragment BillingAccountFields on BillingAccount {\n  id\n  name\n  state\n  contact {\n    id\n    contactName\n    contactMedium {\n      __typename\n      ... on EmailContactMedium {\n        emailAddress\n      }\n      ... on GeographicAddressContactMedium {\n        street1\n        street2\n        city\n        stateOrProvince\n        postCode\n        country\n      }\n    }\n  }\n}\n\nquery BillingAccounts {\n  billingAccountList {\n    ...BillingAccountFields\n  }\n}\n\nquery BillingAccount($id: String!) {\n  billingAccount(id: $id) {\n    ...BillingAccountFields\n  }\n}\n\nmutation CreateBillingAccount($name: String!, $contact: [ContactInput!]!) {\n  createBillingAccount(name: $name, contact: $contact) {\n    ...BillingAccountFields\n  }\n}": types.BillingAccountFieldsFragmentDoc,
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
export function graphql(source: "fragment BillingAccountFields on BillingAccount {\n  id\n  name\n  state\n  contact {\n    id\n    contactName\n    contactMedium {\n      __typename\n      ... on EmailContactMedium {\n        emailAddress\n      }\n      ... on GeographicAddressContactMedium {\n        street1\n        street2\n        city\n        stateOrProvince\n        postCode\n        country\n      }\n    }\n  }\n}\n\nquery BillingAccounts {\n  billingAccountList {\n    ...BillingAccountFields\n  }\n}\n\nquery BillingAccount($id: String!) {\n  billingAccount(id: $id) {\n    ...BillingAccountFields\n  }\n}\n\nmutation CreateBillingAccount($name: String!, $contact: [ContactInput!]!) {\n  createBillingAccount(name: $name, contact: $contact) {\n    ...BillingAccountFields\n  }\n}"): (typeof documents)["fragment BillingAccountFields on BillingAccount {\n  id\n  name\n  state\n  contact {\n    id\n    contactName\n    contactMedium {\n      __typename\n      ... on EmailContactMedium {\n        emailAddress\n      }\n      ... on GeographicAddressContactMedium {\n        street1\n        street2\n        city\n        stateOrProvince\n        postCode\n        country\n      }\n    }\n  }\n}\n\nquery BillingAccounts {\n  billingAccountList {\n    ...BillingAccountFields\n  }\n}\n\nquery BillingAccount($id: String!) {\n  billingAccount(id: $id) {\n    ...BillingAccountFields\n  }\n}\n\nmutation CreateBillingAccount($name: String!, $contact: [ContactInput!]!) {\n  createBillingAccount(name: $name, contact: $contact) {\n    ...BillingAccountFields\n  }\n}"];

export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;