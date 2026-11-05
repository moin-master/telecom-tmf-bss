from datetime import datetime

import strawberry

from bss_shared.graphql import DtoConverter
from identity import dto

_convert = DtoConverter()
_for = _convert.register


@_for(dto.Profile)
@strawberry.type
class Profile:
    customer_id: str
    individual_id: str
    name: str
    email: str | None


@_for(dto.Session)
@strawberry.type
class Session:
    token: str
    expires_at: datetime
    profile: Profile


def _service(info: strawberry.Info):
    return info.context["identity"]


def _token(info: strawberry.Info) -> str | None:
    return info.context["token"]


@strawberry.type
class Query:
    @strawberry.field
    def me(self, info: strawberry.Info) -> Profile:
        return _convert(_service(info).me(_token(info)))


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(
        self, info: strawberry.Info, email: str, password: str, given_name: str, family_name: str
    ) -> Session:
        return _convert(_service(info).register(email, password, given_name, family_name))

    @strawberry.mutation
    def sign_in(self, info: strawberry.Info, email: str, password: str) -> Session:
        return _convert(_service(info).sign_in(email, password))

    @strawberry.mutation
    def sign_out(self, info: strawberry.Info) -> bool:
        return _service(info).sign_out(_token(info))


schema = strawberry.Schema(query=Query, mutation=Mutation)
