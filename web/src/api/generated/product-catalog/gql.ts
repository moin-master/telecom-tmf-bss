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
    "query Offers($offset: Int!, $limit: Int!, $filter: ProductOfferingFilter) {\n  productOfferingList(offset: $offset, limit: $limit, filter: $filter) {\n    id\n    name\n    description\n    isSellable\n    category {\n      id\n      name\n    }\n    productSpecification {\n      brand\n      productSpecCharacteristic {\n        name\n        values\n      }\n    }\n    productOfferingPrice {\n      id\n      name\n      priceType\n      recurringChargePeriodType\n      price {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Offer($id: String!) {\n  productOffering(id: $id) {\n    id\n    name\n    description\n    isSellable\n    category {\n      id\n      name\n    }\n    productSpecification {\n      name\n      brand\n      description\n      productSpecCharacteristic {\n        name\n        description\n        values\n      }\n    }\n    productOfferingPrice {\n      id\n      name\n      priceType\n      recurringChargePeriodType\n      recurringChargePeriodLength\n      price {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Categories {\n  categoryList(offset: 0, limit: 100) {\n    id\n    name\n    isRoot\n  }\n}": typeof types.OffersDocument,
};
const documents: Documents = {
    "query Offers($offset: Int!, $limit: Int!, $filter: ProductOfferingFilter) {\n  productOfferingList(offset: $offset, limit: $limit, filter: $filter) {\n    id\n    name\n    description\n    isSellable\n    category {\n      id\n      name\n    }\n    productSpecification {\n      brand\n      productSpecCharacteristic {\n        name\n        values\n      }\n    }\n    productOfferingPrice {\n      id\n      name\n      priceType\n      recurringChargePeriodType\n      price {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Offer($id: String!) {\n  productOffering(id: $id) {\n    id\n    name\n    description\n    isSellable\n    category {\n      id\n      name\n    }\n    productSpecification {\n      name\n      brand\n      description\n      productSpecCharacteristic {\n        name\n        description\n        values\n      }\n    }\n    productOfferingPrice {\n      id\n      name\n      priceType\n      recurringChargePeriodType\n      recurringChargePeriodLength\n      price {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Categories {\n  categoryList(offset: 0, limit: 100) {\n    id\n    name\n    isRoot\n  }\n}": types.OffersDocument,
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
export function graphql(source: "query Offers($offset: Int!, $limit: Int!, $filter: ProductOfferingFilter) {\n  productOfferingList(offset: $offset, limit: $limit, filter: $filter) {\n    id\n    name\n    description\n    isSellable\n    category {\n      id\n      name\n    }\n    productSpecification {\n      brand\n      productSpecCharacteristic {\n        name\n        values\n      }\n    }\n    productOfferingPrice {\n      id\n      name\n      priceType\n      recurringChargePeriodType\n      price {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Offer($id: String!) {\n  productOffering(id: $id) {\n    id\n    name\n    description\n    isSellable\n    category {\n      id\n      name\n    }\n    productSpecification {\n      name\n      brand\n      description\n      productSpecCharacteristic {\n        name\n        description\n        values\n      }\n    }\n    productOfferingPrice {\n      id\n      name\n      priceType\n      recurringChargePeriodType\n      recurringChargePeriodLength\n      price {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Categories {\n  categoryList(offset: 0, limit: 100) {\n    id\n    name\n    isRoot\n  }\n}"): (typeof documents)["query Offers($offset: Int!, $limit: Int!, $filter: ProductOfferingFilter) {\n  productOfferingList(offset: $offset, limit: $limit, filter: $filter) {\n    id\n    name\n    description\n    isSellable\n    category {\n      id\n      name\n    }\n    productSpecification {\n      brand\n      productSpecCharacteristic {\n        name\n        values\n      }\n    }\n    productOfferingPrice {\n      id\n      name\n      priceType\n      recurringChargePeriodType\n      price {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Offer($id: String!) {\n  productOffering(id: $id) {\n    id\n    name\n    description\n    isSellable\n    category {\n      id\n      name\n    }\n    productSpecification {\n      name\n      brand\n      description\n      productSpecCharacteristic {\n        name\n        description\n        values\n      }\n    }\n    productOfferingPrice {\n      id\n      name\n      priceType\n      recurringChargePeriodType\n      recurringChargePeriodLength\n      price {\n        unit\n        value\n      }\n    }\n  }\n}\n\nquery Categories {\n  categoryList(offset: 0, limit: 100) {\n    id\n    name\n    isRoot\n  }\n}"];

export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;