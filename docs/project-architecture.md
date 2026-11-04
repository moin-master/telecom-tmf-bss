# Project architecture: Telecom BSS

Status: **draft for discussion**. Complements [project-proposal.md](project-proposal.md); decisions are tracked there.

## 1. Overview

Structure of the workspace-hosted services chosen in [project-proposal.md](project-proposal.md) (scope, scenario, stack and decisions live there). Each block below is a service, a separate Python project named after the TM Forum Open API it implements. A host app mounts all services in one process on one port.

## 2. Service block diagram

Arrows point to the module being called (service interface). Event traffic goes through the event bus.

```ascii
            Client: support agent UI, storefront, API consumer
                                  |
                                  v
+----------------------------------------------------------------------+
|  Host app (FastAPI): mounts each service; combined schema, cust. 360 |
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
|  [TMF621 Trouble Ticket]   |        | Mongita, one database folder   |
+----------------------------+        | per service, never shared      |
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
| cart | TMF663 | TMF620, TMF639 | none |
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

These are the intended dependencies; they will be adjusted when the specifications are read.

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

- Each service is its own Python project (`uv` workspace member) and owns its database file; no service reads another service's database or repositories.
- Cross-service access goes through the other service's client interface and ids only. The client calls the service in-process today and can become an HTTP call later.
- A service never imports another service's internals, only its client interface.
- Inside a service: GraphQL resolver -> service -> repository.
- Events mirror TM Forum notifications; the in-process bus can be replaced by a broker later.
