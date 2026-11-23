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
    "fragment ServiceFields on Service {\n  id\n  name\n  state\n  startDate\n  isBundle\n  serviceType\n  supportingService {\n    id\n    name\n    referredType\n  }\n  serviceRelationship {\n    relationshipType\n    service {\n      id\n      name\n      referredType\n    }\n  }\n  relatedEntity {\n    role\n    entity {\n      id\n      name\n      referredType\n    }\n  }\n  serviceOrderItem {\n    serviceOrderId\n    itemId\n  }\n  serviceCharacteristic {\n    name\n    value\n  }\n  supportingResource {\n    id\n    name\n  }\n}\n\nquery Services {\n  serviceList {\n    ...ServiceFields\n  }\n}": typeof types.ServiceFieldsFragmentDoc,
};
const documents: Documents = {
    "fragment ServiceFields on Service {\n  id\n  name\n  state\n  startDate\n  isBundle\n  serviceType\n  supportingService {\n    id\n    name\n    referredType\n  }\n  serviceRelationship {\n    relationshipType\n    service {\n      id\n      name\n      referredType\n    }\n  }\n  relatedEntity {\n    role\n    entity {\n      id\n      name\n      referredType\n    }\n  }\n  serviceOrderItem {\n    serviceOrderId\n    itemId\n  }\n  serviceCharacteristic {\n    name\n    value\n  }\n  supportingResource {\n    id\n    name\n  }\n}\n\nquery Services {\n  serviceList {\n    ...ServiceFields\n  }\n}": types.ServiceFieldsFragmentDoc,
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
export function graphql(source: "fragment ServiceFields on Service {\n  id\n  name\n  state\n  startDate\n  isBundle\n  serviceType\n  supportingService {\n    id\n    name\n    referredType\n  }\n  serviceRelationship {\n    relationshipType\n    service {\n      id\n      name\n      referredType\n    }\n  }\n  relatedEntity {\n    role\n    entity {\n      id\n      name\n      referredType\n    }\n  }\n  serviceOrderItem {\n    serviceOrderId\n    itemId\n  }\n  serviceCharacteristic {\n    name\n    value\n  }\n  supportingResource {\n    id\n    name\n  }\n}\n\nquery Services {\n  serviceList {\n    ...ServiceFields\n  }\n}"): (typeof documents)["fragment ServiceFields on Service {\n  id\n  name\n  state\n  startDate\n  isBundle\n  serviceType\n  supportingService {\n    id\n    name\n    referredType\n  }\n  serviceRelationship {\n    relationshipType\n    service {\n      id\n      name\n      referredType\n    }\n  }\n  relatedEntity {\n    role\n    entity {\n      id\n      name\n      referredType\n    }\n  }\n  serviceOrderItem {\n    serviceOrderId\n    itemId\n  }\n  serviceCharacteristic {\n    name\n    value\n  }\n  supportingResource {\n    id\n    name\n  }\n}\n\nquery Services {\n  serviceList {\n    ...ServiceFields\n  }\n}"];

export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;