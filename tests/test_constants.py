import pytest

from fastapi_web_session.constants import DEFAULT_ENCODING, DEFAULT_SESSION_ID


@pytest.mark.parametrize(
    "default, expected",
    [
        (DEFAULT_ENCODING, "utf-8"),
        (DEFAULT_SESSION_ID, "sessionid"),
    ],
)
def test_defaults(default, expected):
    assert default == expected
