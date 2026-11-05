import strawberry

from bss_shared.graphql import DtoConverter
from party import dto

_convert = DtoConverter()
_for = _convert.register


@_for(dto.EmailContactMedium)
@strawberry.type
class EmailContactMedium:
    id: str
    preferred: bool
    contact_type: str
    email_address: str


@_for(dto.Individual)
@strawberry.type
class Individual:
    id: str
    given_name: str
    family_name: str
    name: str
    status: str
    contact_medium: list[EmailContactMedium]


@strawberry.input
class EmailContactMediumInput:
    email_address: str
    preferred: bool = False


@strawberry.input
class IndividualFilter:
    # Matches an email address of the individual, ignoring case.
    email: str | None = None


def _service(info: strawberry.Info):
    return info.context["party"]


@strawberry.type
class Query:
    @strawberry.field
    def individual(self, info: strawberry.Info, id: str) -> Individual:
        return _convert(_service(info).get_individual(id))

    @strawberry.field
    def individual_list(
        self, info: strawberry.Info, filter: IndividualFilter | None = None
    ) -> list[Individual]:
        f = filter or IndividualFilter()
        return _convert(_service(info).list_individuals(f.email))


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_individual(
        self,
        info: strawberry.Info,
        given_name: str,
        family_name: str,
        contact_medium: list[EmailContactMediumInput] | None = None,
    ) -> Individual:
        emails = [(c.email_address, c.preferred) for c in contact_medium or []]
        return _convert(_service(info).create_individual(given_name, family_name, emails))


schema = strawberry.Schema(query=Query, mutation=Mutation)
