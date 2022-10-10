import hashlib
import uuid
from datetime import datetime
from typing import Any, Generator, KeysView, Optional

from .constants import DEFAULT_ENCODING


class Session:
    def __init__(
        self,
        max_age: Optional[datetime] = None,
        identity: Optional[str] = None,
        created: Optional[int] = None,
        changed: bool = False,
        data: Optional[dict] = None,
    ) -> None:
        self.max_age = max_age
        self._identity = (
            identity
            or hashlib.sha256(uuid.uuid4().hex.encode(DEFAULT_ENCODING)).hexdigest()
        )
        self._created = created
        self._changed = changed
        self._data = data or {}
        self._expired: bool = False

    @property
    def created(self) -> Optional[int]:
        if self._created:
            return int(self._created)
        return None

    @property
    def changed(self) -> bool:
        return self._changed

    @property
    def identity(self) -> str:
        return self._identity

    @property
    def expired(self) -> bool:
        return self._expired

    @property
    def follow(self) -> str:
        followed_attr: Optional[str] = self.get(self.get("follow"))
        if followed_attr:
            return followed_attr
        return ""

    @follow.setter
    def follow(self, key: str):
        if key in self:
            self["follow"] = key

    def __repr__(self) -> str:
        return f"Session(identity={self.identity}, created={self.created}, changed={self.changed}, data={self._data})"

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._changed = True
        self._created = int(datetime.now().timestamp())

    def __delitem__(self, key: str) -> None:
        del self._data[key]
        self._changed = True
        self._created = int(datetime.now().timestamp())

    def __iter__(self) -> Generator:
        for key in self._data:
            yield key

    def get(self, key: str) -> Any:
        return self._data.get(key)

    def keys(self) -> KeysView:
        return self._data.keys()

    def data(self) -> dict:
        if not self.empty():
            return {"created": self.created, "session": self._data}
        return self._data

    def empty(self) -> bool:
        return not bool(self._data)

    def invalidate(self):
        self._changed = True
        self._expired = True
