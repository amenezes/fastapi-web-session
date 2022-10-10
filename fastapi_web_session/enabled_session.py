from pydantic import BaseModel


class EnabledSession(BaseModel):
    key: str
    timestamp: float
