from typing import Any, Optional


class Storage:
    def __init__(self, storage_impl) -> None:
        self._storage = storage_impl

    def __repr__(self) -> str:
        impl_str = str(self.__class__).split(".")[-1]
        return f"Storage(impl='{impl_str[0:len(impl_str)-2]}')"

    def get(self, key: str) -> Any:
        raise NotImplementedError

    def set(self, key: str, value: bytes) -> None:
        raise NotImplementedError

    def delete(self, key: str, value: Optional[str] = None) -> None:
        raise NotImplementedError

    def actives(self, key: str):
        raise NotImplementedError
