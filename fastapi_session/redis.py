import json
from typing import Any, List, Optional

from fastapi import Request
from redis import Redis, Sentinel

from .session import Session
from .storage import Storage


class RedisStorage(Storage):
    def __init__(self, session: Optional[Session] = None, *args, **kwargs):
        super().__init__(Redis(*args, **kwargs))

    def __call__(self, request: Request):
        request.app.FASTAPI_SESSION_STORAGE = self._storage

    def get(self, *args: str) -> Any:
        return self._storage.get(*args)

    def set(self, key: str, value: str) -> None:
        raw_data = json.loads(value)
        pipe = self._storage.pipeline()
        pipe.set(key, value)
        if raw_data["session"].get("follow"):
            follow_data = raw_data["session"][raw_data["session"]["follow"]]
            pipe.zadd(f"active_sessions_{follow_data}", {key: raw_data["created"]})
        pipe.execute()

    def delete(self, key: str, value: Optional[str] = None) -> None:
        pipeline = self._storage.pipeline()
        pipeline.delete(key)
        if value:
            raw_data = json.loads(value).get("session")
            if raw_data.get("follow"):
                follow_data = raw_data[raw_data["follow"]]
                pipeline.zrem(f"active_sessions_{follow_data}", key)
        pipeline.execute()

    def actives(self, key: str) -> List[Any]:
        return self._storage.zrange(f"active_sessions_{key}", 0, -1)


class SentinelStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(Sentinel(*args, **kwargs))

    def __call__(self, request: Request):
        request.app.FASTAPI_SESSION_STORAGE = self._storage

    def get(self, *args: str) -> Any:
        pass

    def set(self, key: str, value: str) -> None:
        pass

    def delete(self, *args: str) -> None:
        pass
