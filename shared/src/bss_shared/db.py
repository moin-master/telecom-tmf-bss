import os
import types
import typing
from dataclasses import fields, is_dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from mongita import MongitaClientDisk
from mongita.database import Database

# Mongita keeps JSON-like documents. Datetimes are stored as UTC ISO text and
# Decimals as text, so they come back exact. Fields marked transient are
# relations the repository fills in; they are not stored.
TRANSIENT = {"transient": True}


def mongita_database(name: str, default_dir: Path) -> Database:
    folder = Path(os.environ.get("BSS_DATA_DIR") or default_dir) / name
    folder.mkdir(parents=True, exist_ok=True)
    return MongitaClientDisk(host=str(folder))[name]


def _encode(value):
    if is_dataclass(value):
        return {
            f.name: _encode(getattr(value, f.name))
            for f in fields(value)
            if not f.metadata.get("transient")
        }
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise ValueError("naive datetime; use timezone-aware UTC")
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, list):
        return [_encode(v) for v in value]
    return value


def _decode(hint, value):
    if value is None:
        return None
    origin = typing.get_origin(hint)
    if origin in (typing.Union, types.UnionType):
        (inner,) = [a for a in typing.get_args(hint) if a is not type(None)]
        return _decode(inner, value)
    if origin is list:
        return [_decode(typing.get_args(hint)[0], v) for v in value]
    if hint is datetime:
        return datetime.fromisoformat(value)
    if hint is Decimal:
        return Decimal(value)
    if is_dataclass(hint):
        return _from_dict(hint, value)
    return value


def _from_dict(cls, data: dict):
    hints = typing.get_type_hints(cls)
    kwargs = {
        f.name: _decode(hints[f.name], data[f.name])
        for f in fields(cls)
        if not f.metadata.get("transient") and f.name in data
    }
    return cls(**kwargs)


def to_doc(obj) -> dict:
    """Dataclass to a Mongita document; the top-level `id` becomes `_id`."""
    doc = _encode(obj)
    doc["_id"] = doc.pop("id")
    return doc


def from_doc(cls, doc: dict):
    data = dict(doc)
    data["id"] = data.pop("_id")
    return _from_dict(cls, data)
