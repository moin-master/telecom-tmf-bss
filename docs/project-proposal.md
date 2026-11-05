# Project proposal: Telecom BSS

Status: **draft for discussion**. Items marked *proposed* or *open* are not yet decided.

## 1. Goal

Build a proof of concept that implements a realistic telecom order-to-cash scenario using TM Forum Open API resource models, served over GraphQL, with Mongita (embedded document database) as storage. The result should be understandable end to end and structured so it can later grow into a real application.

## 2. Why GraphQL on top of TM Forum APIs

TM Forum Open APIs are REST/JSON, one API per domain (catalog, customer, ordering, inventory, billing, and so on). A client that needs a complete picture, such as a support agent screen showing a customer, their products, open orders, latest bill and tickets, must call many APIs and stitch the results.

GraphQL lets the client describe that picture in one request while the server resolves each part from its own domain.

## 3. Scenario

1. A catalog admin defines product specifications and offerings with prices.
2. A customer registers and gets a billing account.
3. The customer browses offerings and adds some to a shopping cart.
4. Checkout turns the cart into a product order.
5. The order is fulfilled: a service is created, resources (for example a SIM and a number) are allocated, and a shipment is created for physical items.
6. When the order completes, the product appears in the customer's product inventory.
7. Usage records are generated (simulated).
8. A billing cycle run produces a customer bill with applied rates.
9. The customer pays the bill.
10. Optionally the customer raises a trouble ticket.
11. A customer 360 query reads across all of the above.

## 4. TM Forum APIs in scope

| Area | API | Notes |
|------|-----|-------|
| Product catalog | TMF620 Product Catalog Management | specifications, offerings, prices |
| Customer registry | TMF629 Customer Management, TMF632 Party Management | |
| Accounts | TMF666 Account Management | billing accounts, billing cycle specification |
| Shopping cart | TMF663 Shopping Cart | |
| Ordering | TMF622 Product Ordering | order state machine |
| Service fulfilment | TMF641 Service Ordering, TMF638 Service Inventory | |
| Resources | TMF639 Resource Inventory | SIM, phone number |
| Shipment | TMF700 Shipping Order Management | *repo exists, v4.0.0 only, no v5* |
| Product inventory | TMF637 Product Inventory | what the customer owns |
| Usage | TMF635 Usage Management | simulated records |
| Billing | TMF678 Customer Bill Management | bill cycles, bills, applied rates |
| Payment | TMF676 Payment Management | |
| Support (optional) | TMF621 Trouble Ticket | |

The exact resources and fields will be confirmed by reading the specifications in [specs/](../specs/README.md). The project uses **TM Forum v5** (OpenAPI yaml). TMF641, TMF676 and TMF700 have no v5 file in the tmforum-apis repositories yet.

## 5. Architecture (proposed)

A **workspace-hosted set of services**: one separate Python project per TM Forum domain (a `uv` workspace), each with its own code, Mongita database and GraphQL schema. A thin host app mounts every service under its own path, so everything runs as one process on one port. A combined schema at `/graphql` serves the customer 360 query.

Services call each other through a small client interface per service. Today the client calls the other service's code in the same process; later it can make an HTTP call without changing the callers.

The technologies used (Python, GraphQL, Mongita and the rest) are listed in [project-tech-stack.md](project-tech-stack.md).

Module rules, the service block diagram, dependencies and event flow are in [project-architecture.md](project-architecture.md).

Path to a real application:

- Mongita to MongoDB, since Mongita uses the MongoDB API; only the repository layer changes.
- A service replaced by calls to a real TM Forum service, with the GraphQL schema unchanged.
- A service run in its own process on its own port, with a reverse proxy keeping the public URLs and the client interface switched to HTTP.

Alternatives considered: a single-package modular monolith (simplest, but services are not independent projects), full microservices with a reverse proxy and 15 ports (more realistic, much heavier to run), and a monolith that also exposes TM Forum REST endpoints (closer to the standard, doubles the API work).

## 6. Technical considerations

