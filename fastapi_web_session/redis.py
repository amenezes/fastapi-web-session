import json
from typing import Any, List, Optional

from redis import Redis, Sentinel

from .constants import DEFAULT_ENCODING
from .enabled_session import EnabledSession
from .session import Session
from .storage import Storage


class RedisStorage(Storage):
    def __init__(self, session: Optional[Session] = None, *args, **kwargs):
        super().__init__(Redis(*args, **kwargs))

    def get(self, key: str) -> bytes:
        return self._storage.get(key)  # type: ignore

    def set(self, key: str, value: dict) -> None:
        pipe = self._storage.pipeline()
        pipe.set(key, json.dumps(value), nx=True)
        if value["session"].get("follow"):
            follow_data = value["session"][value["session"]["follow"]]
            pipe.zadd(f"active_sessions_{follow_data}", {key: value["created"]})
        pipe.execute()

    def delete(self, key: str, followed: Optional[str] = None) -> None:
        pipeline = self._storage.pipeline()
        pipeline.delete(key)
        if followed:
            pipeline.zrem(f"active_sessions_{followed}", key)
        pipeline.execute()

    def actives(self, key: str) -> List[EnabledSession]:
        return [
            EnabledSession(key=session_id.decode(DEFAULT_ENCODING), timestamp=timestamp)
            for session_id, timestamp in self._storage.zrange(
                f"active_sessions_{key}", 0, -1, withscores=True
            )
            if session_id is not None
        ]


class SentinelStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(Sentinel(*args, **kwargs))

    def get(self, key: str) -> Any:
        pass

    def set(self, key: str, value: dict) -> None:
        pass

    def delete(self, key: str, followed: Optional[str] = None) -> None:
        pass

    def actives(self, key: str) -> List[EnabledSession]:
        pass
