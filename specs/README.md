# TM Forum specifications

Local copy of the TM Forum Open API specifications used by this project. These files are a **fixed snapshot**: they are not updated, pulled or re-cloned unless the project owner decides to.

## Source

- Organisation: https://github.com/tmforum-apis
- Each API is one repository, `https://github.com/tmforum-apis/<repository>`
- Cloned on 2026-11-02 with `git clone --depth 1` (latest default branch at that time), then reduced to the files listed below. The `.git` folders were removed, so they cannot be pulled.

Each folder contains exactly two files: `LICENSE` and one specification file.

## Specifications

Chosen format: **v5 OpenAPI yaml** (`*.oas.yaml`).

| TMF | API | Folder | Source repository | File kept |
|-----|-----|--------|-------------------|-----------|
| TMF620 | Product Catalog Management | TMF620_ProductCatalog | https://github.com/tmforum-apis/TMF620_ProductCatalog | TMF620-Product_Catalog_Management-v5.0.0.oas.yaml |
| TMF621 | Trouble Ticket | TMF621_TroubleTicket | https://github.com/tmforum-apis/TMF621_TroubleTicket | TMF621-Trouble_Ticket-v5.0.1.oas.yaml |
| TMF622 | Product Ordering | TMF622_ProductOrder | https://github.com/tmforum-apis/TMF622_ProductOrder | TMF622-ProductOrdering-v5.0.0.oas.yaml |
| TMF629 | Customer Management | TMF629_CustomerManagement | https://github.com/tmforum-apis/TMF629_CustomerManagement | TMF629-Customer_Management-v5.0.1.oas.yaml |
| TMF632 | Party Management | TMF632_PartyManagement | https://github.com/tmforum-apis/TMF632_PartyManagement | TMF632-Party_Management-v5.0.0.oas.yaml |
| TMF635 | Usage Management | TMF635_UsageManagement | https://github.com/tmforum-apis/TMF635_UsageManagement | TMF635-Product_Usage_Management-v5.0.0.oas.yaml |
| TMF637 | Product Inventory | TMF637_ProductInventory | https://github.com/tmforum-apis/TMF637_ProductInventory | TMF637-ProductInventory-v5.0.0.oas.yaml |
| TMF638 | Service Inventory | TMF638_ServiceInventory | https://github.com/tmforum-apis/TMF638_ServiceInventory | TMF638-Service_Inventory_Management-v5.0.0.oas.yaml |
| TMF639 | Resource Inventory | TMF639_ResourceInventory | https://github.com/tmforum-apis/TMF639_ResourceInventory | TMF639-Resource_Inventory_Management-v5.0.0.oas.yaml |
| TMF663 | Shopping Cart | TMF663_ShoppingCart | https://github.com/tmforum-apis/TMF663_ShoppingCart | TMF663-Shopping_Cart-v5.0.0.oas.yaml |
| TMF666 | Account Management | TMF666_AccountManagement | https://github.com/tmforum-apis/TMF666_AccountManagement | TMF666-Account_Management-v5.0.0.oas.yaml |
| TMF678 | Customer Bill Management | TMF678_CustomerBill | https://github.com/tmforum-apis/TMF678_CustomerBill | TMF678-CustomerBill-v5.0.0.oas.yaml |

## No v5 yaml available

These three repositories have no v5 file on GitHub. The newest v4 swagger JSON is kept instead, and only that one file. v5 preview pages exist on tmforum.org for TMF641 and TMF700 but could not be downloaded automatically; TMF676 has no v5.

| TMF | API | Folder | Source repository | File kept |
|-----|-----|--------|-------------------|-----------|
| TMF641 | Service Ordering | TMF641_ServiceOrder | https://github.com/tmforum-apis/TMF641_ServiceOrder | TMF641-ServiceOrdering-v4.2.0.swagger.json |
| TMF676 | Payment Management | TMF676_PaymentManagement | https://github.com/tmforum-apis/TMF676_PaymentManagement | TMF676-Payment-v4.0.0.swagger.json |
| TMF700 | Shipping Order Management | TMF700_ShippingOrder | https://github.com/tmforum-apis/TMF700_ShippingOrder | TMF700-ShippingOrder-v4.0.0.swagger.json |

## License

Every source repository is licensed under the **Apache License 2.0** (checked on GitHub on 2026-11-02). Each folder keeps the `LICENSE` file from its repository (the repository READMEs were removed). The specifications are the work of TM Forum and are included here unmodified (some files were removed, none edited). This project is not an official TM Forum product.

The TM Forum user guides are not included and have their own terms at https://www.tmforum.org.

## Notes

- The repositories contain only the OpenAPI/swagger files, not the TM Forum user guides. State machines (allowed status transitions) are described in the user guides, so they are not in this folder.
- Do not edit these files. Project decisions about which fields to keep or skip are recorded in `docs/`.
- To refresh a specification, re-clone it from its source repository on purpose and update this file.
