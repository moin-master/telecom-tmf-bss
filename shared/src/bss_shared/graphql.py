from dataclasses import fields, is_dataclass


class DtoConverter:
    """Turns service DTOs into the Strawberry types registered for them.

    Field names match on both sides, so one generic function replaces
    per-type conversion code.
    """

    def __init__(self) -> None:
        self._types: dict[type, type] = {}

    def register(self, dto_class: type):
        def decorator(gql_class: type) -> type:
            self._types[dto_class] = gql_class
            return gql_class

        return decorator

    def __call__(self, value):
        if is_dataclass(value):
            gql_class = self._types[type(value)]
            return gql_class(
                **{f.name: self(getattr(value, f.name)) for f in fields(value)}
            )
        if isinstance(value, list):
            return [self(v) for v in value]
        return value
