import pytest

from fastapi_session import Session
from fastapi_session.storage import Storage


@pytest.fixture
def session():
    yield Session()


@pytest.fixture(scope="session")
def storage():
    return Storage(None)
