import pytest


def test_session_repr(session):
    assert (
        repr(session)
        == f"Session(identity={session.identity}, created=None, changed=False, data={session._data})"
    )


def test_empty(session):
    assert session.empty() is True


def test_data_empty(session):
    assert session.data() == {}


def test_data(session):
    session["test"] = "data"
    assert session.data() == {"created": session.created, "session": session._data}


def test_contains(session):
    assert ("test" in session) is False
    session["test"] = "data"
    assert ("test" in session) is True


def test_getitem_empty(session):
    with pytest.raises(KeyError):
        session["test"]


def test_setitem(session):
    assert session.created is None
    assert session.changed is False
    assert "test" not in session
    session["test"] = "data"
    assert "test" in session
    assert isinstance(session.created, int)


def test_delitem(session):
    assert "test" not in session
    session["test"] = "data"
    assert "test" in session
    del session["test"]
    assert "test" not in session


def test_iter(session):
    assert session.empty()
    values = ["a", "b"]
    session["a"] = values[0]
    session["b"] = values[1]
    for s, v in zip(session, values):
        assert s == v


def test_invalidate(session):
    assert session.expired is False
    session.invalidate()
    assert session.expired is True
