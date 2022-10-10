from typing import List, Optional

from fastapi import Request

from .enabled_session import EnabledSession


class Storage:
    def __init__(self, storage_impl) -> None:
        self._storage = storage_impl

    def __call__(self, request: Request):
        request.app.FASTAPI_SESSION_STORAGE = self

    def __repr__(self) -> str:
        impl_str = str(self.__class__).split(".")[-1]
        return f"Storage(impl='{impl_str[0:len(impl_str)-2]}')"

    def get(self, key: str) -> bytes:
        raise NotImplementedError

    def set(self, key: str, value: dict) -> None:
        raise NotImplementedError

    def delete(self, key: str, value: Optional[str] = None) -> None:
        raise NotImplementedError

    def actives(self, key: str) -> List[EnabledSession]:
        raise NotImplementedError
