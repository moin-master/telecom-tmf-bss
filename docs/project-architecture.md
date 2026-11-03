# Project architecture: Telecom BSS

Status: **draft for discussion**. Complements [project-proposal.md](project-proposal.md); decisions are tracked there.

## 1. Overview

Structure of the modular monolith chosen in [project-proposal.md](project-proposal.md) (scope, scenario, stack and decisions live there). Each block below is a module named after the TM Forum Open API it implements.

## 2. Service block diagram

Arrows point to the module being called (service interface). Event traffic goes through the event bus.

```text
            Client: support agent UI, storefront, API consumer
                                  |
                                  v
+----------------------------------------------------------------------+
|  GraphQL layer (FastAPI + Strawberry): one schema, customer 360      |
+----------------------------------------------------------------------+
        |                                          |
        v                                          v
+----------------------------+        +--------------------------------+
| PARTY AND ACCOUNT          |        | CATALOG AND SALES              |
|                            |        |                                |
|  [TMF632 Party Mgmt]       |        |  [TMF620 Product Catalog]      |
|         ^                  |        |         ^                      |
|  [TMF629 Customer Mgmt]    |        |  [TMF663 Shopping Cart]        |
|         ^                  |        |         ^                      |
|  [TMF666 Account Mgmt]     |        |  [TMF622 Product Ordering]     |
+----------------------------+        +----------------+---------------+
                                                        |
                                                        | order accepted
                                                        v
+----------------------------------------------------------------------+
|                        IN-PROCESS EVENT BUS                          |
+------------------+-------------------------------------+-------------+
                   | order accepted                      | order completed
                   v                                     |
+--------------------------------------------------+     |
| FULFILMENT                                       |     |
|                                                  |     |
|  [TMF641 Service Ordering]                       |     |
|         |                                        |     |
|         +--> [TMF638 Service Inventory]          |     |
|         |                                        |     |
|         +--> [TMF639 Resource Inventory]         |     |
|                                                  |     |
|  [TMF700 Shipping Order Management]              |     |
|                                                  |     |
|  publishes: fulfilment done, shipment done       |     |
+--------------------------------------------------+     |
                                                         v
+----------------------------+        +--------------------------------+
| INVENTORY                  |        | USAGE, BILLING, PAYMENT        |
|                            |        |                                |
|  [TMF637 Product Inventory]| <------|  [TMF635 Usage Mgmt]           |
|                            |        |         ^                      |
|                            |        |  [TMF678 Customer Bill Mgmt]   |
|                            |        |         ^                      |
|                            |        |  [TMF676 Payment Mgmt]         |
+----------------------------+        +--------------------------------+

+----------------------------+        +--------------------------------+
| SUPPORT (optional)         |        | STORAGE                        |
|  [TMF621 Trouble Ticket]   |        | SQLite, one set of tables per  |
+----------------------------+        | module, never shared           |
                                      +--------------------------------+
```

Calls between groups are not all drawn; the full dependency list is in section 3.

## 3. Module dependencies

What each module is for is described per API in proposal section 4. This table adds only the structure: which modules a module calls through their service interfaces, and which events it publishes.

| Module | API | Depends on | Publishes |
|--------|-----|------------|-----------|
| party | TMF632 | none | none |
| customer | TMF629 | TMF632 | none |
| account | TMF666 | TMF629 | none |
| catalog | TMF620 | none | none |
| cart | TMF663 | TMF620 | none |
| order | TMF622 | TMF663, TMF620, TMF629 | order accepted, order completed |
| service-order | TMF641 | TMF639, TMF638 | fulfilment done |
| service-inventory | TMF638 | none | none |
| resource | TMF639 | none | none |
| shipment | TMF700 | none | shipment done |
| product-inventory | TMF637 | none | product active |
| usage | TMF635 | TMF637 | none |
| billing | TMF678 | TMF666, TMF635 | none |
| payment | TMF676 | TMF678 | none |
| ticket | TMF621 | TMF629 | none |

## 4. Event flow

The business steps are in proposal section 3. This is how the modules trigger each other.

| Event | Published by | Consumed by | Effect |
|-------|--------------|-------------|--------|
| order accepted | TMF622 | TMF641, TMF700 | service created and resources allocated; shipment created for physical items |
| fulfilment done | TMF641 | TMF622 | order moves toward completed |
| shipment done | TMF700 | TMF622 | order moves toward completed |
| order completed | TMF622 | TMF637 | the customer's product is created |
| product active | TMF637 | TMF678 | billing setup for the product |

## 5. Rules

- Each module owns its tables; no module reads another module's tables or repositories.
- Cross-module access goes through service interfaces and ids only.
- Inside a module: GraphQL resolver -> service -> repository.
- Events mirror TM Forum notifications; the in-process bus can be replaced by a broker later.

## 6. Open points

- The dependencies above are the intended ones; they will be adjusted when the specifications are read.
- Open decisions on shipment and spec version are tracked in the proposal (section 9).
