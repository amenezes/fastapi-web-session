import json
from typing import Any, List, Optional

from fastapi import Request
from redis import Redis, Sentinel

from .constants import DEFAULT_ENCODING
from .session import Session
from .storage import Storage


class RedisStorage(Storage):
    def __init__(self, session: Optional[Session] = None, *args, **kwargs):
        super().__init__(Redis(*args, **kwargs))

    def __call__(self, request: Request):
        request.app.FASTAPI_SESSION_STORAGE = self._storage

    def get(self, key: str) -> Any:
        return self._storage.get(key)

    def set(self, key: str, value: bytes) -> None:
        raw_data = json.loads(value)
        pipe = self._storage.pipeline()
        pipe.set(key, value)
        if raw_data["session"].get("follow"):
            follow_data = raw_data["session"][raw_data["session"]["follow"]]
            pipe.zadd(f"active_sessions_{follow_data}", {key: raw_data["created"]})
        pipe.execute()

    def delete(self, key: str, followed: Optional[str] = None) -> None:
        pipeline = self._storage.pipeline()
        pipeline.delete(key)
        if followed:
            pipeline.zrem(f"active_sessions_{followed}", key)
        pipeline.execute()

    def actives(self, key: str) -> List[str]:
        return [
            session_id.decode(DEFAULT_ENCODING)
            for session_id in self._storage.zrange(f"active_sessions_{key}", 0, -1)
            if session_id is not None
        ]


class SentinelStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(Sentinel(*args, **kwargs))

    def __call__(self, request: Request):
        request.app.FASTAPI_SESSION_STORAGE = self._storage

    def get(self, key: str) -> Any:
        pass

    def set(self, key: str, value: bytes) -> None:
        pass

    def delete(self, key: str, followed: Optional[str] = None) -> None:
        pass

    def actives(self, key: str):
        pass
