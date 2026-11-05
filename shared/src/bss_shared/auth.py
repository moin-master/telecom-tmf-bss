def bearer_token(authorization: str | None) -> str | None:
    """The token of an `Authorization: Bearer <token>` header, or None."""
    scheme, _, token = (authorization or "").partition(" ")
    return token.strip() if scheme.lower() == "bearer" and token.strip() else None
