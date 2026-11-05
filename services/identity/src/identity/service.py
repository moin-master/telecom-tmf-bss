import hashlib
import hmac
import secrets
import threading
from collections.abc import Callable
from datetime import datetime, timedelta

from bss_shared.clock import utcnow
from bss_shared.config import SESSION_HOURS
from bss_shared.errors import BadRequestError, ConflictError, UnauthorizedError
from customer.client import CustomerClient
from identity import dto, models
from identity.repository import IdentityRepository
from party.client import PartyClient

MIN_PASSWORD = 8
MAX_PASSWORD = 128

# scrypt from the standard library: the cost parameters are stored with each hash.
_N, _R, _P = 2**14, 8, 1


def _hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=_N, r=_R, p=_P)
    return f"scrypt${_N}${_R}${_P}${salt.hex()}${digest.hex()}"


def _verify(password: str, stored: str) -> bool:
    _, n, r, p, salt, digest = stored.split("$")
    candidate = hashlib.scrypt(
        password.encode(), salt=bytes.fromhex(salt), n=int(n), r=int(r), p=int(p)
    )
    return hmac.compare_digest(candidate, bytes.fromhex(digest))


# An unknown email is checked against this, so it takes as long as a wrong password.
_DUMMY = _hash("not a real password")

# Mongita has no transactions, so registering one email runs under one lock.
_REGISTER_LOCK = threading.Lock()


def _session_id(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class IdentityService:
    def __init__(
        self,
        repo: IdentityRepository,
        parties: PartyClient,
        customers: CustomerClient,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.repo = repo
        self.parties = parties
        self.customers = customers
        self.clock = clock

    def register(
        self, email: str, password: str, given_name: str, family_name: str
    ) -> dto.Session:
        email = email.strip().lower()
        if not MIN_PASSWORD <= len(password) <= MAX_PASSWORD:
            raise BadRequestError(
                f"password must have {MIN_PASSWORD} to {MAX_PASSWORD} characters"
            )
        with _REGISTER_LOCK:
            if self.repo.get_credential(email):
                raise ConflictError("That email is already registered")
            # The party service validates the names and the address.
            individual = self.parties.create_individual(given_name, family_name, [(email, True)])
            customer = self.customers.create_customer(individual.id)
            self.repo.save_credential(
                models.Credential(
                    id=email,
                    password_hash=_hash(password),
                    party_id=individual.id,
                    customer_id=customer.id,
                    created=self.clock(),
                )
            )
        return self._open_session(customer.id)

    def sign_in(self, email: str, password: str) -> dto.Session:
        credential = self.repo.get_credential(email.strip().lower())
        # One message and one cost for an unknown email and a wrong password.
        stored = credential.password_hash if credential else _DUMMY
        if not _verify(password, stored) or credential is None:
            raise UnauthorizedError("Email or password is wrong")
        return self._open_session(credential.customer_id)

    def me(self, token: str | None) -> dto.Profile:
        return self._profile(self._session(token).customer_id)

    def sign_out(self, token: str | None) -> bool:
        self.repo.delete_session(_session_id(self._token(token)))
        return True

    @staticmethod
    def _token(token: str | None) -> str:
        if not token:
            raise UnauthorizedError()
        return token

    def _session(self, token: str | None) -> models.Session:
        session = self.repo.get_session(_session_id(self._token(token)))
        if session is None or session.expires <= self.clock():
            raise UnauthorizedError()
        return session

    def _open_session(self, customer_id: str) -> dto.Session:
        token = secrets.token_urlsafe(32)
        expires = self.clock() + timedelta(hours=SESSION_HOURS)
        self.repo.save_session(
            models.Session(id=_session_id(token), customer_id=customer_id, expires=expires)
        )
        return dto.Session(token, expires, self._profile(customer_id))

    def _profile(self, customer_id: str) -> dto.Profile:
        customer = self.customers.get_customer(customer_id)
        individual = self.parties.get_individual(customer.engaged_party.id)
        preferred = next(
            (c for c in individual.contact_medium if c.preferred),
            individual.contact_medium[0] if individual.contact_medium else None,
        )
        return dto.Profile(
            customer_id=customer.id,
            individual_id=individual.id,
            name=individual.name,
            email=preferred.email_address if preferred else None,
        )
