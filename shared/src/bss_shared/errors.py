from graphql import GraphQLError


class TmfError(GraphQLError):
    """GraphQL error carrying the TM Forum error fields in its extensions."""

    def __init__(self, code: str, reason: str, message: str, status: int):
        super().__init__(
            message,
            extensions={"code": code, "reason": reason, "status": status},
        )


class NotFoundError(TmfError):
    def __init__(self, resource: str, id: str):
        super().__init__(
            "NotFound", "Resource not found", f"{resource} {id} was not found", 404
        )


class BadRequestError(TmfError):
    def __init__(self, message: str):
        super().__init__("BadRequest", "Invalid request", message, 400)


class ConflictError(TmfError):
    def __init__(self, message: str):
        super().__init__("Conflict", "Conflict", message, 409)


class UnauthorizedError(TmfError):
    def __init__(self, message: str = "Sign in to continue"):
        super().__init__("Unauthorized", "Unauthorized", message, 401)


class ForbiddenError(TmfError):
    def __init__(self, message: str = "You are not allowed to do that"):
        super().__init__("Forbidden", "Forbidden", message, 403)
