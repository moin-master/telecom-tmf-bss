from datetime import datetime

import strawberry

from bss_shared.graphql import DtoConverter
from customer import dto

_convert = DtoConverter()
_for = _convert.register


@_for(dto.TimePeriod)
@strawberry.type
class TimePeriod:
    start_date_time: datetime | None
    end_date_time: datetime | None


@_for(dto.PartyRef)
@strawberry.type
class PartyRef:
    id: str
    name: str
    referred_type: str


@_for(dto.Customer)
@strawberry.type
class Customer:
    id: str
    name: str
    status: str
    valid_for: TimePeriod
    engaged_party: PartyRef


@strawberry.input
class CustomerFilter:
    engaged_party_id: str | None = None


def _service(info: strawberry.Info):
    return info.context["customers"]


@strawberry.type
class Query:
    @strawberry.field
    def customer(self, info: strawberry.Info, id: str) -> Customer:
        return _convert(_service(info).get_customer(id))

    @strawberry.field
    def customer_list(
        self, info: strawberry.Info, filter: CustomerFilter | None = None
    ) -> list[Customer]:
        f = filter or CustomerFilter()
        return _convert(_service(info).list_customers(f.engaged_party_id))


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_customer(self, info: strawberry.Info, engaged_party_id: str) -> Customer:
        return _convert(_service(info).create_customer(engaged_party_id))


schema = strawberry.Schema(query=Query, mutation=Mutation)
