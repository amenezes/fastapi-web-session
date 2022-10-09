import pytest

from fastapi_web_session import Session
from fastapi_web_session.storage import Storage


@pytest.fixture
def session():
    yield Session()


@pytest.fixture(scope="session")
def storage():
    return Storage(None)