| Topic | Approach (proposed) |
|-------|---------------------|
| State machines (order, product, ticket) | enforced in the service layer; defined by spec text, not the swagger files |
| Order orchestration | event-driven inside the host process, synchronous first for clarity |
| Billing | simple: monthly recurring charges plus usage; no tax, proration or discounts initially |
| Money and time | `decimal.Decimal` for amounts, timezone-aware `datetime` (UTC) for timestamps |
| Billing cycle trigger | an on-demand mutation (for example `runBillingCycle`) before any scheduler |
| Storage | one Mongita database folder per service so data survives restarts; seed data in a Python seed module per service |
| Bundles and purchase options | a bundle is a ProductOffering with `isBundle` and `bundledProductOffering` (the components stay normal offerings). Own it, trade-in and finance are alternative ProductOfferingPrices tagged with `purchaseOption` (own, tradeIn, finance), a project extension that TMF620 does not define; untagged prices apply to every option. The cart prices an item with one option (default own). |
| Promotions and contract | discount offers live in the catalog (category Promotions, not sellable on their own) and are applied by the cart. A bundle points to them with `productOfferingRelationship` types `launchOffer` (three alternatives, shopper picks one, 6 month `productOfferingTerm`), `activationWaiver`, `multiBundleDiscount` and `contract` (24 month term). The contract is only available with Finance or Trade-in (`availableWith` on the term, a project extension). Discounts are copied into the cart item as negative lines; the cart splits the monthly total into "first N months" and "after". The 5.00 double bundle discount applies once per cart from two bundles. |
| Configuration (MSISDN) | the shopper configures a SIM or eSIM component in the cart. The number is a `LogicalResource` in TMF639 (`/resource`, seeded pool, `resourceCharacteristic` `MSISDN`). The catalog marks the SIM and eSIM specifications with an `MSISDN` characteristic and a `resourceSpecification` reference. The configure page lists idle numbers; choosing one reserves it in TMF639 (`allocationStatus` reserved) and the cart item stores it as the `TEL_MSISDN` characteristic plus a reference to the resource. Removing the item releases the number. SIM or eSIM is fixed by the bundle; the eSIM ICCID/EID is allocated at fulfilment, outside this scope. Assumptions, to confirm: reservation released on item removal, expiry later; unconfigured lines show a badge and do not block checkout yet; one number per unit, so lines needing a number are limited to quantity 1; items without a SIM have no Configure link and no marker. Configured state is derived, not stored: TMF663 has no such field (`CartItemStatusType` is only active or saveForLater), so a SIM or eSIM line is unconfigured when it has no `TEL_MSISDN` characteristic. Colour is a UI choice, not TMF: on `/cart` the parts of a bundle are quiet tiles across the card, and only the SIM or eSIM tile that still needs a number is dashed and carries the one lemon Configure button with the note "Needs a number" (a single SIM offer has the same note and button in a row); once a number is saved the tile shows it with an Edit link. No other accent colours. |
| Configure page | `/cart/items/:id/configure`, linked from each cart line. Shows the full bundle structure as a tree (bundle, phone, plan, eSIM, add-ons, discounts) read from the catalog, with the number picker on the SIM or eSIM node. Slice order: TMF639 reads, catalog characteristic, cart reserve and release, then the page. Every part of a bundle has its own panel, as TMF663 allows (a nested `cartItem` with its own `product` characteristics): the tiles of the bundle tree are the tabs. Selecting a tile outlines it and titles the panel below with that offer (for example "eSIM, part of Plus Bundle"). The tile that needs a number says "Needs a number" (or shows the chosen number) and opens the number picker; every other tile says "Nothing to configure" and its panel shows a plain message that the offer is included as it is. The page opens on the first tile that needs configuration. A single SIM offer has just its panel, titled with the offer. |
| Bundle tree | the configure page draws the bundle as a tree, not a text list: the bundle at the top, its components as tiles below joined by connector lines (CSS only), and discounts hanging underneath. Each tile has the lemon circle with the product emoji, a role label (Device, Plan, SIM, Add-on), the name and one key characteristic (for example 256 GB, Unlimited). The SIM or eSIM tile carries the number picker and the "Needs configuration" badge. Included components have a solid outline, optional ones (the protection plan, an `addOn` relationship) a dashed outline. On a phone the tree becomes a vertical list with a line on the left. The `/cart` line shows the same components as small icon chips in the same order. TM Forum gives the structure, not the look: TMF620 `bundledProductOffering` with `bundledProductOfferingOption` (`numberRelOfferDefault`, `LowerLimit`, `UpperLimit`) and TMF663 nested `cartItem`. Catalog change: the bundled entries gain the option limits (seeded 1/1/1) and a `role` (device, plan, sim, addOn), a project extension because TMF has no role on a bundled offering. No per-component prices; only the bundle price and the discounts are shown, since the components do not add up to the bundle price. |
| Reserve a number | TMF639 has no reserve operation: reserving is `patchResource` on the number. The first resource mutation is `patchResource(id, patch)` with merge-patch semantics (only the fields sent change; this is the PATCH policy for the resource service). Reserving sets `allocationStatus` reserved and `usageState` busy; releasing sets them back to available and idle. The service guards the transition: only an available number can be reserved and only a reserved one released, otherwise a TM Forum `409 Conflict`. The cart (which now depends on resource, through its client only) stores the choice on the cart item the TMF663 way: `product.productCharacteristic` `TEL_MSISDN` and `product.realizingResource`, a reference to the TMF639 resource. Choosing another number releases the old one and reserves the new one; removing the item releases it. A line that needs a number has quantity 1 and is never merged with an identical line (two bundles are two lines with two numbers). No timed expiry yet: abandoned carts free their numbers when cart expiry (issue 5) arrives. `ResourceStateChangeEvent` is not published yet, because the shared event bus does not exist. |
| Checkout | four slices, each its own issue and PR, in this order. **1 Party and customer:** `party` (TMF632 `Individual`: `givenName`, `familyName`, `status` initialized, an `EmailContactMedium`) and `customer` (TMF629 `Customer`, a `PartyRole` whose required `engagedParty` refers to the Individual; status Approved, a project choice because TMF leaves it free text). **2 Sign-in:** TM Forum defines nothing for email and password, so it is a separate non-TMF `identity` module (project extension, `/identity`) with `register`, `signIn`, `signOut` and `me`. It keeps the email, a salted password hash (standard library only) and the party and customer ids; Party and Customer never hold a password. Sessions are opaque tokens that expire; wrong credentials give a TM Forum style 401 without saying which part was wrong. **3 Cart with customer:** TMF663 `relatedParty` with role customer (`partyOrPartyRole` refers to the Customer) and `contactMedium` for a guest; set with `patchShoppingCart`, validated through the customer client. **4 Order:** `product_order` (TMF622). `createProductOrder(cartId)` is the one project extension: the order service reads the cart through its client and builds a pure TMF622 `ProductOrder` (state acknowledged, `productOrderItem` with action add, `productOffering`, `product` with `TEL_MSISDN` and `realizingResource`, `itemPrice`, `itemTotalPrice`, `orderTotalPrice`, `relatedParty` customer, channel web). The cart must have a customer and every SIM line a number. The order service checks the sign-in token, so an order can only be created from, and read by, its own customer (403 for another customer's cart, 404 for another customer's order). Afterwards the cart is deleted (TMF663 `DELETE`) and the numbers stay reserved; reservation expiry (#26) must not free a number that an order holds. Out of scope: fulfilment, service inventory, billing account, billing, payment, events (no shared event bus), email verification, password reset. |
| Billing details | three slices, each its own issue and PR. **1 Account (TMF666, `/account`):** a `BillingAccount` with `name`, `state` Active, `ratingType` postpaid, `relatedParty` (role customer, the Customer; set by the service from the sign-in token, not sent by the client), one `contact` (`contactName`, `contactType` primary, `contactMedium` list holding a `GeographicAddressContactMedium` with `street1`, `street2`, `city`, `stateOrProvince`, `postCode`, `country` and an `EmailContactMedium` with `emailAddress`) and a fixed `billStructure` (presentation media Email, format Standard, cycle Monthly, seeded as TMF666 reference data: `BillPresentationMedia`, `BillFormat`, `BillingCycleSpecification`). A customer can have several accounts. Operations: `createBillingAccount`, `patchBillingAccount` (merge-patch), `billingAccount(id)`, `billingAccountList`; the service checks the sign-in token, so only the owner reads or changes an account. Validation: a name, a valid email, and street, city, post code and country are required. `ContactMedium` is a GraphQL union of the two concrete types; the input carries a `type` field (`EmailContactMedium` or `GeographicAddressContactMedium`) that plays the role of `@type`. `defaultPaymentMethod`, `paymentPlan`, `paymentStatus` and the balance stay empty (payment is excluded). **2 Order:** `createProductOrder(cartId, billingAccountId)` (project extension arguments) requires an account that belongs to the customer; the order and each `productOrderItem` carry the same `billingAccount` reference (TMF622 has it on both). **3 Web:** a "Billing details" step on `/checkout` between Account and Place order: choose one of your accounts (the newest preselected) or add a new one (name, address, email; contact name and email prefilled from the sign-in), and the confirmation page shows who is billed. Out of scope: card or bank details, billing runs and bills, paper bills, address lookup or validation (TMF673 is not in the snapshot), events. |
| Polymorphism (`@type`), reference objects (`href`), free-form values, PATCH semantics | one agreed policy per issue, written down once |
| Scope creep | fixed slice order below |
