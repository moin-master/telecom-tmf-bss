from bss_shared.errors import BadRequestError

DEFAULT_LIMIT = 20
MAX_LIMIT = 100


def check_page(offset: int, limit: int) -> None:
    if offset < 0:
        raise BadRequestError("offset must be 0 or greater")
    if not 1 <= limit <= MAX_LIMIT:
        raise BadRequestError(f"limit must be between 1 and {MAX_LIMIT}")
